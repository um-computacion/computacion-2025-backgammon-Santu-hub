import pytest
from core.board import Board
from core.player import Player


def test_board_has_24_points():
    """Verifica que el tablero se crea con 24 puntos."""
    board = Board()
    assert len(board._points) == 24
    assert all(isinstance(p, list) for p in board._points)


def test_place_checker_adds_player_piece():
    """Verifica que se puede colocar la ficha de un jugador."""
    board = Board()
    player1 = Player("Alice", "W")
    board.place_checker(0, player1)
    assert board.get_point(0) == [player1]
    assert len(board.get_point(0)) == 1


def test_get_point_invalid_index_raises_error():
    """Verifica que un índice inválido lanza IndexError al obtener un punto."""
    board = Board()
    with pytest.raises(IndexError, match="Índice de punto inválido"):
        board.get_point(24)
    with pytest.raises(IndexError, match="Índice de punto inválido"):
        board.get_point(-1)


def test_place_checker_invalid_index_raises_error():
    """Verifica que un índice inválido lanza IndexError al colocar una ficha."""
    board = Board()
    player1 = Player("Alice", "W")
    with pytest.raises(IndexError, match="Índice de punto inválido"):
        board.place_checker(24, player1)
    with pytest.raises(IndexError, match="Índice de punto inválido"):
        board.place_checker(-1, player1)


def test_initial_board_setup():
    """Verifica la configuración inicial de las fichas en el tablero."""
    board = Board()
    p1 = Player("P1", "W")
    p2 = Player("P2", "B")
    board._setup_initial_checkers(p1, p2)

    # Verificaciones de cantidad de fichas por punto
    assert len(board.get_point(0)) == 2
    assert len(board.get_point(5)) == 5
    assert len(board.get_point(7)) == 3
    assert len(board.get_point(11)) == 5
    assert len(board.get_point(12)) == 5
    assert len(board.get_point(16)) == 3
    assert len(board.get_point(18)) == 5
    assert len(board.get_point(23)) == 2

    # Verificaciones de pertenencia de fichas
    assert all(p == p1 for p in board.get_point(0))
    assert all(p == p2 for p in board.get_point(5))
    assert all(p == p1 for p in board.get_point(18))
    assert all(p == p2 for p in board.get_point(23))

    # Verificar que el total de fichas en el tablero es correcto
    total_checkers_on_board = sum(len(p) for p in board._points)
    assert total_checkers_on_board == 30  # 15 por jugador


def test_move_checker_valid_move():
    """Verifica que una ficha se mueve de un punto a otro."""
    board = Board()
    player1 = Player("Alice", "W")
    board.place_checker(0, player1)

    board.move_checker(0, 5)

    assert len(board.get_point(0)) == 0
    assert len(board.get_point(5)) == 1
    assert board.get_point(5)[0] == player1


def test_move_checker_from_empty_point_raises_error():
    """Verifica que mover desde un punto vacío lanza ValueError."""
    board = Board()
    with pytest.raises(ValueError, match="No hay fichas en el punto 1"):
        board.move_checker(1, 5)