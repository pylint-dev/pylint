# pylint: disable=missing-function-docstring, missing-module-docstring, invalid-name, import-outside-toplevel
import codecs
import multiprocessing
import subprocess
import tarfile
import tempfile
import threading
import urllib
import zipfile
from concurrent import futures


def test_codecs_open():
    fh = codecs.open("test.txt", "utf8")  # [consider-using-with]
    fh.close()


def test_urlopen():
    _ = urllib.request.urlopen("http://www.python.org")  # [consider-using-with]


def test_temporary_file():
    _ = tempfile.TemporaryFile("r")  # [consider-using-with]


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

    # Not working currently
    # condition = threading.Condition()
    # condition.acquire()
    # condition.release()

    # with condition:  # must not trigger
    #     pass

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


def test_futures():
    _ = futures.ThreadPoolExecutor()  # [consider-using-with]
    with futures.ThreadPoolExecutor():
        pass

    _ = futures.ProcessPoolExecutor()  # [consider-using-with]
    with futures.ProcessPoolExecutor():
        pass


def test_popen():
    _ = subprocess.Popen("sh")  # [consider-using-with]
    with subprocess.Popen("sh"):
        pass
