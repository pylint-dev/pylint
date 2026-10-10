# pylint: disable=missing-docstring, redundant-keyword-arg, invalid-name, line-too-long
import threading


threading.Thread(lambda: None).run()  # [bad-thread-instantiation]
threading.Thread(None, lambda: None)
threading.Thread(lambda: None, group=None)  # [bad-thread-instantiation]
threading.Thread()  # [bad-thread-instantiation]

threading.Thread(group=None, target=lambda: None).run()
threading.Thread(group=None, target=None, name=None, args=(), kwargs={})
threading.Thread(None, None, "name")

def thread_target(n):
    print(n ** 2)


thread = threading.Thread(thread_target, args=(10,))  # [bad-thread-instantiation]


kw = {'target_typo': lambda x: x}
# kw may have gained a target since its assignment
threading.Thread(None, **kw)  # [unexpected-keyword-arg]

threading.Thread(None, target_typo=lambda x: x)  # [unexpected-keyword-arg, bad-thread-instantiation]

threading.Thread(**{"target": thread_target})
threading.Thread(None, **{"target": thread_target})
threading.Thread(**{"name": "worker"})  # [bad-thread-instantiation]
threading.Thread(None, **{})  # [bad-thread-instantiation]
threading.Thread(*[None, thread_target])


def thread_with_forwarded_kwargs(**kwargs):
    return threading.Thread(**kwargs)


def thread_with_opaque_options(options):
    return threading.Thread(**options)


def thread_with_extra_options(options):
    return threading.Thread(**{"name": "worker", **options})


def thread_with_variable_key(key):
    return threading.Thread(**{key: thread_target})
