import pytest
from core.game import BackgammonGame
from core.board import Board
from core.player import Player


def test_game_initialization():
    """Verifica que el juego se inicializa correctamente."""
    game = BackgammonGame()
    assert game.get_board() is not None
    assert isinstance(game.get_board(), Board)
    assert game.get_player1() is not None
    assert isinstance(game.get_player1(), Player)
    assert game.get_player2() is not None
    assert isinstance(game.get_player2(), Player)
    assert game.get_player1().get_color() == "W"
    assert game.get_player2().get_color() == "B"


def test_game_initializes_board_with_checkers():
    """Verifica que el tablero no está vacío después de la inicialización."""
    game = BackgammonGame()
    board = game.get_board()
    total_checkers = sum(len(point) for point in board._points)
    assert total_checkers == 30


def test_game_roll_dice():
    """Verifica que la tirada de dados funciona y devuelve una lista."""
    game = BackgammonGame()
    dice_roll = game.roll_dice()
    assert isinstance(dice_roll, list)
    assert len(dice_roll) in [2, 4]  # Puede ser 2 o 4 (en caso de dobles)


def test_turn_management():
    """Verifica que la gestión de turnos funciona correctamente."""
    game = BackgammonGame()
    p1 = game.get_player1()
    p2 = game.get_player2()

    assert game.current_player == p1
    game.switch_player()
    assert game.current_player == p2
    game.switch_player()
    assert game.current_player == p1


def test_check_winner_no_winner():
    """Verifica que no hay ganador al inicio del juego."""
    game = BackgammonGame()
    assert game.check_winner() is None