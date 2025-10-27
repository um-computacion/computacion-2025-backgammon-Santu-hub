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
        # Limpia el tablero por si se reutiliza
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
        off_home_board_range = range(0, 18) if player.get_color() == "W" else range(6, 24)
        for point_idx in off_home_board_range:
            if player in self.__points__[point_idx]:
                return False
        return self.__bar__[player.get_color()] == 0

    def has_won(self, player: Player) -> bool:
        """
        Verifica si un jugador ha ganado (ha retirado sus 15 fichas).
        
        Args:
            player (Player): Jugador a verificar
            
        Returns:
            bool: True si el jugador ganó, False en caso contrario
        """
        return self.__borne_off__[player.get_color()] == 15

    def move_checker(self, player: Player, from_point: int, to_point: int, dice_roll: List[int]):
        """
        Mueve una ficha de un punto a otro o la retira del tablero, validando el movimiento.
        
        Args:
            player (Player): Jugador que realiza el movimiento
            from_point (int): Punto de origen
            to_point (int): Punto de destino o BEAR_OFF_*_POINT
            dice_roll (List[int]): Valores disponibles de dados
            
        Raises:
            ValueError: Si el movimiento es inválido
        """
        is_bearing_off = (player.get_color() == "W" and to_point == BEAR_OFF_W_POINT) or \
                         (player.get_color() == "B" and to_point == BEAR_OFF_B_POINT)
        
        if self.__bar__[player.get_color()] > 0:
            raise ValueError("Debes reingresar tus fichas desde la barra primero.")

        source_point_content = self.get_point(from_point)
        if not source_point_content or source_point_content[-1] != player:
            raise ValueError("No puedes mover una ficha que no es tuya.")

        if is_bearing_off:
            if not self.is_ready_to_bear_off(player):
                raise ValueError("No puedes retirar fichas hasta que todas estén en tu home board.")
            
            move_distance = abs(to_point - from_point)
            if move_distance not in dice_roll:
                raise ValueError(f"La distancia del movimiento ({move_distance}) no coincide con la tirada ({dice_roll}).")

            self.get_point(from_point).pop()
            self.__borne_off__[player.get_color()] += 1
        else:
            move_distance = to_point - from_point
            if player.get_color() == "W" and move_distance < 0:
                raise ValueError("El jugador blanco solo puede mover hacia adelante.")
            if player.get_color() == "B" and move_distance > 0:
                raise ValueError("El jugador negro solo puede mover hacia adelante.")

            if abs(move_distance) not in dice_roll:
                raise ValueError(f"La distancia del movimiento no coincide con la tirada.")

            destination_point_content = self.get_point(to_point)
            if destination_point_content and destination_point_content[0] != player:
                if len(destination_point_content) > 1:
                    raise ValueError("No se puede mover a un punto bloqueado.")
                
                # Hit a blot
                opponent_checker = self.get_point(to_point).pop()
                self.__bar__[opponent_checker.get_color()] += 1

            checker = self.get_point(from_point).pop()
            self.place_checker(to_point, checker)

    def move_checker_from_bar(self, player: Player, to_point: int, dice_roll: List[int]):
        """
        Mueve una ficha desde la barra al tablero.
        
        Args:
            player (Player): Jugador que reingresa la ficha
            to_point (int): Punto de destino
            dice_roll (List[int]): Valores disponibles de dados
            
        Raises:
            ValueError: Si el movimiento es inválido
        """
        if self.__bar__[player.get_color()] == 0:
            raise ValueError("No tienes fichas en la barra.")

        # La tirada de dado corresponde al índice del punto
        required_roll = to_point + 1 if player.get_color() == "W" else 24 - to_point
        
        if required_roll not in dice_roll:
            raise ValueError("La tirada no permite reingresar a ese punto.")

        destination_point_content = self.get_point(to_point)
        if destination_point_content and destination_point_content[0] != player:
            if len(destination_point_content) > 1:
                raise ValueError("No se puede reingresar a un punto bloqueado.")
            
            # Hit a blot
            opponent_checker = self.get_point(to_point).pop()
            self.__bar__[opponent_checker.get_color()] += 1

        self.__bar__[player.get_color()] -= 1
        self.place_checker(to_point, player)