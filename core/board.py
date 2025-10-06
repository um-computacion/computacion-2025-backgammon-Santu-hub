from typing import List
from core.player import Player


class Board:
    """
    Representa el tablero de Backgammon con 24 puntos.
    Cada punto puede contener fichas de un jugador.
    """

    def __init__(self):
        # 24 puntos, cada uno es una lista de objetos Player
        self.__points__: List[List[Player]] = [[] for _ in range(24)]

    def __setup_initial_checkers__(self, __p1__: Player, __p2__: Player):
        """Configura la posición inicial de las fichas en el tablero."""
        __initial_setup__ = {
            0: (__p1__, 2),
            5: (__p2__, 5),
            7: (__p2__, 3),
            11: (__p1__, 5),
            12: (__p2__, 5),
            16: (__p1__, 3),
            18: (__p1__, 5),
            23: (__p2__, 2),
        }
        for __point__, (__player__, __count__) in __initial_setup__.items():
            for _ in range(__count__):
                self.__place_checker__(__point__, __player__)

    def __get_point__(self, __index__: int) -> List[Player]:
        """Devuelve la lista de jugadores (fichas) en un punto."""
        if 0 <= __index__ < 24:
            return self.__points__[__index__]
        raise IndexError("Índice de punto inválido")

    def __place_checker__(self, __index__: int, __player__: Player):
        """Coloca una ficha de un jugador en un punto del tablero."""
        if 0 <= __index__ < 24:
            self.__points__[__index__].append(__player__)
        else:
            raise IndexError("Índice de punto inválido")
