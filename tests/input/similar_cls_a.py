class A:
    def parent_method(
        self,
        *,
        a="",
        b=None,
        c=True,
    ):
        """Overridden method example."""

        def _internal_func(
            arg1: int = 1,
            arg2: str = "2",
            arg3: int = 3,
            arg4: bool = True,
        ):
            pass

    class InternalA:
        def some_method_a(
            self,
            *,
            a=None,
            b=False,
            c="",
        ):
            pass
