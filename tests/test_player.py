import pytest
from core.player import Player

def test_player_creation():
    player = Player(name="Player 1", color="white")
    assert player.get_name() == "Player 1"
    assert player.get_color() == "white"
    assert player.get_remaining_checkers() == 15

def test_remove_checker():
    player = Player(name="Player 1", color="white")
    player.remove_checker()
    assert player.get_remaining_checkers() == 14

def test_remove_checker_raises_error_when_no_checkers_left():
    player = Player(name="Player 1", color="white")
    for _ in range(15):
        player.remove_checker()
    
    with pytest.raises(ValueError, match="No quedan fichas para remover"):
        player.remove_checker()

def test_add_checker():
    player = Player(name="Player 1", color="white")
    player.remove_checker()
    player.add_checker()
    assert player.get_remaining_checkers() == 15
