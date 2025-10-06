import pytest
from unittest.mock import patch
from core.dice import Dice


def test_roll_values_are_valid():
    """Verifica que los valores de los dados están siempre entre 1 y 6."""
    dice = Dice()
    for _ in range(100):  # Realizar múltiples lanzamientos para mayor seguridad
        values = dice.roll()
        assert all(1 <= v <= 6 for v in values)


@patch('random.randint')
def test_roll_regular_returns_two_values(mock_randint):
    """
    Verifica que una tirada normal (no dobles) devuelve dos valores.
    Forzamos a random.randint a devolver (3, 4).
    """
    mock_randint.side_effect = [3, 4]
    dice = Dice()
    values = dice.roll()
    assert values == [3, 4]
    assert len(values) == 2
    assert mock_randint.call_count == 2


@patch('random.randint')
def test_roll_doubles_returns_four_values(mock_randint):
    """
    Verifica que una tirada de dobles devuelve cuatro valores idénticos.
    Forzamos a random.randint a devolver (5, 5).
    """
    mock_randint.side_effect = [5, 5]
    dice = Dice()
    values = dice.roll()
    assert values == [5, 5, 5, 5]
    assert len(values) == 4
    assert mock_randint.call_count == 2


def test_get_values_returns_last_roll():
    """Verifica que get_values() devuelve el resultado de la última tirada."""
    dice = Dice()
    rolled_values = dice.roll()
    assert dice.get_values() == rolled_values