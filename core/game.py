from core.board import Board
from core.dice import Dice

class BackgammonGame:
    """
    Orquesta el flujo del juego.
    Por ahora solo inicializa tablero y dados.
    """

    def __init__(self):
        self.__board__ = Board()
        self.__dice__ = Dice()

    def roll_dice(self):
        return self.__dice__.roll()

    def get_board(self):
        return self.__board__
