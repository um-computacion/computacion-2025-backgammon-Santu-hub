from core.board import Board
from core.dice import Dice
from core.player import Player
from typing import List


class BackgammonGame:
    """
    Orquesta el flujo completo de una partida de Backgammon.
    
    Coordina la interacción entre el tablero, los dados y los jugadores,
    gestionando el flujo del juego y las condiciones de victoria.
    
    Attributes:
        __board__ (Board): Tablero de juego
        __dice__ (Dice): Dados del juego
        __player1__ (Player): Primer jugador (Blancas)
        __player2__ (Player): Segundo jugador (Negras)
        __current_player__ (Player): Jugador con el turno actual
    """

    def __init__(self):
        """
        Inicializa el juego, creando el tablero, los dados y los jugadores.
        Configura el tablero con la posición inicial de las fichas.
        """
        self.__board__ = Board()
        self.__dice__ = Dice()
        self.__player1__ = Player("Player 1", "W")  # Fichas Blancas (White)
        self.__player2__ = Player("Player 2", "B")  # Fichas Negras (Black)
        self.__current_player__ = self.__player1__

        # Configura el tablero con la posición inicial de las fichas
        self.__board__.setup_initial_checkers(self.__player1__, self.__player2__)

    def get_current_player(self) -> Player:
        """
        Devuelve el jugador con el turno actual.
        
        Returns:
            Player: Jugador actual
        """
        return self.__current_player__

    def switch_player(self):
        """
        Cambia el turno al siguiente jugador.
        """
        self.__current_player__ = (
            self.__player2__ if self.__current_player__ == self.__player1__ 
            else self.__player1__
        )

    def check_winner(self) -> Player | None:
        """
        Verifica si alguno de los jugadores ha ganado.
        
        Returns:
            Player | None: El jugador ganador o None si no hay ganador aún
        """
        if self.__board__.has_won(self.__player1__):
            return self.__player1__
        if self.__board__.has_won(self.__player2__):
            return self.__player2__
        return None

    def roll_dice(self) -> List[int]:
        """
        Lanza los dados y devuelve los valores.
        
        Returns:
            List[int]: Lista con los valores de los dados (2 o 4 elementos si hay dobles)
        """
        return self.__dice__.roll()

    def get_board(self) -> Board:
        """
        Devuelve la instancia del tablero.
        
        Returns:
            Board: Tablero de juego
        """
        return self.__board__

    def get_player1(self) -> Player:
        """
        Devuelve al jugador 1.
        
        Returns:
            Player: Primer jugador (Blancas)
        """
        return self.__player1__

    def get_player2(self) -> Player:
        """
        Devuelve al jugador 2.
        
        Returns:
            Player: Segundo jugador (Negras)
        """
        return self.__player2__