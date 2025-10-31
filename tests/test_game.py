import pytest
from unittest.mock import patch
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

    p1_checkers = sum(
        len(p) for p in board.get_all_points() if p and p[0].get_color() == "W"
    )
    p2_checkers = sum(
        len(p) for p in board.get_all_points() if p and p[0].get_color() == "B"
    )

    assert p1_checkers == 15
    assert p2_checkers == 15


@patch('core.dice.Dice.roll')
def test_game_roll_dice(mock_roll):
    """Verifica que la tirada de dados funciona y actualiza los movimientos."""
    mock_roll.return_value = [3, 4]
    game = BackgammonGame()

    dice_roll = game.roll_dice()
    assert dice_roll == [3, 4]
    assert game.get_remaining_moves() == [3, 4]


def test_turn_management():
    """Verifica que la gestión de turnos funciona correctamente."""
    game = BackgammonGame()
    p1 = game.get_player1()
    p2 = game.get_player2()

    assert game.get_current_player() == p1
    game.switch_player()
    assert game.get_current_player() == p2
    game.switch_player()
    assert game.get_current_player() == p1


def test_check_winner_no_winner():
    """Verifica que no hay ganador al inicio del juego."""
    game = BackgammonGame()
    assert game.check_winner() is None


@patch('core.dice.Dice.roll')
def test_get_remaining_moves(mock_roll):
    """Verifica que get_remaining_moves devuelve los movimientos correctos."""
    mock_roll.return_value = [5, 2]
    game = BackgammonGame()
    
    assert game.get_remaining_moves() == []
    dice_roll = game.roll_dice()
    assert game.get_remaining_moves() == dice_roll


def test_start_new_game():
    """Verifica que se pueden establecer nombres de jugadores y reiniciar."""
    game = BackgammonGame()
    game.start_new_game("Alice", "Bob")
    
    assert game.get_player1().get_name() == "Alice"
    assert game.get_player2().get_name() == "Bob"
    assert game.get_current_player() == game.get_player1()


@patch('core.dice.Dice.roll')
def test_make_move_invalid_die(mock_roll):
    """Verifica que no se puede mover con un dado no disponible."""
    mock_roll.return_value = [1, 2]
    game = BackgammonGame()
    game.roll_dice()
    
    result = game.make_move(1, 5)
    assert result is False


@patch('core.dice.Dice.roll')
def test_switch_player_clears_moves(mock_roll):
    """Verifica que cambiar de turno limpia los movimientos."""
    mock_roll.return_value = [1, 1]
    game = BackgammonGame()
    game.roll_dice()
    
    assert len(game.get_remaining_moves()) > 0
    game.switch_player()
    assert game.get_remaining_moves() == []


@patch('core.dice.Dice.roll')
def test_has_valid_moves_at_start(mock_roll):
    """Verifica que hay movimientos válidos al inicio del juego."""
    mock_roll.return_value = [3, 4]
    game = BackgammonGame()
    game.roll_dice()
    
    assert game.has_valid_moves() is True


def test_has_valid_moves_without_dice():
    """Verifica que no hay movimientos válidos sin tirar dados."""
    game = BackgammonGame()
    assert game.has_valid_moves() is False


@patch('core.dice.Dice.roll')
def test_make_valid_move(mock_roll):
    """Verifica que un movimiento válido actualiza el estado."""
    mock_roll.return_value = [3]
    game = BackgammonGame()
    game.roll_dice()

    result = game.make_move(1, 3)

    assert result is True
    assert 3 not in game.get_remaining_moves()

    board = game.get_board()
    assert len(board.get_point(0)) == 1
    assert len(board.get_point(3)) == 1
    assert board.get_point(3)[0] == game.get_player1()


@patch('core.dice.Dice.roll')
def test_make_move_from_bar(mock_roll):
    """Verifica que se puede mover una ficha desde la barra."""
    mock_roll.return_value = [3]
    game = BackgammonGame()
    p1 = game.get_player1()
    p2 = game.get_player2()
    board = game.get_board()

    # Clear board for predictable test
    for i in range(24):
        board.get_all_points()[i].clear()

    # Simulate a checker on the bar for player1
    board.place_checker(0, p1)
    board.place_checker(3, p2)
    board.move_checker(p2, 3, 3)

    game.roll_dice()

    result = game.make_move(25, 3)

    assert result is True
    assert board.get_bar("W") == 0
    assert board.get_point(2)[0] == p1
