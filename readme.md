# Backgammon - Proyecto Computación 2025

Implementación completa del juego de Backgammon en Python con interfaz CLI y Pygame, desarrollado como proyecto final para la materia Computación 2025.

Alumno: Santiago Barredo

## 📋 Descripción

Este proyecto implementa todas las reglas oficiales del Backgammon, incluyendo:
- Movimientos estándar y validaciones
- Capturas de fichas (blots)
- Reingresos desde la barra
- Bear off (retirada de fichas)
- Detección automática de ganador
- Dobles (4 movimientos)

## 🎯 Características

- ✅ **Lógica completa de Backgammon** siguiendo reglas oficiales
- ✅ **Interfaz CLI** para jugar en terminal
- ✅ **Interfaz gráfica con Pygame** con visualización completa
- ✅ **Tests unitarios** con >90% de cobertura
- ✅ **Arquitectura modular** con separación core/UI
- ✅ **Principios SOLID** aplicados
- ✅ **Código documentado** con docstrings completos

## 📁 Estructura del Proyecto

```
backgammon/
├── cli/                    # Interfaz de línea de comando
│   ├── __init__.py
│   └── main.py            # Punto de entrada CLI
├── core/                   # Lógica del juego (independiente de UI)
│   ├── __init__.py
│   ├── board.py           # Tablero y validaciones
│   ├── dice.py            # Dados
│   ├── game.py            # Coordinador del juego
│   └── player.py          # Jugador
├── pygame_ui/             # Interfaz gráfica
│   ├── __init__.py
│   └── main.py            # Punto de entrada Pygame
├── tests/                 # Tests unitarios
│   ├── __init__.py
│   ├── test_board.py
│   ├── test_dice.py
│   ├── test_game.py
│   └── test_player.py
├── entorno_virtual/       # Entorno virtual de Python
├── .gitignore
├── CHANGELOG.md           # Historial de cambios
├── JUSTIFICACION.md       # Justificación de diseño
├── README.md              # Este archivo
├── requirements.txt       # Dependencias del proyecto
├── prompts-desarrollo.md  # Prompts de IA usados (desarrollo)
├── prompts-testing.md     # Prompts de IA usados (testing)
└── prompts-documentacion.md  # Prompts de IA usados (docs)
```

## 🚀 Instalación

### Requisitos Previos

- Python 3.10 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio:**
```bash
git clone <https://github.com/um-computacion/computacion-2025-backgammon-Santu-hub.git>
cd backgammon
```

2. **Crear y activar entorno virtual:**

**En Linux/Mac:**
```bash
python3 -m venv entorno_virtual
source entorno_virtual/bin/activate
```

**En Windows:**
```bash
python -m venv entorno_virtual
entorno_virtual\Scripts\activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

## 🎮 Cómo Jugar

### Modo CLI (Línea de Comando)

```bash
python -m cli.main
```

#### Comandos Disponibles:

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `(origen,destino)` | Mover ficha normal | `0,5` |
| `(bar,destino)` | Reingresar desde barra | `bar,3` |
| `(origen,off)` | Retirar ficha | `18,off` |
| `pass` | Pasar turno | - |
| `quit` | Salir del juego | - |

#### Tabla de Referencia - Reingreso desde Barra:

**Jugador Blanco (W):**
- Dado 1 → `bar,0`
- Dado 2 → `bar,1`
- Dado 3 → `bar,2`
- Dado 4 → `bar,3`
- Dado 5 → `bar,4`
- Dado 6 → `bar,5`

**Jugador Negro (B):**
- Dado 1 → `bar,23`
- Dado 2 → `bar,22`
- Dado 3 → `bar,21`
- Dado 4 → `bar,20`
- Dado 5 → `bar,19`
- Dado 6 → `bar,18`

### Modo Pygame (Interfaz Gráfica)

```bash
python -m pygame_ui.interfaz
```

#### Controles:

| Tecla/Acción | Función |
|--------------|---------|
| `ESPACIO` | Tirar los dados |
| `Click izquierdo` | Seleccionar ficha origen |
| `Click izquierdo` | Seleccionar punto destino |
| `P` | Pasar turno |
| `ESC` o `Q` | Salir del juego |

#### Flujo del Juego:

1. Al iniciar, ingresa los nombres de ambos jugadores
2. Presiona `ESPACIO` para tirar los dados
3. Haz clic en una ficha tuya (se resaltará)
4. Haz clic en el punto de destino
5. Repite hasta usar todos los dados
6. El turno cambia automáticamente cuando no quedan movimientos

#### Características Visuales:

- 🎨 Tablero con triángulos en colores alternados
- ⚪ Fichas blancas y negras claramente diferenciadas
- 🎲 Dados visuales con puntos
- 📊 Indicadores de barra y fichas fuera
- ⚠️ Mensajes de error y estado en pantalla
- ✨ Detección automática de movimientos válidos/inválidos

## 🧪 Testing

### Ejecutar Todos los Tests

```bash
pytest
```

### Tests con Cobertura

```bash
pytest --cov=core --cov-report=html --cov-report=term
```

### Ver Reporte HTML de Cobertura

```bash
# Linux/Mac
open htmlcov/index.html

# Windows
start htmlcov/index.html
```

### Ejecutar Tests Específicos

```bash
# Solo tests de Board
pytest tests/test_board.py

# Solo tests de Game
pytest tests/test_game.py

# Solo tests de Dice
pytest tests/test_dice.py

# Solo tests de Player
pytest tests/test_player.py
```


## 🏗️ Arquitectura

### Principios de Diseño

El proyecto sigue una arquitectura de **3 capas**:

```
┌─────────────────────────────────────┐
│     UI Layer (CLI / Pygame)         │  ← Presentación
├─────────────────────────────────────┤
│     Game Layer (BackgammonGame)     │  ← Coordinación
├─────────────────────────────────────┤
│  Logic Layer (Board, Dice, Player)  │  ← Reglas del juego
└─────────────────────────────────────┘
```

## 🔧 Tecnologías Utilizadas

- **Python 3.10+:** Lenguaje principal
- **Pygame 2.5.2:** Interfaz gráfica
- **Pytest 7.4.3:** Framework de testing
- **Pytest-cov 4.1.0:** Medición de cobertura de tests

## 📝 Reglas del Backgammon

### Objetivo

Ser el primero en retirar todas tus 15 fichas del tablero.

### Reglas Básicas

1. **Movimiento:**
   - Blancas (W) mueven de 0 → 23
   - Negras (B) mueven de 23 → 0

2. **Dados:**
   - Cada turno tiras 2 dados
   - Si sacas dobles (ej: 5-5), juegas 4 veces ese número

3. **Capturas:**
   - Si hay una ficha solitaria del oponente, puedes capturarla
   - La ficha capturada va a la barra

4. **Reingreso desde Barra:**
   - DEBES reingresar todas tus fichas antes de mover otras
   - Reingresas en el home board del oponente

5. **Bear Off (Retirar Fichas):**
   - Solo puedes retirar cuando TODAS tus fichas están en tu home board
   - Home board blancas: puntos 18-23
   - Home board negras: puntos 0-5

6. **Victoria:**
   - Ganas cuando retiras tus 15 fichas


**¡Disfruta jugando Backgammon!** 🎲
