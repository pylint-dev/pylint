# pylint: disable=missing-docstring,unused-argument,pointless-statement
# pylint: disable=too-few-public-methods

class Gateaux:
    def nihon(self, a, r, i, /, cheese=False):
        return f"{a}{r}{i}gateaux" + " au fromage" if cheese else ""


cake = Gateaux()
# Should not emit error
cake.nihon(1, 2, 3)
cake.nihon(1, 2, 3, True)
cake.nihon(1, 2, 3, cheese=True)
# Emits error
cake.nihon(1, 2, i=3)  # [positional-only-arguments-expected]
cake.nihon(1, r=2, i=3)  # [positional-only-arguments-expected]
cake.nihon(a=1, r=2, i=3)  # [positional-only-arguments-expected]
cake.nihon(1, r=2, i=3, cheese=True)  # [positional-only-arguments-expected]
