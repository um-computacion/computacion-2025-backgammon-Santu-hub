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
        __remaining_moves__ (List[int]): Movimientos restantes en el turno actual
    """

    def __init__(self):
        """
        Inicializa el juego, creando el tablero, los dados y los jugadores.
        """
        self.__board__ = Board()
        self.__dice__ = Dice()
        self.__player1__ = Player("Player 1", "W")
        self.__player2__ = Player("Player 2", "B")
        self.__current_player__ = self.__player1__
        self.__remaining_moves__ = []
        self.start_new_game("Player 1", "Player 2")

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
        self.__remaining_moves__ = []

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
        self.__remaining_moves__ = self.__dice__.roll()
        return self.__remaining_moves__

    def get_remaining_moves(self) -> List[int]:
        """
        Devuelve los valores de dados restantes.
        
        Returns:
            List[int]: Lista con los valores de los dados no utilizados
        """
        return self.__remaining_moves__

    def make_move(self, from_point: int, die_value: int) -> bool:
        """
        Realiza un movimiento.
        
        Args:
            from_point (int): Punto de origen (1-24, 25 para la barra)
            die_value (int): Valor del dado a utilizar
        
        Returns:
            bool: True si el movimiento fue exitoso, False en caso contrario
        """
        if die_value not in self.__remaining_moves__:
            return False

        player = self.get_current_player()
        
        try:
            if from_point == 25:
                self.__board__.move_checker_from_bar(player, die_value)
            else:
                self.__board__.move_checker(player, from_point - 1, die_value)
            
            self.__remaining_moves__.remove(die_value)
            return True
        except ValueError:
            return False

    def has_valid_moves(self) -> bool:
        """
        Verifica si el jugador actual tiene movimientos válidos.
        
        Returns:
            bool: True si hay movimientos válidos, False en caso contrario
        """
        player = self.get_current_player()

        if not self.__remaining_moves__:
            return False

        if self.__board__.get_bar(player.get_color()) > 0:
            return any(
                self.__board__.is_valid_move(player, 25, die)
                for die in self.__remaining_moves__
            )

        for point_idx, point in enumerate(self.__board__.get_all_points()):
            if point and point[0] == player:
                if any(self.__board__.is_valid_move(player, point_idx, die) for die in self.__remaining_moves__):
                    return True

        return False

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

    def start_new_game(self, name1: str, name2: str):
        """
        Establece los nombres de los jugadores y reinicia el tablero.
        
        Args:
            name1 (str): Nombre del jugador 1
            name2 (str): Nombre del jugador 2
        """
        self.__player1__ = Player(name1, "W")
        self.__player2__ = Player(name2, "B")
        self.__current_player__ = self.__player1__
        self.__board__.setup_initial_checkers(self.__player1__, self.__player2__)
