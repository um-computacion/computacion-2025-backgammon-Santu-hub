import random

class Dice:
    """
    Simula dos dados de Backgammon.
    """

    def __init__(self):
        self.__values__ = []

    def roll(self):
        """Lanza los dados y guarda el resultado."""
        d1, d2 = random.randint(1, 6), random.randint(1, 6)
        self.__values__ = [d1, d2] * (2 if d1 == d2 else 1)
        return self.__values__

    def get_values(self):
        """Devuelve los valores de la última tirada."""
        return self.__values__
