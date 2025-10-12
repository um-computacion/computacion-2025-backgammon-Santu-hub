from core.board import Board
from core.dice import Dice
from core.player import Player


class BackgammonGame:
    """
    Orquesta el flujo completo de una partida de Backgammon.
    """

    def __init__(self):
        """Inicializa el juego, creando el tablero, los dados y los jugadores."""
        self._board = Board()
        self._dice = Dice()
        self._player1 = Player("Player 1", "W")  # Fichas Blancas (White)
        self._player2 = Player("Player 2", "B")  # Fichas Negras (Black)

        # Configura el tablero con la posición inicial de las fichas
        self._board._setup_initial_checkers(self._player1, self._player2)

    def roll_dice(self):
        """Lanza los dados y devuelve los valores."""
        return self._dice.roll()

    def get_board(self) -> Board:
        """Devuelve la instancia del tablero."""
        return self._board

    def get_player1(self) -> Player:
        """Devuelve al jugador 1."""
        return self._player1

    def get_player2(self) -> Player:
        """Devuelve al jugador 2."""
        return self._player2

