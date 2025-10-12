from typing import List
from core.player import Player


class Board:
    """
    Representa el tablero de Backgammon con 24 puntos.
    Cada punto puede contener fichas de un jugador.
    """

    def __init__(self):
        # 24 puntos, cada uno es una lista de objetos Player
        self._points: List[List[Player]] = [[] for _ in range(24)]

    def _setup_initial_checkers(self, p1: Player, p2: Player):
        """Configura la posición inicial de las fichas en el tablero."""
        initial_setup = {
            0: (p1, 2),
            5: (p2, 5),
            7: (p2, 3),
            11: (p1, 5),
            12: (p2, 5),
            16: (p1, 3),
            18: (p1, 5),
            23: (p2, 2),
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

    def move_checker(self, from_point: int, to_point: int):
        """Mueve una ficha de un punto a otro."""
        if not self.get_point(from_point):
            raise ValueError(f"No hay fichas en el punto {from_point}")

        player = self.get_point(from_point).pop()
        self.place_checker(to_point, player)
