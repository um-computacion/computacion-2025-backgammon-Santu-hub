import pytest
from core.board import Board
from core.player import Player


@pytest.fixture
def board_with_players():
    """Fixture para crear un tablero con dos jugadores."""
    board = Board()
    player1 = Player("Alice", "W")
    player2 = Player("Bob", "B")
    return board, player1, player2


def test_board_has_24_points(board_with_players):
    """Verifica que el tablero se crea con 24 puntos."""
    board, _, _ = board_with_players
    assert len(board.get_all_points()) == 24


def test_place_checker_adds_player_piece(board_with_players):
    """Verifica que se puede colocar la ficha de un jugador."""
    board, p1, _ = board_with_players
    board.place_checker(0, p1)
    assert board.get_point(0) == [p1]


def test_get_point_invalid_index_raises_error(board_with_players):
    """Verifica que un índice inválido lanza IndexError."""
    board, _, _ = board_with_players
    with pytest.raises(IndexError):
        board.get_point(24)


def test_initial_board_setup(board_with_players):
    """Verifica la configuración inicial de las fichas."""
    board, p1, p2 = board_with_players
    board.setup_initial_checkers(p1, p2)
    assert len(board.get_point(0)) == 2 and board.get_point(0)[0] == p1
    assert len(board.get_point(5)) == 5 and board.get_point(5)[0] == p2
    assert sum(len(p) for p in board.get_all_points()) == 30


def test_is_valid_move_simple(board_with_players):
    """Prueba una validación de movimiento simple."""
    board, p1, p2 = board_with_players
    board.place_checker(0, p1)
    board.place_checker(7, p2)
    assert board.is_valid_move(p1, 0, 5) is True
    assert board.is_valid_move(p1, 0, 7) is True


def test_is_valid_move_blocked(board_with_players):
    """Prueba que no se puede mover a un punto bloqueado."""
    board, p1, p2 = board_with_players
    board.place_checker(0, p1)
    board.place_checker(5, p2)
    board.place_checker(5, p2)
    assert board.is_valid_move(p1, 0, 5) is False


def test_move_checker_valid(board_with_players):
    """Verifica un movimiento válido."""
    board, p1, _ = board_with_players
    board.place_checker(0, p1)
    board.move_checker(p1, 0, 5)
    assert len(board.get_point(0)) == 0
    assert board.get_point(5) == [p1]


def test_move_checker_invalid_raises_error(board_with_players):
    """Verifica que un movimiento inválido lanza ValueError."""
    board, p1, p2 = board_with_players
    board.place_checker(0, p1)
    board.place_checker(5, p2)
    board.place_checker(5, p2)
    with pytest.raises(ValueError, match="Movimiento inválido"):
        board.move_checker(p1, 0, 5)


def test_is_ready_to_bear_off(board_with_players):
    """Verifica la lógica para saber si se puede retirar fichas."""
    board, p1, _ = board_with_players
    for i in range(15):
        board.place_checker(20, p1)
    assert board.is_ready_to_bear_off(p1)


def test_bear_off_valid(board_with_players):
    """Verifica que se puede retirar una ficha."""
    board, p1, _ = board_with_players
    for _ in range(15):
        board.place_checker(20, p1)

    board.move_checker(p1, 20, 4)
    assert len(board.get_point(20)) == 14
    assert board.get_borne_off("W") == 1


def test_bear_off_overshoot_valid(board_with_players):
    """Verifica que se puede retirar con un dado mayor si no hay fichas detrás."""
    board, p1, _ = board_with_players
    for _ in range(15):
        board.place_checker(20, p1)

    assert board.is_valid_move(p1, 20, 6) is True
    board.move_checker(p1, 20, 6)
    assert board.get_borne_off("W") == 1


def test_bear_off_overshoot_invalid(board_with_players):
    """Verifica que no se puede retirar con dado mayor si hay fichas detrás."""
    board, p1, _ = board_with_players
    # Clear board and set up for bear off
    for i in range(24):
        board.get_all_points()[i].clear()

    for _ in range(14):
        board.place_checker(22, p1)
    board.place_checker(20, p1)

    assert board.is_ready_to_bear_off(p1)
    assert board.is_valid_move(p1, 20, 5) is False


def test_has_won(board_with_players):
    """Verifica la condición de victoria."""
    board, p1, _ = board_with_players
    # Clear board and set up for bear off
    for i in range(24):
        board.get_all_points()[i].clear()
    
    for _ in range(15):
        board.place_checker(20, p1)
    
    for _ in range(15):
        board.move_checker(p1, 20, 4)
    assert board.has_won(p1)


def test_hit_blot(board_with_players):
    """Verifica que se puede golpear una ficha solitaria."""
    board, p1, p2 = board_with_players
    board.place_checker(0, p1)
    board.place_checker(5, p2)
    board.move_checker(p1, 0, 5)
    assert board.get_point(5) == [p1]
    assert board.get_bar("B") == 1


def test_move_from_bar_valid(board_with_players):
    """Verifica que se puede reingresar desde la barra."""
    board, p1, p2 = board_with_players
    board.place_checker(0, p1)
    board.place_checker(3, p2)
    board.move_checker(p2, 3, 3)
    
    assert board.get_bar("W") == 1
    board.move_checker_from_bar(p1, 4)
    assert board.get_point(3) == [p1]
    assert board.get_bar("W") == 0


def test_move_from_bar_invalid(board_with_players):
    """Verifica que no se puede mover desde la barra a un punto bloqueado."""
    board, p1, p2 = board_with_players
    board.place_checker(0, p1)
    board.place_checker(3, p2)
    board.move_checker(p2, 3, 3)
    
    board.place_checker(3, p2)
    board.place_checker(3, p2)
    with pytest.raises(ValueError):
        board.move_checker_from_bar(p1, 4)


def test_is_valid_move_from_bar(board_with_players):
    """Verifica la validación de movimientos desde la barra."""
    board, p1, p2 = board_with_players
    board.place_checker(0, p1)
    board.place_checker(3, p2)
    board.move_checker(p2, 3, 3)
    
    board.place_checker(3, p2)
    board.place_checker(3, p2)
    assert board.is_valid_move(p1, 25, 4) is False
    assert board.is_valid_move(p1, 25, 2) is True
