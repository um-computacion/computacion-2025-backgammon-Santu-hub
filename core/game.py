from core.board import Board
from core.dice import Dice
from core.player import Player


class BackgammonGame:
    """
    Orquesta el flujo completo de una partida de Backgammon.
    """

    def __init__(self):
        """Inicializa el juego, creando el tablero, los dados y los jugadores."""
        self.__board__ = Board()
        self.__dice__ = Dice()
        self.__player1__ = Player("Player 1", "W")  # Fichas Blancas (White)
        self.__player2__ = Player("Player 2", "B")  # Fichas Negras (Black)

        # Configura el tablero con la posición inicial de las fichas
        self.__board__.__setup_initial_checkers__(self.__player1__, self.__player2__)

    def __roll_dice__(self):
        """Lanza los dados y devuelve los valores."""
        return self.__dice__.roll()

    def __get_board__(self) -> Board:
        """Devuelve la instancia del tablero."""
        return self.__board__

    def __get_player1__(self) -> Player:
        """Devuelve al jugador 1."""
        return self.__player1__

    def __get_player2__(self) -> Player:
        """Devuelve al jugador 2."""
        return self.__player2__
