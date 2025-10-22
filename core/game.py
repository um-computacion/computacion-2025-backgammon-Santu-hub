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
        self.current_player = self._player1

        # Configura el tablero con la posición inicial de las fichas
        self._board._setup_initial_checkers(self._player1, self._player2)

    def switch_player(self):
        """Cambia el turno al siguiente jugador."""
        self.current_player = self._player2 if self.current_player == self._player1 else self._player1

    def check_winner(self) -> Player | None:
        """Verifica si alguno de los jugadores ha ganado."""
        if self._board.has_won(self._player1):
            return self._player1
        if self._board.has_won(self._player2):
            return self._player2
        return None

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


