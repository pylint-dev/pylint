A common issue is that this message is triggered when using `pytest` `fixtures <https://docs.pytest.org/en/7.1.x/how-to/fixtures.html>`_:

.. code-block:: python

    import pytest

    @pytest.fixture
    def setup():
        ...


    def test_something(setup):  # [redefined-outer-name]
        ...

One solution to this problem is to explicitly name the fixture:

.. code-block:: python

    @pytest.fixture(name="setup")
    def setup_fixture():
        ...

Alternatively `pylint` plugins like `pylint-pytest <https://pypi.org/project/pylint-pytest/>`_ can be used.
