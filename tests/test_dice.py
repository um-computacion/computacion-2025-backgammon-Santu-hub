from core.dice import Dice

def test_roll_values_between_1_and_6():
    dice = Dice()
    values = dice.roll()
    for v in values:
        assert 1 <= v <= 6

def test_doubles_generate_four_values():
    dice = Dice()
    dice._Dice__values__ = [3, 3, 3, 3]
    assert len(dice.get_values()) == 4
