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
    assert game.get_remaining_moves() == []


def test_game_initializes_board_with_checkers():
    """Verifica que el tablero no está vacío después de la inicialización."""
    game = BackgammonGame()
    board = game.get_board()
    total_checkers = sum(len(point) for point in board.get_all_points())
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

    assert game.get_current_player() == p1
    game.switch_player()
    assert game.get_current_player() == p2
    game.switch_player()
    assert game.get_current_player() == p1


def test_check_winner_no_winner():
    """Verifica que no hay ganador al inicio del juego."""
    game = BackgammonGame()
    assert game.check_winner() is None


def test_get_remaining_moves():
    """Verifica que get_remaining_moves devuelve los movimientos correctos."""
    game = BackgammonGame()
    assert game.get_remaining_moves() == []
    
    dice_roll = game.roll_dice()
    assert game.get_remaining_moves() == dice_roll


def test_set_player_names():
    """Verifica que se pueden establecer nombres de jugadores."""
    game = BackgammonGame()
    game.set_player_names("Alice", "Bob")
    
    assert game.get_player1().get_name() == "Alice"
    assert game.get_player2().get_name() == "Bob"
    assert game.get_current_player() == game.get_player1()


def test_make_move_invalid_die():
    """Verifica que no se puede mover con un dado no disponible."""
    game = BackgammonGame()
    game.roll_dice()
    
    # Intentar mover con un dado que no existe
    result = game.make_move(1, 10)
    assert result is False


def test_switch_player_clears_moves():
    """Verifica que cambiar de turno limpia los movimientos."""
    game = BackgammonGame()
    game.roll_dice()
    
    assert len(game.get_remaining_moves()) > 0
    game.switch_player()
    assert game.get_remaining_moves() == []


def test_has_valid_moves_at_start():
    """Verifica que hay movimientos válidos al inicio del juego."""
    game = BackgammonGame()
    game.roll_dice()
    
    # Al inicio del juego siempre debe haber movimientos válidos
    assert game.has_valid_moves() is True


def test_has_valid_moves_without_dice():
    """Verifica que no hay movimientos válidos sin tirar dados."""
    game = BackgammonGame()
    assert game.has_valid_moves() is False