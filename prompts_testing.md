Este documento registra todos los prompts utilizados con herramientas de IA durante el testing del proyecto Backgammon.

---

## Prompt: Estrategia General de Testing

**Modelo:** Claude Sonnet 4.5  
**Herramienta:** claude.ai  

### Prompt Exacto:
```
necesito hacer tests para mi proyecto de backgammon. 
tengo que alcanzar 90% de cobertura. que estrategia me recomiendas?
que casos debo probar?
```

### Respuesta de la IA:

La IA recomendó una estrategia en pirámide:

```
        /\
       /UI\       ← No testear (manual)
      /----\
     /Game \      ← Tests de integración ligera
    /------\
   / Board  \     ← Mayor cantidad (lógica compleja)
  /----------\
 /Dice|Player\    ← Tests simples (componentes básicos)
```



## Prompt: Tests para Board - Casos Básicos

**Modelo:** Claude Sonnet 4.5  
**Herramienta:** claude.ai  

### Prompt Exacto:
```
dame ejemplos de tests para la clase Board. 
necesito probar la inicializacion, colocacion de fichas, y movimientos basicos
```

### Respuesta de la IA:

```python
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

def test_place_checker(board_with_players):
    """Verifica que se puede colocar una ficha."""
    board, p1, _ = board_with_players
    board.place_checker(0, p1)
    assert board.get_point(0) == [p1]

def test_initial_setup(board_with_players):
    """Verifica la configuración inicial."""
    board, p1, p2 = board_with_players
    board.setup_initial_checkers(p1, p2)
    
    # Verificar puntos específicos
    assert len(board.get_point(0)) == 2
    assert board.get_point(0)[0] == p1
    
    # Verificar total
    total = sum(len(p) for p in board.get_all_points())
    assert total == 30
```


## Prompt: Testing de Bear Off (Casos Complejos)

**Modelo:** Claude Sonnet 4.5  
**Herramienta:** claude.ai  

### Prompt Exacto:
```
el bear off en backgammon tiene una regla compleja:
- puedes usar un dado mayor para sacar una ficha si no hay fichas mas atras
- pero no puedes si HAY fichas mas atras

como testeo esto? dame ejemplos de tests
```

### Respuesta de la IA:

```python
def test_bear_off_overshoot_valid(board_with_players):
    """Verifica que se puede retirar con dado mayor si no hay fichas detrás."""
    board, p1, _ = board_with_players
    
    # Colocar todas las fichas en punto 20 (home board de W)
    for _ in range(15):
        board.place_checker(20, p1)
    
    # Dado 6, debería poder sacar desde punto 20
    assert board.is_valid_move(p1, 20, 6) is True
    board.move_checker(p1, 20, 6)
    assert board.get_borne_off("W") == 1

def test_bear_off_overshoot_invalid(board_with_players):
    """Verifica que NO se puede retirar con dado mayor si hay fichas detrás."""
    board, p1, _ = board_with_players
    
    # Limpiar tablero
    for i in range(24):
        board.get_all_points()[i].clear()
    
    # Poner 14 fichas en punto 22 y 1 en punto 20
    for _ in range(14):
        board.place_checker(22, p1)
    board.place_checker(20, p1)
    
    # Desde punto 20 con dado 5: NO válido (hay fichas en 22)
    assert board.is_valid_move(p1, 20, 5) is False
    
    # Desde punto 22 con dado 5: SÍ válido (no hay nada más atrás)
    assert board.is_valid_move(p1, 22, 5) is True
```


## Prompt: Mocking para Dice

**Modelo:** Claude Sonnet 4.5  
**Herramienta:** claude.ai  

### Prompt Exacto:
```
como testeo la clase Dice si es aleatoria? 
necesito probar que los dobles devuelven 4 valores
```

### Respuesta de la IA:

```python
from unittest.mock import patch
import pytest
from core.dice import Dice

@patch('random.randint')
def test_roll_regular_returns_two_values(mock_randint):
    """Verifica tirada normal."""
    mock_randint.side_effect = [3, 4]  # Forzar valores
    dice = Dice()
    values = dice.roll()
    
    assert values == [3, 4]
    assert len(values) == 2
    assert mock_randint.call_count == 2

@patch('random.randint')
def test_roll_doubles_returns_four_values(mock_randint):
    """Verifica tirada de dobles."""
    mock_randint.side_effect = [5, 5]  # Forzar dobles
    dice = Dice()
    values = dice.roll()
    
    assert values == [5, 5, 5, 5]
    assert len(values) == 4
```


## Prompt : Tests de Excepciones

**Modelo:** Claude Sonnet 4.5  
**Herramienta:** claude.ai  

### Prompt Exacto:
```
como testeo que se lanzan las excepciones correctas?
por ejemplo cuando intento mover a un punto bloqueado
```

### Respuesta de la IA:

```python
def test_move_checker_blocked_raises_error(board_with_players):
    """Verifica que mover a punto bloqueado lanza ValueError."""
    board, p1, p2 = board_with_players
    
    # Setup: p1 en punto 0, p2 bloquea punto 5 (2+ fichas)
    board.place_checker(0, p1)
    board.place_checker(5, p2)
    board.place_checker(5, p2)
    
    # Intentar mover debería lanzar ValueError
    with pytest.raises(ValueError, match="Movimiento inválido"):
        board.move_checker(p1, 0, 5)

def test_get_point_invalid_index_raises_error(board_with_players):
    """Verifica que índice inválido lanza IndexError."""
    board, _, _ = board_with_players
    
    with pytest.raises(IndexError, match="Índice de punto inválido"):
        board.get_point(24)  # Fuera de rango
```


## Prompt : Tests de Integración (Game)

**Modelo:** Claude Sonnet 4.5  
**Herramienta:** claude.ai  

### Prompt Exacto:
```
necesito tests para la clase Game. 
no es logica compleja pero necesito probar que coordina bien
los otros componentes
```

### Respuesta de la IA:

```python
def test_game_initialization():
    """Verifica inicialización correcta."""
    game = BackgammonGame()
    
    assert game.get_board() is not None
    assert game.get_player1() is not None
    assert game.get_player2() is not None
    assert game.get_player1().get_color() == "W"
    assert game.get_player2().get_color() == "B"

def test_turn_management():
    """Verifica cambio de turnos."""
    game = BackgammonGame()
    p1 = game.get_player1()
    p2 = game.get_player2()
    
    assert game.get_current_player() == p1
    game.switch_player()
    assert game.get_current_player() == p2

def test_switch_player_clears_moves():
    """Verifica que cambiar turno limpia movimientos."""
    game = BackgammonGame()
    game.roll_dice()
    
    assert len(game.get_remaining_moves()) > 0
    game.switch_player()
    assert game.get_remaining_moves() == []
```


## Prompt : Tests para has_valid_moves()

**Modelo:** Claude Sonnet 4.5  
**Herramienta:** claude.ai  

### Prompt Exacto:
```
como testeo el metodo has_valid_moves() de Game?
es un metodo complejo que verifica si hay movimientos posibles
```

### Respuesta de la IA:

```python
def test_has_valid_moves_at_start():
    """Al inicio siempre hay movimientos válidos."""
    game = BackgammonGame()
    game.roll_dice()
    
    # Con configuración inicial y dados, siempre hay movimientos
    assert game.has_valid_moves() is True

def test_has_valid_moves_without_dice():
    """Sin dados, no hay movimientos."""
    game = BackgammonGame()
    # No tirar dados
    
    assert game.has_valid_moves() is False

def test_has_valid_moves_blocked():
    """Verificar caso donde todos los movimientos están bloqueados."""
    game = BackgammonGame()
    board = game.get_board()
    
    # Setup específico donde no hay movimientos válidos
    # ... configurar tablero ...
    
    game.roll_dice()
    assert game.has_valid_moves() is False
```
---
