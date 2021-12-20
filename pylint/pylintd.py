import sys
from http.server import BaseHTTPRequestHandler, HTTPServer, HTTPStatus
from io import StringIO

from pylint.__pkginfo__ import __version__
from pylint.lint.pylinter import MANAGER, PyLinter
from pylint.lint.run import BaseRun
from pylint.lint.utils import fix_import_path
from pylint.reporters import json_reporter, text
from pylint.typing import FileItem

CONTENT_TYPE_MAPPING = {
    "application/X-pylint-text": text.TextReporter,
    "application/X-pylint-parseable": text.ParseableTextReporter,
    "application/X-pylint-msvs": text.VSTextReporter,
    "application/X-pylint-json": json_reporter.JSONReporter,
}


class DaemonRun(BaseRun):
    """Class implementing pylintd.

    ## Request:

    Method `GET` with path `/`.
    Header `X-Protocol-Version` is the pylintd protocol version. Currently supports only value 1. This parameter is optional.
    Header `X-File-Name` is the name of the file to be checked.
    Header `accept` is the response content type representing reporter to be used for generating pylint report.

    ## Response:

    The protocol following http response status codes:
        * status code 200 - pylint successfully linted the file. This is equivalent pylint returning status code 0.
        * status code 400 - sent request cannot be processed by pylint due wrong format.
        * status code 406 - pylint successfully linted the file but the code is not meeting the quality standards.
          This is equivalent pylint returning non-zero status code.

    Header `X-Pylint-Status` contains status code returned by pylint.

    The body contains pylint report.

    Example:

        $ curl -v -H "X-File-Name:test.py" -H accept:application/X-pylint-parseable localhost:8000
        *   Trying 127.0.0.1...
        * TCP_NODELAY set
        * Connected to localhost (127.0.0.1) port 8000 (#0)
        > GET / HTTP/1.1
        > Host: localhost:8000
        > User-Agent: curl/7.64.1
        > X-File-Name:test.py
        > accept:application/X-pylint-parseable
        >
        * HTTP 1.0, assume close after body
        < HTTP/1.0 406 Not Acceptable
        < Server: pylintd/2.11.2-dev0 Python/3.9.7
        < Date: Thu, 25 Nov 2021 21:13:14 GMT
        < Content-type: application/X-pylint-parseable
        < Content-Length: 308
        < X-Pylint-Status: 6
        <
        ************* Module test
        test.py:2: [E1101(no-member), ] Module 'pdb' has no 'breakpoint' member
        test.py:3: [W0107(unnecessary-pass), ] Unnecessary pass statement

        ----------------------------------------------------------------------
        Your code has been rated at -10.00/10 (previous run: -10.00/10, +0.00)

        * Closing connection 0
    """

    def __init__(self, args: list, port: int):

        run_linter = self.run_linter

        class PylintdHTTPRequestHandler(BaseHTTPRequestHandler):

            server_version = "pylintd/" + __version__

            def do_GET(self) -> None:
                protocol_version = int(self.headers.get("X-Protocol-Version", 1))
                if protocol_version != 1:
                    self.send_error(400, "Wrong X-Protocol-Version header")
                    return
                file_name = self.headers.get("X-File-Name", None)
                if not file_name:
                    self.send_error(400, "Wrong X-File-Name header")
                    return
                pylint_output = StringIO()
                result_format = self.headers.get("accept", "application/X-pylint-text")
                try:
                    reporter = CONTENT_TYPE_MAPPING[result_format](pylint_output)
                except KeyError:
                    self.send_error(400, "Wrong accept header")
                    return

                linter.set_reporter(reporter)
                score_value = run_linter(linter, file_name)

                if linter.config.exit_zero:
                    http_response = HTTPStatus.OK
                    status_code = 0
                elif linter.any_fail_on_issues():
                    # We need to make sure we return a failing exit code in this case.
                    # So we use self.linter.msg_status if that is non-zero, otherwise we just return 1.
                    http_response = HTTPStatus.NOT_ACCEPTABLE
                    status_code = linter.msg_status or 1
                elif (
                    score_value is not None and score_value >= linter.config.fail_under
                ):
                    http_response = HTTPStatus.OK
                    status_code = 0
                else:
                    http_response = HTTPStatus.NOT_ACCEPTABLE
                    status_code = linter.msg_status

                self.send_response(http_response)
                body = pylint_output.getvalue().encode("utf8")
                self.send_header("Content-type", result_format)
                self.send_header("Content-Length", len(body))
                self.send_header("X-Pylint-Status", status_code)
                self.end_headers()
                self.wfile.write(body)

        linter, args = self.initialize(args, None)
        self.initialize_jobs(linter)

        server_address = ("", port)
        with HTTPServer(server_address, PylintdHTTPRequestHandler) as httpd:
            httpd.serve_forever()

    @staticmethod
    def run_linter(linter: PyLinter, file_or_module: FileItem) -> int:
        linter.initialize()
        with fix_import_path([file_or_module]):
            linter.open()
            file_item = next(linter._iterate_file_descrs([file_or_module]))
            # Remove the checked file from cache
            # FIXME: Changing another cached file without clearing cache can lead to errors.
            MANAGER.astroid_cache.pop(file_item.name, None)
            linter.check_single_file_item(file_item)
        score_value = linter.generate_reports()
        return score_value


if __name__ == "__main__":
    try:
        DaemonRun(sys.argv, 8000)
    except KeyboardInterrupt:
        pass
