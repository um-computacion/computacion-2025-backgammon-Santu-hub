class Board:
    """
    Representa el tablero de Backgammon con 24 puntos.
    Cada punto puede contener fichas de un jugador.
    """

    def __init__(self):
        # 24 puntos inicializados como listas vacías
        self.__points__ = [[] for _ in range(24)]

    def get_point(self, index: int):
        """Devuelve las fichas en un punto del tablero."""
        if 0 <= index < 24:
            return self.__points__[index]
        raise IndexError("Índice de punto inválido")

    def place_checker(self, index: int, checker: str):
        """Coloca una ficha (checker) en un punto del tablero."""
        if 0 <= index < 24:
            self.__points__[index].append(checker)
        else:
            raise IndexError("Índice de punto inválido")
