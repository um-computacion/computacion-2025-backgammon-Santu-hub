from typing import List, Dict
from core.player import Player

BEAR_OFF_W_POINT = 24
BEAR_OFF_B_POINT = -1


class Board:
    """
    Representa el tablero de Backgammon con 24 puntos y la barra.
    
    Attributes:
        __points__ (List[List[Player]]): Lista de 24 puntos, cada uno contiene fichas (Players)
        __borne_off__ (Dict[str, int]): Fichas retiradas por cada jugador
        __bar__ (Dict[str, int]): Fichas en la barra por cada jugador
    """

    def __init__(self):
        """Inicializa un tablero vacío con 24 puntos."""
        self.__points__: List[List[Player]] = [[] for _ in range(24)]
        self.__borne_off__: Dict[str, int] = {"W": 0, "B": 0}
        self.__bar__: Dict[str, int] = {"W": 0, "B": 0}

    def setup_initial_checkers(self, p1: Player, p2: Player):
        """
        Configura la posición inicial de las fichas en el tablero.
        
        Args:
            p1 (Player): Primer jugador (Blancas)
            p2 (Player): Segundo jugador (Negras)
        """
        self.__points__ = [[] for _ in range(24)]
        self.__borne_off__ = {"W": 0, "B": 0}
        self.__bar__ = {"W": 0, "B": 0}

        initial_setup = {
            0: (p1, 2), 5: (p2, 5), 7: (p2, 3), 11: (p1, 5),
            12: (p2, 5), 16: (p1, 3), 18: (p1, 5), 23: (p2, 2),
        }
        for point, (player, count) in initial_setup.items():
            for _ in range(count):
                self.place_checker(point, player)

    def get_point(self, index: int) -> List[Player]:
        """
        Devuelve la lista de jugadores (fichas) en un punto.
        
        Args:
            index (int): Índice del punto (0-23)
            
        Returns:
            List[Player]: Lista de fichas en ese punto
            
        Raises:
            IndexError: Si el índice está fuera del rango válido
        """
        if 0 <= index < 24:
            return self.__points__[index]
        raise IndexError("Índice de punto inválido")

    def get_bar(self, color: str) -> int:
        """
        Devuelve la cantidad de fichas en la barra para un jugador.
        
        Args:
            color (str): Color del jugador ("W" o "B")
            
        Returns:
            int: Cantidad de fichas en la barra
        """
        return self.__bar__[color]

    def get_borne_off(self, color: str) -> int:
        """
        Devuelve la cantidad de fichas retiradas para un jugador.
        
        Args:
            color (str): Color del jugador ("W" o "B")
            
        Returns:
            int: Cantidad de fichas retiradas
        """
        return self.__borne_off__[color]

    def get_all_points(self) -> List[List[Player]]:
        """
        Devuelve todos los puntos del tablero.
        
        Returns:
            List[List[Player]]: Lista con los 24 puntos
        """
        return self.__points__

    def place_checker(self, index: int, player: Player):
        """
        Coloca una ficha de un jugador en un punto del tablero.
        
        Args:
            index (int): Índice del punto (0-23)
            player (Player): Jugador que coloca la ficha
            
        Raises:
            IndexError: Si el índice está fuera del rango válido
        """
        if 0 <= index < 24:
            self.__points__[index].append(player)
        else:
            raise IndexError("Índice de punto inválido")

    def is_ready_to_bear_off(self, player: Player) -> bool:
        """
        Verifica si todas las fichas de un jugador están en su home board.
        
        Args:
            player (Player): Jugador a verificar
            
        Returns:
            bool: True si puede retirar fichas, False en caso contrario
        """
        home_board_range = range(18, 24) if player.get_color() == "W" else range(0, 6)
        checkers_in_home_board = sum(
            len(self.get_point(i))
            for i in home_board_range
            if self.get_point(i) and self.get_point(i)[0] == player
        )
        return checkers_in_home_board + self.get_borne_off(player.get_color()) == 15

    def has_won(self, player: Player) -> bool:
        """
        Verifica si un jugador ha ganado (ha retirado sus 15 fichas).
        
        Args:
            player (Player): Jugador a verificar
            
        Returns:
            bool: True si el jugador ganó, False en caso contrario
        """
        return self.get_borne_off(player.get_color()) == 15

    def _can_move_to_point(self, player: Player, to_point: int) -> bool:
        """Verifica si un punto de destino es válido para un movimiento."""
        if not (0 <= to_point < 24):
            return False

        destination_content = self.get_point(to_point)
        return (
            not destination_content or
            destination_content[0] == player or
            len(destination_content) == 1
        )

    def is_valid_move(self, player: Player, from_point: int, die_value: int) -> bool:
        """
        Verifica si un movimiento es válido sin ejecutarlo.
        
        Args:
            player (Player): Jugador que realiza el movimiento
            from_point (int): Punto de origen (0-24, 25 para la barra)
            die_value (int): Valor del dado
            
        Returns:
            bool: True si el movimiento es válido, False en caso contrario
        """
        if from_point == 25:
            if self.get_bar(player.get_color()) == 0:
                return False
            to_point = (die_value - 1) if player.get_color() == "W" else (24 - die_value)
            return self._can_move_to_point(player, to_point)

        source_content = self.get_point(from_point)
        if not source_content or source_content[0] != player:
            return False

        direction = 1 if player.get_color() == "W" else -1
        to_point = from_point + die_value * direction

        if self.is_ready_to_bear_off(player):
            is_exact_move = (player.get_color() == 'W' and from_point + die_value == 24) or \
                            (player.get_color() == 'B' and from_point - die_value == -1)
            
            if is_exact_move:
                return True

            is_overshoot = (player.get_color() == 'W' and to_point > 24) or \
                           (player.get_color() == 'B' and to_point < -1)

            if is_overshoot:
                if player.get_color() == 'W':
                    higher_points_range = range(from_point + 1, 24)
                else:
                    higher_points_range = range(0, from_point)
                return not any(self.get_point(i) and self.get_point(i)[0] == player for i in higher_points_range)

        return self._can_move_to_point(player, to_point)

    def move_checker(self, player: Player, from_point: int, die_value: int):
        """
        Mueve una ficha de un punto a otro o la retira del tablero.

        Args:
            player (Player): Jugador que realiza el movimiento
            from_point (int): Punto de origen (0-23)
            die_value (int): Valor del dado a utilizar

        Raises:
            ValueError: Si el movimiento es inválido
        """
        if not self.is_valid_move(player, from_point, die_value):
            raise ValueError("Movimiento inválido.")

        direction = 1 if player.get_color() == "W" else -1
        to_point = from_point + die_value * direction
        source_content = self.get_point(from_point)

        if self.is_ready_to_bear_off(player) and \
           ((player.get_color() == "W" and to_point >= 24) or \
            (player.get_color() == "B" and to_point <= -1)):
            source_content.pop()
            self.__borne_off__[player.get_color()] += 1
            return

        destination_content = self.get_point(to_point)
        if destination_content and destination_content[0] != player:
            opponent_checker = destination_content.pop()
            self.__bar__[opponent_checker.get_color()] += 1

        source_content.pop()
        self.place_checker(to_point, player)

    def move_checker_from_bar(self, player: Player, die_value: int):
        """
        Mueve una ficha desde la barra al tablero.
        
        Args:
            player (Player): Jugador que reingresa la ficha
            die_value (int): Valor del dado a utilizar
            
        Raises:
            ValueError: Si el movimiento es inválido
        """
        if not self.is_valid_move(player, 25, die_value):
            raise ValueError("Movimiento desde la barra inválido.")

        to_point = (die_value - 1) if player.get_color() == "W" else (24 - die_value)
        
        destination_content = self.get_point(to_point)
        if destination_content and destination_content[0] != player:
            opponent_checker = destination_content.pop()
            self.__bar__[opponent_checker.get_color()] += 1

        self.__bar__[player.get_color()] -= 1
        self.place_checker(to_point, player)
