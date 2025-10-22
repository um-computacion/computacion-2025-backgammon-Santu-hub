from core.game import BackgammonGame
from core.board import BEAR_OFF_B_POINT, BEAR_OFF_W_POINT

def print_board(board):
    """Imprime una representación textual del tablero."""
    for i, point in enumerate(board._points):
        checkers = [player.get_color() for player in point]
        print(f"{i:2d}: {checkers}")
    print(f"Barra (W): {board._bar['W']}")
    print(f"Barra (B): {board._bar['B']}")
    print(f"Fichas fuera (W): {board._borne_off['W']}")
    print(f"Fichas fuera (B): {board._borne_off['B']}")

def main():
    """Función principal para correr el juego en modo CLI."""
    game = BackgammonGame()
    board = game.get_board()

    while True:
        print("\n" + "="*20)
        print_board(board)
        player = game.current_player
        print(f"Turno de: {player.get_name()} ({player.get_color()})")

        dice_roll = game.roll_dice()
        print(f"Tirada: {dice_roll}")
        
        moves_left = dice_roll.copy()
        
        while moves_left:
            try:
                move = input(f"Movimientos restantes: {moves_left} | (de,a), (bar,a), (de,off) o 'pass': ")
                if move.lower() == 'pass':
                    break
                if move.lower() == 'quit':
                    return

                from_point_str, to_point_str = move.split(',')
                from_point_str = from_point_str.strip().lower()

                if from_point_str == 'bar':
                    to_point = int(to_point_str)
                    board.move_checker_from_bar(player, to_point, moves_left)
                    used_roll = to_point + 1 if player.get_color() == "W" else 24 - to_point
                else:
                    from_point = int(from_point_str)
                    if to_point_str.strip().lower() == 'off':
                        to_point = BEAR_OFF_W_POINT if player.get_color() == "W" else BEAR_OFF_B_POINT
                    else:
                        to_point = int(to_point_str)
                    
                    board.move_checker(player, from_point, to_point, moves_left)
                    used_roll = abs(to_point - from_point)
                
                moves_left.remove(used_roll)

                winner = game.check_winner()
                if winner:
                    print(f"\n¡El jugador {winner.get_name()} ha ganado la partida!")
                    return

            except (ValueError, IndexError) as e:
                print(f"Error: Movimiento inválido. {e}")
            except Exception as e:
                print(f"Ha ocurrido un error inesperado: {e}")
        
        game.switch_player()

if __name__ == "__main__":
    main()
