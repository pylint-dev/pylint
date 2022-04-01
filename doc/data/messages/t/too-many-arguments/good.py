from dataclasses import dataclass


@dataclass
class ThreeDChessPiece:
    x: int
    y: int
    z: int
    type: str


def three_d_chess_move(
    white: ThreeDChessPiece,
    black: ThreeDChessPiece,
    blue: ThreeDChessPiece,
    current_player,
):
    pass
