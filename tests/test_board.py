from core.board import Board

def test_board_has_24_points():
    board = Board()
    assert len(board._Board__points__) == 24

def test_place_checker_adds_piece():
    board = Board()
    board.place_checker(0, "X")
    assert board.get_point(0) == ["X"]

def test_invalid_index_raises_error():
    board = Board()
    try:
        board.get_point(25)
        assert False  # no debería llegar acá
    except IndexError:
        assert True
