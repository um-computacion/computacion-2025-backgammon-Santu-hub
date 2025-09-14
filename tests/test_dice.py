from core.dice import Dice
import random

def test_roll_values_between_1_and_6():
    dice = Dice()
    values = dice.roll()
    for v in values:
        assert 1 <= v <= 6

import random

def test_doubles_generate_four_values():
    random.seed(1)  # fuerza un valor predecible
    dice = Dice()
    values = dice.roll()
    if values[0] == values[1]:  # si salió doble
        assert len(values) == 4
    else:
        assert len(values) == 2
