from core.game import BackgammonGame

def print_board(board):
    """Imprime una representación textual del tablero."""
    for i, point in enumerate(board._points):
        checkers = [player.get_color() for player in point]
        print(f"{i:2d}: {checkers}")

def main():
    """Función principal para correr el juego en modo CLI."""
    game = BackgammonGame()
    board = game.get_board()

    while True:
        print_board(board)

        try:
            move = input("Introduce tu movimiento (de,a) o 'quit' para salir: ")
            if move.lower() == 'quit':
                break

            from_point_str, to_point_str = move.split(',')
            from_point = int(from_point_str)
            to_point = int(to_point_str)

            board.move_checker(from_point, to_point)

        except (ValueError, IndexError) as e:
            print(f"Error: Movimiento inválido. {e}")
        except Exception as e:
            print(f"Ha ocurrido un error inesperado: {e}")

if __name__ == "__main__":
    main()
