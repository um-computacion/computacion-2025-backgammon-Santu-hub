class Player:
    """
    Representa a un jugador de Backgammon.
    """

    def __init__(self, name: str, color: str):
        self.__name__ = name
        self.__color__ = color
        self.__checkers__ = 15  # cada jugador arranca con 15 fichas

    def get_name(self):
        return self.__name__

    def get_color(self):
        return self.__color__

    def get_remaining_checkers(self):
        return self.__checkers__

    def remove_checker(self):
        """Quita una ficha del jugador (cuando la mueve al tablero)."""
        if self.__checkers__ > 0:
            self.__checkers__ -= 1
        else:
            raise ValueError("No quedan fichas para remover")

    def add_checker(self):
        """Agrega una ficha al jugador (cuando reingresa o recupera)."""
        self.__checkers__ += 1
