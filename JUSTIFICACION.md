# Justificación de Diseño - Backgammon

**Proyecto:** Backgammon en Python  
**Fecha de inicio:** Agosto 2024  
**Última actualización:** Noviembre 2024  
**Commits totales:** ~50  

---

## 1. Resumen del Diseño General

El proyecto implementa el juego de Backgammon siguiendo una arquitectura modular de tres capas bien diferenciadas:

### **Arquitectura de Capas**

1. **Capa de Lógica (core/)**: Contiene toda la lógica del juego completamente independiente de cualquier interfaz de usuario. Esta capa incluye:
   - Gestión del tablero y sus 24 puntos
   - Validación de movimientos según reglas oficiales de Backgammon
   - Manejo de estados especiales (barra, bear off)
   - Detección de condiciones de victoria

2. **Capa de Presentación CLI (cli/)**: Interfaz de línea de comando que permite jugar mediante texto. Esta capa se comunica con el core únicamente a través de métodos públicos, sin acceder a atributos privados.

3. **Capa de Presentación Gráfica (pygame_ui/)**: Interfaz gráfica desarrollada con Pygame que proporciona una experiencia visual completa con:
   - Entrada de nombres de jugadores
   - Visualización gráfica del tablero con triángulos
   - Sistema de clicks para interacción
   - Detección automática de movimientos válidos/inválidos
   - Mensajes visuales de estado

### **Principio de Diseño Fundamental**

La separación estricta entre lógica y presentación permite:
- **Reutilización**: El mismo core funciona para CLI y Pygame sin modificaciones
- **Testabilidad**: La lógica se prueba aisladamente sin dependencias de UI
- **Mantenibilidad**: Cambios en la UI no afectan la lógica del juego
- **Extensibilidad**: Se podrían agregar nuevas interfaces (web, mobile) sin tocar el core

---

## 2. Justificación de las Clases Elegidas

### 2.1. **Player** (core/player.py)

**Responsabilidad:** Representar a un jugador individual del juego.

**Por qué esta clase:**
- Encapsula toda la información relacionada con un jugador (identidad y estado)
- En el paradigma de OOP, los "jugadores" son entidades naturales con identidad propia
- Facilita la extensibilidad futura (estadísticas, nivel de habilidad, AI)
- Permite diferenciar claramente entre las fichas de cada jugador

**Métodos públicos:**
- `get_name()`: Acceso al nombre para identificación en interfaces
- `get_color()`: Fundamental para la lógica del juego (determina dirección de movimiento)
- `get_remaining_checkers()`: Para tracking de estado
- `add_checker()` / `remove_checker()`: Gestión de fichas

### 2.2. **Board** (core/board.py)

**Responsabilidad:** Gestionar el estado completo del tablero y validar todos los movimientos según las reglas de Backgammon.

**Por qué esta clase:**
- El tablero es la estructura de datos central del juego
- Centraliza toda la lógica relacionada con el estado del juego
- Encapsula las reglas complejas de Backgammon (movimientos, capturas, bear off)
- Mantiene alta cohesión: datos y operaciones relacionadas están juntos

**Métodos principales:**

**Configuración:**
- `setup_initial_checkers()`: Configura la posición inicial estándar del Backgammon

**Consulta de estado (getters):**
- `get_point()`: Acceso a un punto específico
- `get_all_points()`: Vista completa del tablero
- `get_bar()`: Estado de la barra para un jugador
- `get_borne_off()`: Fichas retiradas de un jugador

**Validación:**
- `is_valid_move()`: Verifica si un movimiento es legal sin ejecutarlo
- `is_ready_to_bear_off()`: Determina si un jugador puede empezar a retirar fichas
- `has_won()`: Verifica condición de victoria

**Ejecución:**
- `move_checker()`: Ejecuta un movimiento (con validación previa)
- `move_checker_from_bar()`: Caso especial para reingresar desde la barra
- `place_checker()`: Operación básica de colocación

**Decisiones de diseño importantes:**
1. **Toda la validación está en Board**: Porque Board tiene acceso al estado completo y es el único que debe conocer las reglas
2. **Separación de validación y ejecución**: `is_valid_move()` permite consultar sin modificar estado
3. **Métodos específicos por tipo de movimiento**: `move_checker()` vs `move_checker_from_bar()` para claridad

### 2.3. **Dice** (core/dice.py)

**Responsabilidad:** Simular el lanzamiento de dos dados de seis caras y manejar el caso especial de dobles.

**Por qué esta clase:**
- Encapsula la lógica de aleatoriedad (facilita testing con mocking)
- Maneja la regla especial de Backgammon: dobles permiten 4 movimientos
- Sigue el principio de responsabilidad única
- Permite cambiar el comportamiento de los dados sin afectar otras clases

**Implementación clave:**
```python
def roll(self):
    d1, d2 = random.randint(1, 6), random.randint(1, 6)
    self.__values__ = [d1, d2] * (2 if d1 == d2 else 1)
    return self.__values__
```

**Decisión importante:** Duplicar los valores en caso de dobles ([5,5] → [5,5,5,5]) simplifica enormemente la lógica de consumo de movimientos:
- La CLI puede usar `.remove()` directamente sobre la lista
- No hay que llevar contadores adicionales
- Más intuitivo para el código cliente

### 2.4. **BackgammonGame** (core/game.py)

**Responsabilidad:** Orquestar el flujo del juego y coordinar las demás clases (patrón Facade).

**Por qué esta clase:**
- Actúa como punto de entrada único para las interfaces
- Coordina Board, Dice y Players sin exponer detalles internos
- Gestiona el flujo de turnos y la secuencia del juego
- Implementa lógica de alto nivel (has_valid_moves, make_move)

**Atributos:**
- `__board__`: Instancia del tablero
- `__dice__`: Instancia de los dados
- `__player1__`, `__player2__`: Los dos jugadores
- `__current_player__`: Control del turno actual
- `__remaining_moves__`: Tracking de dados disponibles en el turno

**Métodos clave:**

**Gestión de turnos:**
- `get_current_player()`: Consulta quién juega
- `switch_player()`: Cambia turno y limpia movimientos restantes
- `check_winner()`: Delega en Board la verificación de victoria

**Interface de alto nivel:**
- `roll_dice()`: Tira dados y guarda valores
- `get_remaining_moves()`: Consulta dados disponibles
- `make_move()`: API simplificada para movimientos (usada por Pygame)
- `has_valid_moves()`: Determina si el jugador puede mover (para auto-pasar turno)

**Configuración:**
- `set_player_names()`: Permite personalizar nombres (usado por Pygame)


## 3. Justificación de Atributos

### 3.1. **Board**

#### `__points__: List[List[Player]]`
**Por qué esta estructura:**
- Lista de 24 listas representa naturalmente los 24 puntos del tablero

#### `__bar__: Dict[str, int]`
**Por qué diccionario:**
- Acceso directo O(1) por color ("W" o "B")
- Claridad: `self.__bar__["W"]` es más legible que índices numéricos

#### `__borne_off__: Dict[str, int]`
**Por qué diccionario:**
- Mismas razones que `__bar__`
- Representa estado final: cuántas fichas sacó cada jugador
- Esencial para determinar condición de victoria

### 3.2. **Player**

#### `__name__: str`
**Justificación:**
- Identificación humana del jugador
- Necesario para mostrar en interfaces
- Permite personalización de la experiencia

#### `__color__: str`
**Justificación:**
- Atributo crítico para la lógica del juego
- Determina dirección de movimiento (W → adelante, B → atrás)
- Determina home board (W: 18-23, B: 0-5)


#### `__checkers__: int`
**Justificación:**
- Preparado para tracking de estado
- Actualmente no se usa extensivamente porque el tablero trackea la ubicación
- Útil para validaciones futuras o estadísticas
- Representa el "inventario" del jugador

### 3.3. **Dice**

#### `__values__: List[int]`
**Justificación:**
- Almacena resultado de última tirada
- Lista porque en dobles hay 4 valores disponibles
- Permite consultar sin volver a tirar
- Facilita el patrón de consumir movimientos con `.remove()`

### 3.4. **BackgammonGame**

#### `__board__: Board`
**Justificación:**
- Composición: Game "tiene un" Board
- Encapsula el estado del juego
- Game delega operaciones de tablero a Board

#### `__dice__: Dice`
**Justificación:**
- Composición: Game "tiene unos" Dados
- Encapsula la aleatoriedad
- Permite a Game orquestar tiradas

#### `__player1__, __player2__: Player`
**Justificación:**
- Backgammon es siempre de 2 jugadores
- Atributos separados más claro que lista/tupla
- Facilita referencia directa en check_winner()

#### `__current_player__: Player`
**Justificación:**
- Tracking del turno actual
- Evita índices o flags booleanos
- Referencia directa al objeto Player activo

#### `__remaining_moves__: List[int]`
**Justificación:**
- Crítico para el flujo del juego
- Permite consumir dados uno a uno
- Se inicializa en `roll_dice()` y se limpia en `switch_player()`
- Lista mutable que se modifica con `.remove()`

---

## 4. Decisiones de Diseño Relevantes

### 4.1. **Separación Core / UI**

**Decisión:** Lógica del juego completamente independiente de la interfaz.

**Justificación:**
- **Testabilidad**: Se puede probar la lógica sin inicializar Pygame
- **Reutilización**: Un solo core, múltiples interfaces (CLI + Pygame)
- **Mantenibilidad**: Cambios en UI no rompen la lógica
- **Principio de Responsabilidad Única**: Core se enfoca en reglas, UI en presentación

**Evidencia en el código:**
- `core/` no importa nada de `pygame` ni `cli/`
- CLI y Pygame solo llaman métodos públicos de core
- Tests solo importan clases de core

### 4.2. **Validación Centralizada en Board**

**Decisión:** Toda validación de movimientos está en la clase Board.

**Justificación:**
- **Cohesión**: Board tiene el estado completo, debe validar
- **Consistencia**: Una sola fuente de verdad para las reglas
- **Reutilización**: Tanto CLI como Pygame usan las mismas validaciones
- **Mantenibilidad**: Cambio de reglas en un solo lugar

**Implementación:**
```python
def is_valid_move(self, player: Player, from_point: int, die_value: int) -> bool:
    # Validación completa sin modificar estado
    # Permite consultar antes de ejecutar
```

### 4.3. **Estructura de Datos del Tablero**

**Decisión:** Usar `List[List[Player]]` para representar los puntos.

**Justificación:**
- **Simplicidad**: Fácil de entender e implementar
- **Eficiencia**: Acceso O(1) a cualquier punto
- **Naturalidad**: Apilamiento de fichas es naturalmente una lista
- **Python-idiomático**: Las listas son la estructura por defecto

**Trade-offs aceptados:**
- No es type-safe (podría agregar cualquier objeto)
- Solución: Validar en `place_checker()` y confiar en encapsulación

### 4.4. **Manejo de Dobles en Dice**

**Decisión:** Duplicar valores cuando hay dobles: `[5,5] → [5,5,5,5]`

**Justificación:**
- **Simplificación del código cliente**: CLI y Game pueden usar `.remove()` uniformemente
- **Representación intuitiva**: 4 valores = 4 movimientos disponibles
- **Sin casos especiales**: No hay que chequear si es doble en cada iteración

**Implementación:**
```python
self.__values__ = [d1, d2] * (2 if d1 == d2 else 1)
```


### 4.5. **Getters Públicos para Encapsulación**

**Decisión:** Todos los atributos son privados (`__atributo__`) con getters públicos.

**Justificación:**
- **Cumplimiento de requisitos**: Mandatorio en las especificaciones del proyecto
- **Encapsulación**: Control total sobre el acceso a datos
- **Flexibilidad futura**: Podemos cambiar implementación interna sin romper API
- **Validación centralizada**: Si quisiéramos validar accesos, está en un solo lugar

**Patrón aplicado:**
```python
# Atributo privado
self.__points__: List[List[Player]]

# Getter público
def get_all_points(self) -> List[List[Player]]:
    return self.__points__
```

## 5. Excepciones y Manejo de Errores

### 5.1. **Excepciones Utilizadas**

El proyecto usa **excepciones estándar de Python** en lugar de crear excepciones personalizadas:

#### **ValueError**
**Cuándo se usa:**
- Movimientos que violan reglas del juego
- Operaciones inválidas en el estado actual

**Ejemplos:**
```python
raise ValueError("Movimiento inválido.")
raise ValueError("Movimiento desde la barra inválido.")
raise ValueError("No quedan fichas para remover")
```

**Por qué ValueError:**
- Es la excepción semánticamente correcta para "valor inapropiado"
- Los movimientos inválidos son efectivamente "valores incorrectos" de parámetros
- Standard library pattern: ValueError para argumentos incorrectos pero tipo correcto

#### **IndexError**
**Cuándo se usa:**
- Acceso a puntos fuera del rango del tablero (< 0 o >= 24)

**Ejemplo:**
```python
if 0 <= index < 24:
    return self.__points__[index]
raise IndexError("Índice de punto inválido")
```

**Por qué IndexError:**
- Es la excepción correcta para índices fuera de rango
- Consistente con el comportamiento de listas de Python
- Intuitivo para cualquier programador Python



### 5.2. **Mensajes de Error Descriptivos**

Todos los errores tienen mensajes claros:

```python
"Movimiento inválido."  # General
"Movimiento desde la barra inválido."  # Específico de barra
"No quedan fichas para remover"  # Específico de Player
"Índice de punto inválido"  # Específico de acceso
```

**Principio:** El mensaje debe indicar claramente QUÉ falló, no necesariamente POR QUÉ (eso se puede derivar del contexto).


## 6. Estrategia de Testing y Cobertura

### 6.1. **Enfoque General**

**Filosofía:** Test Unitario enfocado en la lógica del core, sin dependencias de UI.

**Estructura:**
```
tests/
├── test_board.py    # Tests del tablero (24 tests)
├── test_dice.py     # Tests de dados (4 tests)
├── test_game.py     # Tests del juego (11 tests)
└── test_player.py   # Tests de jugador (4 tests)
```

### 6.2. **test_board.py - Cobertura del Tablero**

**Qué se probó:**

#### **Inicialización y Estructura**
```python
def test_board_has_24_points()
```
- Verifica que el tablero se crea con exactamente 24 puntos
- Asegura que la estructura base es correcta

#### **Configuración Inicial**
```python
def test_initial_board_setup()
```
- Valida que setup_initial_checkers() coloca 30 fichas total
- Verifica posiciones específicas (punto 0: 2 fichas, punto 5: 5 fichas, etc.)
- Confirma propiedad correcta de fichas por jugador

**Por qué es importante:** La configuración inicial incorrecta invalidaría todo el juego.

#### **Movimientos Básicos**
```python
def test_is_valid_move_simple()
def test_move_checker_valid()
```
- Prueba movimientos normales sin obstáculos
- Verifica que las fichas se mueven correctamente de un punto a otro

#### **Bloqueos**
```python
def test_is_valid_move_blocked()
def test_move_checker_invalid_raises_error()
```
- Verifica que no se puede mover a un punto con 2+ fichas del oponente
- Confirma que se lanza ValueError apropiadamente

**Por qué es crítico:** Regla fundamental de Backgammon.

#### **Capturas (Blots)**
```python
def test_hit_blot()
```
- Verifica que golpear una ficha solitaria la envía a la barra
- Confirma que la ficha capturada se remueve del punto
- Valida que el contador de barra se incrementa

**Escenario:**
```python
board.place_checker(0, p1)      # P1 en punto 0
board.place_checker(5, p2)      # P2 solitaria en punto 5
board.move_checker(p1, 0, 5)    # P1 captura P2
assert board.get_point(5) == [p1]
assert board.get_bar("B") == 1
```

#### **Reingresos desde Barra**
```python
def test_move_from_bar_valid()
def test_move_from_bar_invalid()
def test_is_valid_move_from_bar()
```
- Prueba reingresos exitosos
- Verifica que no se puede reingresar a punto bloqueado
- Valida la lógica de `is_valid_move()` para barra (from_point=25)

**Por qué múltiples tests:**
- Reingreso desde barra es caso especial con lógica diferente
- Debe funcionar tanto validación como ejecución

#### **Bear Off (Retirar Fichas)**
```python
def test_is_ready_to_bear_off()
def test_bear_off_valid()
def test_bear_off_overshoot_valid()
def test_bear_off_overshoot_invalid()
```

**Casos cubiertos:**
1. **Ready check:** Verifica que solo se puede bear off cuando todas las fichas están en home board
2. **Exact roll:** Retirar con dado exacto (punto 20, dado 4 → off)
3. **Overshoot válido:** Retirar con dado mayor si no hay fichas más atrás
4. **Overshoot inválido:** No se puede usar dado mayor si hay fichas más atrás

**Por qué es complejo:**
```python
# Ejemplo: Fichas en puntos 22 y 20, dado 5
# Desde punto 20: NO se puede usar dado 5 (hay ficha en 22 más atrás)
# Desde punto 22: SÍ se puede usar dado 5 (no hay nada más atrás)
```

Esta regla requiere validación especial implementada en `is_valid_move()`.

#### **Condición de Victoria**
```python
def test_has_won()
```
- Simula retirada de 15 fichas
- Verifica que `has_won()` retorna True solo cuando borne_off == 15

#### **Manejo de Errores**
```python
def test_get_point_invalid_index_raises_error()
def test_place_checker_invalid_index_raises_error()
```
- Verifica que índices fuera de rango lanzan IndexError
- Confirma mensajes de error apropiados

### 6.3. **test_dice.py - Cobertura de Dados**

**Qué se probó:**

#### **Valores Válidos**
```python
def test_roll_values_are_valid()
```
- Ejecuta 100 tiradas
- Verifica que TODOS los valores están entre 1 y 6
- Prueba estadística básica de aleatoriedad

#### **Tiradas Normales vs Dobles**
```python
@patch('random.randint')
def test_roll_regular_returns_two_values(mock_randint)
def test_roll_doubles_returns_four_values(mock_randint)
```

**Técnica: Mocking**
- Usa `unittest.mock.patch` para controlar aleatoriedad
- Fuerza valores específicos: (3,4) para normal, (5,5) para dobles
- Verifica comportamiento determinístico

**Por qué mocking:**
- Testing de código aleatorio requiere control
- Evita falsos positivos/negativos por azar
- Prueba lógica exacta (duplicación en dobles)

#### **Persistencia de Valores**
```python
def test_get_values_returns_last_roll()
```
- Verifica que `get_values()` retorna la última tirada
- Confirma que el estado se mantiene entre llamadas

### 6.4. **test_game.py - Cobertura del Juego**

**Qué se probó:**

#### **Inicialización**
```python
def test_game_initialization()
def test_game_initializes_board_with_checkers()
```
- Verifica creación correcta de todos los componentes
- Confirma que Board se inicializa con 30 fichas
- Valida colores correctos de jugadores

#### **Gestión de Turnos**
```python
def test_turn_management()
def test_switch_player_clears_moves()
```
- Verifica alternancia correcta de jugadores
- Confirma que cambiar turno limpia `__remaining_moves__`

**Por qué importante:** Evitar que el siguiente jugador use dados del turno anterior.

#### **Sistema de Dados**
```python
def test_game_roll_dice()
def test_get_remaining_moves()
```
- Verifica que `roll_dice()` retorna lista válida (2 o 4 elementos)
- Confirma que `get_remaining_moves()` sincroniza correctamente

#### **Validación de Movimientos**
```python
def test_make_move_invalid_die()
def test_has_valid_moves_at_start()
def test_has_valid_moves_without_dice()
```
- Verifica que no se puede mover con dado no disponible
- Confirma que al inicio siempre hay movimientos válidos
- Valida que sin tirar dados no hay movimientos

#### **Configuración de Jugadores**
```python
def test_set_player_names()
```
- Verifica que `set_player_names()` funciona correctamente
- Confirma que se reinicia el tablero al cambiar jugadores

#### **Condición de Victoria**
```python
def test_check_winner_no_winner()
```
- Verifica que al inicio no hay ganador
- Previene falsos posit