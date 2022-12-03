If you attempt to disable this message via ``# pylint: disable=line-too-long`` in a module with no code, you may receive a message for ``useless-suppression``. This is a false positive of ``useless-suppression`` we can't easily fix.

See https://github.com/PyCQA/pylint/issues/3368 for more information.
