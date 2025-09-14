from core.game import BackgammonGame

def test_game_initializes_board_and_dice():
    game = BackgammonGame()
    assert game.get_board() is not None
    assert isinstance(game.roll_dice(), list)
