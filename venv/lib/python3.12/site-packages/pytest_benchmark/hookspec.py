"""
..
  PYTEST_DONT_REWRITE
"""

import pytest


@pytest.hookspec(firstresult=True)
def pytest_benchmark_scale_unit(config, unit, benchmarks, best, worst, sort):
    """
    To have custom time scaling do something like this:

    .. sourcecode:: python

        def pytest_benchmark_scale_unit(config, unit, benchmarks, best, worst, sort):
            if unit == 'seconds':
                prefix = ''
                scale = 1.0
            elif unit == 'operations':
                prefix = 'K'
                scale = 0.001
            else:
                raise RuntimeError("Unexpected measurement unit %r" % unit)

            return prefix, scale
    """


@pytest.hookspec(firstresult=True)
def pytest_benchmark_generate_machine_info(config):
    """
    To completely replace the generated machine_info do something like this:

    .. sourcecode:: python

        def pytest_benchmark_generate_machine_info(config):
            return {'user': getpass.getuser()}
    """


def pytest_benchmark_update_machine_info(config, machine_info):
    """
    If benchmarks are compared and machine_info is different then warnings will be shown.

    To add the current user to the commit info override the hook in your conftest.py like this:

    .. sourcecode:: python

        def pytest_benchmark_update_machine_info(config, machine_info):
            machine_info['user'] = getpass.getuser()
    """


@pytest.hookspec(firstresult=True)
def pytest_benchmark_generate_commit_info(config):
    """
    To completely replace the generated commit_info do something like this:

    .. sourcecode:: python

        def pytest_benchmark_generate_commit_info(config):
            return {'id': subprocess.check_output(['svnversion']).strip()}
    """


def pytest_benchmark_update_commit_info(config, commit_info):
    """
    To add something into the commit_info, like the commit message do something like this:

    .. sourcecode:: python

        def pytest_benchmark_update_commit_info(config, commit_info):
            commit_info['message'] = subprocess.check_output(['git', 'log', '-1', '--pretty=%B']).strip()
    """


@pytest.hookspec(firstresult=True)
def pytest_benchmark_group_stats(config, benchmarks, group_by):
    """
    You may perform grouping customization here, in case the builtin grouping doesn't suit you.

    Example:

    .. sourcecode:: python

        @pytest.hookimpl(wrapper=True)
        def pytest_benchmark_group_stats(config, benchmarks, group_by):
            outcome = yield
            if group_by == "special":  # when you use --benchmark-group-by=special
                result = defaultdict(list)
                for bench in benchmarks:
                    # `bench.special` doesn't exist, replace with whatever you need
                    result[bench.special].append(bench)
                outcome.force_result(result.items())
    """


@pytest.hookspec(firstresult=True)
def pytest_benchmark_generate_json(config, benchmarks, include_data, machine_info, commit_info):
    """
    You should read pytest-benchmark's code if you really need to wholly customize the json.

    .. warning::

        Improperly customizing this may cause breakage if ``--benchmark-compare`` or ``--benchmark-histogram`` are used.

    By default, ``pytest_benchmark_generate_json`` strips benchmarks that have errors from the output. To prevent this,
    implement the hook like this:

    .. sourcecode:: python

        @pytest.hookimpl(wrapper=True)
        def pytest_benchmark_generate_json(config, benchmarks, include_data, machine_info, commit_info):
            for bench in benchmarks:
                bench.has_error = False
            yield
    """


def pytest_benchmark_update_json(config, benchmarks, output_json):
    """
    Use this to add custom fields in the output JSON.

    Example:

    .. sourcecode:: python

        def pytest_benchmark_update_json(config, benchmarks, output_json):
            output_json['foo'] = 'bar'
    """


def pytest_benchmark_compare_machine_info(config, benchmarksession, machine_info, compared_benchmark):
    """
    You may want to use this hook to implement custom checks or abort execution.
    ``pytest-benchmark`` builtin hook does this:

    .. sourcecode:: python

        def pytest_benchmark_compare_machine_info(config, benchmarksession, machine_info, compared_benchmark):
            if compared_benchmark["machine_info"] != machine_info:
                benchmarksession.logger.warning(
                    "Benchmark machine_info is different. Current: %s VS saved: %s." % (
                        format_dict(machine_info),
                        format_dict(compared_benchmark["machine_info"]),
                    )
            )
    """
