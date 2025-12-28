from core.game import BackgammonGame
from core.board import BEAR_OFF_B_POINT, BEAR_OFF_W_POINT


def print_board(board):
    """
    Imprime una representación textual del tablero.
    
    Args:
        board (Board): Tablero de juego a mostrar
    """
    points = board.get_all_points()
    for i, point in enumerate(points):
        checkers = [player.get_color() for player in point]
        print(f"{i:2d}: {checkers}")
    
    print(f"Barra (W): {board.get_bar('W')}")
    print(f"Barra (B): {board.get_bar('B')}")
    print(f"Fichas fuera (W): {board.get_borne_off('W')}")
    print(f"Fichas fuera (B): {board.get_borne_off('B')}")


def main():
    """
    Función principal para correr el juego en modo CLI.
    Gestiona el flujo del juego, recibe inputs del usuario y muestra el estado.
    """
    game = BackgammonGame()
    board = game.get_board()

    print("¡Bienvenido a Backgammon!")

    print("\n" + "="*50)
    print("COMANDOS DISPONIBLES:")
    print("  (origen,destino) - Mover ficha normal (ej: 0,5)")
    print("  (bar,destino)    - Reingresar desde barra")
    print("                     Blanco: bar,0 hasta bar,5")
    print("                     Negro: bar,18 hasta bar,23")
    print("  (origen,off)     - Retirar ficha (ej: 18,off)")
    print("  pass             - Pasar turno")
    print("  quit             - Salir")
    print("="*50 + "\n")

    
    while True:
        print("\n" + "="*50)
        print_board(board)
        
        player = game.get_current_player()
        print(f"\nTurno de: {player.get_name()} ({player.get_color()})")

        dice_roll = game.roll_dice()
        print(f"Tirada: {dice_roll}")
        
        moves_left = dice_roll.copy()
        
        while moves_left:
            try:
                user_input = input(
                    f"Movimientos restantes: {moves_left}\n"
                    f"Ingresa tu movimiento: "
                ).strip()
                
                if user_input.lower() == 'pass':
                    print("Pasando turno...")
                    break
                    
                if user_input.lower() == 'quit':
                    print("¡Gracias por jugar!")
                    return

                from_point_str, to_point_str = user_input.split(',')
                from_point_str = from_point_str.strip().lower()
                to_point_str = to_point_str.strip().lower()

                if from_point_str == 'bar':
                    to_point = int(to_point_str)
                    board.move_checker_from_bar(player, to_point, moves_left)
                    used_roll = to_point + 1 if player.get_color() == "W" else 24 - to_point
                else:
                    from_point = int(from_point_str)
                    
                    if to_point_str == 'off':
                        to_point = BEAR_OFF_W_POINT if player.get_color() == "W" else BEAR_OFF_B_POINT
                    else:
                        to_point = int(to_point_str)
                    
                    board.move_checker(player, from_point, to_point, moves_left)
                    used_roll = abs(to_point - from_point)
                
                moves_left.remove(used_roll)
                print(f"✓ Movimiento realizado. Quedan: {moves_left}")
                print_board(board)
                winner = game.check_winner()
                if winner:
                    print("\n" + "="*50)
                    print(f"🎉 ¡El jugador {winner.get_name()} ({winner.get_color()}) ha ganado la partida!")
                    print_board(board)
                    return

            except (ValueError, IndexError) as e:
                print(f"❌ Error: Movimiento inválido. {e}")
            except Exception as e:
                print(f"❌ Ha ocurrido un error inesperado: {e}")
        
        game.switch_player()


if __name__ == "__main__":
    main()