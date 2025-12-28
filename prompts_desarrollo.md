Este documento registra todos los prompts utilizados con herramientas de IA durante el desarrollo del proyecto Backgammon.

##  Prompt 1: Consulta Inicial del Proyecto

**Modelo:** Claude Sonnet 4.5  
**Herramienta:** claude.ai  

### Prompt Exacto:
```
necesito ayuda para mi proyecto de computacion, estoy haciendo un backgammon.
En este archivo estan las instrucciones.

[Se adjuntó el PDF del proyecto: Backgammon Computacion 2025 (1).pdf]
```



## Prompt 2: Diseño de la Clase Board

**Modelo:** Claude Sonnet 4.5  
**Herramienta:** claude.ai  

### Prompt Exacto:
```
como deberia estructurar la clase Board para representar el tablero de backgammon? 
necesito almacenar 24 puntos, cada uno puede tener fichas de diferentes jugadores. 
tambien necesito la barra y las fichas retiradas
```

### Respuesta de la IA:

```python
class Board:
    def __init__(self):
        # 24 puntos, cada uno es una lista
        self.__points__ = [[] for _ in range(24)]
        
        # Fichas en la barra por color
        self.__bar__ = {"W": 0, "B": 0}
        
        # Fichas retiradas (borne off)
        self.__borne_off__ = {"W": 0, "B": 0}
    
    def get_point(self, index):
        if 0 <= index < 24:
            return self.__points__[index]
        raise IndexError("Índice de punto inválido")
```



## Prompt 3: Validación de Movimientos

**Modelo:** Claude Sonnet 4.5  
**Herramienta:** claude.ai  

### Prompt Exacto:
```
necesito implementar la validacion de movimientos en backgammon. 
las reglas son:
- no puedes mover a un punto con 2 o mas fichas del oponente
- puedes capturar una ficha solitaria
- si tienes fichas en la barra, debes sacarlas primero
- para bear off, todas tus fichas deben estar en tu home board

dame una funcion que valide si un movimiento es valido
```

### Respuesta de la IA:

```python
def is_valid_move(self, player: Player, from_point: int, die_value: int) -> bool:
    # Verificar si hay fichas en la barra
    if self.__bar__[player.get_color()] > 0 and from_point != 25:
        return False
    
    # Validar punto de origen
    if from_point != 25:  # No es desde la barra
        source = self.get_point(from_point)
        if not source or source[-1] != player:
            return False
    
    # Calcular destino
    direction = 1 if player.get_color() == "W" else -1
    to_point = from_point + (die_value * direction)
    
    # Verificar bear off
    if self.is_ready_to_bear_off(player):
        if (player.get_color() == "W" and to_point >= 24) or \
           (player.get_color() == "B" and to_point < 0):
            # Validar overshoot...
            return True
    
    # Validar punto de destino
    if 0 <= to_point < 24:
        dest = self.get_point(to_point)
        # Punto vacío, con mis fichas, o con 1 ficha del oponente
        return not dest or dest[0] == player or len(dest) == 1
    
    return False
```


## Prompt 4: Implementación de Dados con Dobles

**Modelo:** Claude Sonnet 4.5  
**Herramienta:** claude.ai  

### Prompt Exacto:
```
como implemento los dados? en backgammon si sacas dobles (ej: 5-5) 
puedes hacer 4 movimientos. como manejo eso?
```

### Respuesta de la IA:

```python
import random

class Dice:
    def __init__(self):
        self.__values__ = []
    
    def roll(self):
        d1, d2 = random.randint(1, 6), random.randint(1, 6)
        
        # Si es doble, duplicar los valores
        if d1 == d2:
            self.__values__ = [d1, d1, d1, d1]
        else:
            self.__values__ = [d1, d2]
        
        return self.__values__
```



