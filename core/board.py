from typing import List, Dict
from core.player import Player

BEAR_OFF_W_POINT = 24
BEAR_OFF_B_POINT = -1


class Board:
    """
    Representa el tablero de Backgammon con 24 puntos y la barra.
    """

    def __init__(self):
        # 24 puntos, cada uno es una lista de objetos Player
        self._points: List[List[Player]] = [[] for _ in range(24)]
        self._borne_off: Dict[str, int] = {"W": 0, "B": 0}
        self._bar: Dict[str, int] = {"W": 0, "B": 0}

    def _setup_initial_checkers(self, p1: Player, p2: Player):
        """Configura la posición inicial de las fichas en el tablero."""
        # Limpia el tablero por si se reutiliza
        self._points = [[] for _ in range(24)]
        self._borne_off = {"W": 0, "B": 0}
        self._bar = {"W": 0, "B": 0}

        initial_setup = {
            0: (p1, 2), 5: (p2, 5), 7: (p2, 3), 11: (p1, 5),
            12: (p2, 5), 16: (p1, 3), 18: (p1, 5), 23: (p2, 2),
        }
        for point, (player, count) in initial_setup.items():
            for _ in range(count):
                self.place_checker(point, player)

    def get_point(self, index: int) -> List[Player]:
        """Devuelve la lista de jugadores (fichas) en un punto."""
        if 0 <= index < 24:
            return self._points[index]
        raise IndexError("Índice de punto inválido")

    def place_checker(self, index: int, player: Player):
        """Coloca una ficha de un jugador en un punto del tablero."""
        if 0 <= index < 24:
            self._points[index].append(player)
        else:
            raise IndexError("Índice de punto inválido")

    def is_ready_to_bear_off(self, player: Player) -> bool:
        """Verifica si todas las fichas de un jugador están en su home board."""
        off_home_board_range = range(0, 18) if player.get_color() == "W" else range(6, 24)
        for point_idx in off_home_board_range:
            if player in self._points[point_idx]:
                return False
        return True

    def has_won(self, player: Player) -> bool:
        """Verifica si un jugador ha ganado (ha retirado sus 15 fichas)."""
        return self._borne_off[player.get_color()] == 15

    def move_checker(self, player: Player, from_point: int, to_point: int, dice_roll: List[int]):
        """
        Mueve una ficha de un punto a otro o la retira del tablero, validando el movimiento.
        """
        is_bearing_off = (player.get_color() == "W" and to_point == BEAR_OFF_W_POINT) or \
                         (player.get_color() == "B" and to_point == BEAR_OFF_B_POINT)
        
        if self._bar[player.get_color()] > 0:
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
            self._borne_off[player.get_color()] += 1
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
                self._bar[opponent_checker.get_color()] += 1

            checker = self.get_point(from_point).pop()
            self.place_checker(to_point, checker)

    def move_checker_from_bar(self, player: Player, to_point: int, dice_roll: List[int]):
        """Mueve una ficha desde la barra al tablero."""
        if self._bar[player.get_color()] == 0:
            raise ValueError("No tienes fichas en la barra.")

        # La tirada de dado corresponde al índice del punto - 1
        # Para W, es 1-6 -> 0-5. Para B, es 1-6 -> 23-18
        required_roll = to_point + 1 if player.get_color() == "W" else 24 - to_point
        
        if required_roll not in dice_roll:
            raise ValueError("La tirada no permite reingresar a ese punto.")

        destination_point_content = self.get_point(to_point)
        if destination_point_content and destination_point_content[0] != player:
            if len(destination_point_content) > 1:
                raise ValueError("No se puede reingresar a un punto bloqueado.")
            
            # Hit a blot
            opponent_checker = self.get_point(to_point).pop()
            self._bar[opponent_checker.get_color()] += 1

        self._bar[player.get_color()] -= 1
        self.place_checker(to_point, player)
