# pylint: disable=missing-function-docstring, missing-module-docstring, invalid-name, import-outside-toplevel
import codecs
import contextlib
import multiprocessing
import pathlib
import subprocess
import tarfile
import tempfile
import threading
import urllib
import zipfile
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from pathlib import Path


def test_pathlib_open():
    _ = pathlib.Path("foo").open(encoding="utf8")  # [consider-using-with]
    _ = Path("foo").open(encoding="utf8")  # [consider-using-with]
    path = Path("foo")
    _ = path.open(encoding="utf8")  # [consider-using-with]
    with Path("foo").open(encoding="utf8") as file:  # must not trigger
        _ = file.read()


def test_codecs_open():
    fh = codecs.open("test.txt", "utf8")  # [consider-using-with]
    fh.close()


def test_urlopen():
    _ = urllib.request.urlopen("http://www.python.org")  # [consider-using-with]


def test_temporary_file():
    _ = tempfile.TemporaryFile("r")  # ambiguous with NamedTemporaryFile


def test_named_temporary_file():
    _ = tempfile.NamedTemporaryFile("r")  # [consider-using-with]


def test_spooled_temporary_file():
    _ = tempfile.SpooledTemporaryFile("r")  # [consider-using-with]


def test_temporary_directory():
    _ = tempfile.TemporaryDirectory()  # [consider-using-with]


def test_zipfile():
    myzip = zipfile.ZipFile("spam.zip", "w")  # [consider-using-with]
    _ = myzip.open("eggs.txt")  # [consider-using-with]


def test_pyzipfile():
    myzip = zipfile.PyZipFile("spam.zip", "w")  # [consider-using-with]

    with zipfile.PyZipFile("spam.zip", "w"):  # must not trigger
        pass

    _ = myzip.open("eggs.txt")  # [consider-using-with]

    with myzip.open("eggs.txt"):  # must not trigger
        pass


def test_tarfile():
    tf = tarfile.open("/tmp/test.tar", "w")  # [consider-using-with]
    tf.close()

    with tarfile.open("/tmp/test.tar", "w"):  # must not trigger
        pass

    tf = tarfile.TarFile("/tmp/test2.tar", "w")  # [consider-using-with]
    tf.close()

    with tarfile.TarFile("/tmp/test2.tar", "w"):  # must not trigger
        pass


def test_lock_acquisition():
    lock = threading.Lock()
    lock.acquire()  # [consider-using-with]
    lock.release()

    with lock:  # must not trigger
        pass

    rlock = threading.RLock()
    rlock.acquire()  # [consider-using-with]
    rlock.release()

    with rlock:  # must not trigger
        pass

    sema = threading.Semaphore()
    sema.acquire()  # [consider-using-with]
    sema.release()

    with sema:  # must not trigger
        pass

    bounded_sema = threading.BoundedSemaphore()
    bounded_sema.acquire()  # [consider-using-with]
    bounded_sema.release()

    with bounded_sema:  # must not trigger
        pass


@contextlib.contextmanager
def test_lock_acquisition_in_context_manager1():
    """
    The message must not be triggered if the resource allocation is done inside a context manager.
    """
    lock = threading.Lock()
    lock.acquire()  # must not trigger
    yield
    lock.release()


class MyLockContext:
    """
    The message must not be triggered if the resource allocation is done inside a context manager.
    """

    def __init__(self):
        self.lock = threading.Lock()

    def __enter__(self):
        self.lock.acquire()  # must not trigger

    def __exit__(self, exc_type, exc_value, traceback):
        self.lock.release()


def test_multiprocessing():
    # the different Locks provided by multiprocessing would be candidates
    # for consider-using-with as well, but they lead to InferenceErrors.
    _ = multiprocessing.Pool()  # [consider-using-with]
    with multiprocessing.Pool():
        pass

    manager = multiprocessing.managers.BaseManager()
    manager.start()  # [consider-using-with]
    with multiprocessing.managers.BaseManager():
        pass

    manager = multiprocessing.managers.SyncManager()
    manager.start()  # [consider-using-with]
    with multiprocessing.managers.SyncManager():
        pass


def test_popen():
    _ = subprocess.Popen("sh")  # [consider-using-with]
    with subprocess.Popen("sh"):
        pass


def test_suppress_in_exit_stack():
    """Regression test for issue #4654 (false positive)"""
    with contextlib.ExitStack() as stack:
        _ = stack.enter_context(
            open("/sys/firmware/devicetree/base/hwid,location", "r", encoding="utf-8")
        )  # must not trigger


def test_futures():
    """
    Regression test for issue #4689.
    ThreadPoolExecutor and ProcessPoolExecutor were formerly part of the callables that raised
    the R1732 message if used outside a with block, but there are legitimate use cases where
    Executor instances are used e.g. as a persistent background worker pool throughout the program.
    """
    thread_executor = ThreadPoolExecutor()
    thread_executor.submit(print, 1)
    process_executor = ProcessPoolExecutor()
    process_executor.submit(print, 2)
    thread_executor.shutdown()
    process_executor.shutdown()


pool = multiprocessing.Pool()  # must not trigger, as it is used later on
with pool:
    pass


global_pool = multiprocessing.Pool()  # must not trigger, will be used in nested scope


def my_nested_function():
    with global_pool:
        pass


# this must also work for tuple unpacking
pool1, pool2 = (
    multiprocessing.Pool(),  # must not trigger
    multiprocessing.Pool(),  # must not trigger
)

with pool1:
    pass

with pool2:
    pass

unused_pool1, unused_pool2 = (
    multiprocessing.Pool(),  # [consider-using-with]
    multiprocessing.Pool(),  # [consider-using-with]
)

used_pool, unused_pool = (
    multiprocessing.Pool(),  # must not trigger
    multiprocessing.Pool(),  # [consider-using-with]
)
with used_pool:
    pass

unused_pool, used_pool = (
    multiprocessing.Pool(),  # [consider-using-with]
    multiprocessing.Pool(),  # must not trigger
)
with used_pool:
    pass


def test_subscript_assignment():
    """
    Regression test for issue https://github.com/pylint-dev/pylint/issues/4732.
    If a context manager is assigned to a list or dict, we are not able to
    tell if / how the context manager is used later on, as it is not assigned
    to a variable or attribute directly.
    In this case we can only emit the message directly.
    """
    job_list = [None, None]
    job_list[0] = subprocess.Popen("ls")  # [consider-using-with]
    job_dict = {}
    job_dict["myjob"] = subprocess.Popen("ls")  # [consider-using-with]
