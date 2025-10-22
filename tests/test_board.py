import pytest
from core.board import Board, BEAR_OFF_B_POINT, BEAR_OFF_W_POINT
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
    assert len(board._points) == 24
    assert all(isinstance(p, list) for p in board._points)


def test_place_checker_adds_player_piece(board_with_players):
    """Verifica que se puede colocar la ficha de un jugador."""
    board, p1, _ = board_with_players
    board.place_checker(0, p1)
    assert board.get_point(0) == [p1]
    assert len(board.get_point(0)) == 1


def test_get_point_invalid_index_raises_error(board_with_players):
    """Verifica que un índice inválido lanza IndexError al obtener un punto."""
    board, _, _ = board_with_players
    with pytest.raises(IndexError, match="Índice de punto inválido"):
        board.get_point(24)
    with pytest.raises(IndexError, match="Índice de punto inválido"):
        board.get_point(-1)


def test_place_checker_invalid_index_raises_error(board_with_players):
    """Verifica que un índice inválido lanza IndexError al colocar una ficha."""
    board, p1, _ = board_with_players
    with pytest.raises(IndexError, match="Índice de punto inválido"):
        board.place_checker(24, p1)
    with pytest.raises(IndexError, match="Índice de punto inválido"):
        board.place_checker(-1, p1)


def test_initial_board_setup(board_with_players):
    """Verifica la configuración inicial de las fichas en el tablero."""
    board, p1, p2 = board_with_players
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


def test_move_checker_valid_move(board_with_players):
    """Verifica que una ficha se mueve de un punto a otro."""
    board, p1, _ = board_with_players
    board.place_checker(0, p1)
    board.move_checker(p1, 0, 5, [5])
    assert len(board.get_point(0)) == 0
    assert len(board.get_point(5)) == 1
    assert board.get_point(5)[0] == p1


def test_move_checker_from_empty_point_raises_error(board_with_players):
    """Verifica que mover desde un punto vacío lanza ValueError."""
    board, p1, _ = board_with_players
    with pytest.raises(ValueError, match="No puedes mover una ficha que no es tuya"):
        board.move_checker(p1, 1, 5, [4])


def test_move_checker_invalid_player(board_with_players):
    """Verifica que un jugador no puede mover la ficha del otro."""
    board, p1, p2 = board_with_players
    board.place_checker(0, p2)
    with pytest.raises(ValueError, match="No puedes mover una ficha que no es tuya"):
        board.move_checker(p1, 0, 5, [5])


def test_move_checker_invalid_dice_roll(board_with_players):
    """Verifica que el movimiento debe coincidir con la tirada."""
    board, p1, _ = board_with_players
    board.place_checker(0, p1)
    with pytest.raises(ValueError, match="no coincide con la tirada"):
        board.move_checker(p1, 0, 5, [1, 2, 3, 4])


def test_is_ready_to_bear_off(board_with_players):
    """Verifica la lógica para determinar si un jugador puede retirar fichas."""
    board, p1, p2 = board_with_players
    
    # P1 no está listo (fichas fuera del home board)
    board.place_checker(10, p1)
    assert not board.is_ready_to_bear_off(p1)

    # P1 está listo (todas las fichas en el home board)
    board.get_point(10).clear()
    board.place_checker(20, p1)
    board.place_checker(22, p1)
    assert board.is_ready_to_bear_off(p1)

    # P2 no está listo
    board.place_checker(10, p2)
    assert not board.is_ready_to_bear_off(p2)

    # P2 está listo
    board.get_point(10).clear()
    board.place_checker(1, p2)
    board.place_checker(4, p2)
    assert board.is_ready_to_bear_off(p2)


def test_bear_off_valid(board_with_players):
    """Verifica que se puede retirar una ficha correctamente."""
    board, p1, _ = board_with_players
    board.place_checker(20, p1)
    
    # Simular que p1 está listo para retirar
    for i in range(18):
        board._points[i] = [p for p in board._points[i] if p != p1]
    
    board.move_checker(p1, 20, BEAR_OFF_W_POINT, [4])
    assert not board.get_point(20)
    assert board._borne_off["W"] == 1


def test_bear_off_not_ready(board_with_players):
    """Verifica que no se puede retirar si no todas las fichas están en casa."""
    board, p1, _ = board_with_players
    board.place_checker(10, p1) # Ficha fuera del home board
    board.place_checker(20, p1)
    with pytest.raises(ValueError, match="No puedes retirar fichas hasta que todas estén en tu home board"):
        board.move_checker(p1, 20, BEAR_OFF_W_POINT, [4])


def test_win_condition(board_with_players):
    """Verifica que la condición de victoria funciona."""
    board, p1, _ = board_with_players
    assert not board.has_won(p1)
    board._borne_off["W"] = 15
    assert board.has_won(p1)


def test_hit_blot(board_with_players):
    """Verifica que se puede golpear una ficha solitaria (blot)."""
    board, p1, p2 = board_with_players
    board.place_checker(0, p1)
    board.place_checker(5, p2)
    board.move_checker(p1, 0, 5, [5])
    assert board.get_point(5) == [p1]
    assert board._bar["B"] == 1


def test_re_enter_from_bar(board_with_players):
    """Verifica que una ficha puede reingresar desde la barra."""
    board, p1, _ = board_with_players
    board._bar["W"] = 1
    board.move_checker_from_bar(p1, 3, [4])
    assert board.get_point(3) == [p1]
    assert board._bar["W"] == 0


def test_move_checker_when_on_bar(board_with_players):
    """Verifica que no se pueden mover fichas si hay alguna en la barra."""
    board, p1, _ = board_with_players
    board.place_checker(10, p1)
    board._bar["W"] = 1
    with pytest.raises(ValueError, match="Debes reingresar tus fichas desde la barra primero"):
        board.move_checker(p1, 10, 15, [5])
