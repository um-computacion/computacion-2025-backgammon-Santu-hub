import pygame
import sys
from core.game import BackgammonGame
"""constantes""" 
WIDTH, HEIGHT = 1000, 700 
MARGIN = 40 
POINT_WIDTH = 60 
POINT_HEIGHT = 200 
CHECKER_RADIUS = 25 
"""colores""" 
BG = (210, 180, 140) 
BROWN_DARK = (139, 69, 19) 
BROWN_LIGHT = (205, 133, 63) 
WHITE = (255, 255, 255) 
BLACK = (30, 30, 30) 
RED = (220, 20, 60) 

def render_board(screen, game, font):
    """Dibuja el tablero y retorna hitmap para clicks"""
    screen.fill(BG)
    board = game.get_board()
    hitmap = {}
    for visual_idx in range(12):
        board_idx = 11 - visual_idx
        x = MARGIN + visual_idx * POINT_WIDTH
        if visual_idx >= 6:
            x += 40
        y_base = HEIGHT - MARGIN - POINT_HEIGHT
        draw_point(screen, x, y_base, board_idx, board, False, hitmap)
        num_text_bottom = font.render(str(12 - visual_idx), True, BLACK)
        screen.blit(num_text_bottom, (x + POINT_WIDTH//2 - 10, HEIGHT - MARGIN + 5))
    for visual_idx in range(12):
        board_idx = 12 + visual_idx
        x = MARGIN + visual_idx * POINT_WIDTH
        if visual_idx >= 6:
            x += 40
        draw_point(screen, x, MARGIN, board_idx, board, True, hitmap)
        num_text = font.render(str(13 + visual_idx), True, BLACK)
        screen.blit(num_text, (x + POINT_WIDTH//2 - 10, MARGIN - 25))
    bar_x = MARGIN + 6 * POINT_WIDTH
    pygame.draw.rect(screen, BROWN_DARK, (bar_x, MARGIN, 40, HEIGHT - 2*MARGIN))
    white_bar = board.get_bar("W")
    black_bar = board.get_bar("B")
    if white_bar > 0:
        for i in range(white_bar):
            cx = bar_x + 20
            cy = HEIGHT - MARGIN - 30 - i * (CHECKER_RADIUS * 2 + 3)
            pygame.draw.circle(screen, WHITE, (cx, cy), CHECKER_RADIUS)
            pygame.draw.circle(screen, BLACK, (cx, cy), CHECKER_RADIUS, 2)
        hitmap[24] = pygame.Rect(bar_x, HEIGHT // 2, 40, HEIGHT // 2 - MARGIN)
    if black_bar > 0:
        for i in range(black_bar):
            cx = bar_x + 20
            cy = MARGIN + 30 + i * (CHECKER_RADIUS * 2 + 3)
            pygame.draw.circle(screen, BLACK, (cx, cy), CHECKER_RADIUS)
            pygame.draw.circle(screen, WHITE, (cx, cy), CHECKER_RADIUS, 2)
        hitmap[24] = pygame.Rect(bar_x, MARGIN, 40, HEIGHT // 2 - MARGIN)
    bear_off_x = MARGIN + 12 * POINT_WIDTH + 40
    bear_off_width = 100
    pygame.draw.rect(screen, (100, 100, 100), (bear_off_x, HEIGHT // 2, bear_off_width, HEIGHT // 2 - MARGIN), 2)
    bear_off_text = font.render("OFF", True, BLACK)
    screen.blit(bear_off_text, (bear_off_x + 35, HEIGHT - MARGIN - 20))
    white_off = board.get_borne_off("W")
    if white_off > 0:
        off_text = font.render(f"W:{white_off}", True, WHITE)
        screen.blit(off_text, (bear_off_x + 35, HEIGHT // 2 + 10))
    hitmap[25] = pygame.Rect(bear_off_x, HEIGHT // 2, bear_off_width, HEIGHT // 2 - MARGIN)
    pygame.draw.rect(screen, (100, 100, 100), (bear_off_x, MARGIN, bear_off_width, HEIGHT // 2 - MARGIN), 2)
    screen.blit(bear_off_text, (bear_off_x + 35, MARGIN + 5))
    black_off = board.get_borne_off("B")
    if black_off > 0:
        off_text = font.render(f"B:{black_off}", True, BLACK)
        screen.blit(off_text, (bear_off_x + 35, HEIGHT // 2 - 30))
    hitmap[26] = pygame.Rect(bear_off_x, MARGIN, bear_off_width, HEIGHT // 2 - MARGIN)
    draw_info(screen, game, font)
    return hitmap

def draw_point(screen, x, y_base, board_idx, board, is_top, hitmap):
    """Dibuja un triángulo y las fichas"""
    visual_pos = board_idx + 1
    color = BROWN_DARK if ((visual_pos - 1) // 6 + visual_pos) % 2 == 0 else BROWN_LIGHT
    if is_top:
        points = [(x, y_base),
                  (x + POINT_WIDTH, y_base),
                  (x + POINT_WIDTH//2, y_base + POINT_HEIGHT)]
    else:
        points = [(x, y_base + POINT_HEIGHT),
                  (x + POINT_WIDTH, y_base + POINT_HEIGHT),
                  (x + POINT_WIDTH//2, y_base)]
    pygame.draw.polygon(screen, color, points)
    pygame.draw.polygon(screen, BLACK, points, 2)
    hitmap[board_idx] = pygame.Rect(x, y_base if not is_top else y_base, POINT_WIDTH, POINT_HEIGHT)
    point = board.get_point(board_idx)
    if point:
        checker_color = WHITE if point[0].get_color() == "W" else BLACK
        border_color = BLACK if point[0].get_color() == "W" else WHITE
        count = len(point)
        for i in range(count):
            cx = x + POINT_WIDTH // 2
            if is_top:
                cy = y_base + 20 + i * (CHECKER_RADIUS * 2 + 5)
            else:
                cy = y_base + POINT_HEIGHT - 20 - i * (CHECKER_RADIUS * 2 + 5)
            pygame.draw.circle(screen, checker_color, (cx, cy), CHECKER_RADIUS)
            pygame.draw.circle(screen, border_color, (cx, cy), CHECKER_RADIUS, 2)

def draw_info(screen, game, font):
    """Dibuja información del juego en el lado derecho"""
    info_x = MARGIN + 12 * POINT_WIDTH + 150
    small_font = pygame.font.SysFont(None, 18)
    player = game.get_current_player()
    info = f"Turno: {player.get_name()}"
    text = small_font.render(info, True, BLACK)
    screen.blit(text, (info_x, HEIGHT // 2 - 60))
    color_text = f"({player.get_color()})"
    text = small_font.render(color_text, True, BLACK)
    screen.blit(text, (info_x, HEIGHT // 2 - 40))
    moves = game.get_remaining_moves()
    if moves:
        dice_text = f"Dados: {moves}"
        text = small_font.render(dice_text, True, BLACK)
        screen.blit(text, (info_x, HEIGHT // 2 - 15))
        board = game.get_board()
        color = player.get_color()
        if board.get_bar(color) > 0:
            tiny_font = pygame.font.SysFont(None, 16)
            warn1 = tiny_font.render("¡FICHA EN", True, RED)
            warn2 = tiny_font.render("EL BAR!", True, RED)
            warn3 = tiny_font.render("Debes", True, RED)
            warn4 = tiny_font.render("sacarla", True, RED)
            warn5 = tiny_font.render("primero", True, RED)
            screen.blit(warn1, (info_x, HEIGHT // 2 + 15))
            screen.blit(warn2, (info_x, HEIGHT // 2 + 30))
            screen.blit(warn3, (info_x, HEIGHT // 2 + 45))
            screen.blit(warn4, (info_x, HEIGHT // 2 + 60))
            screen.blit(warn5, (info_x, HEIGHT // 2 + 75))
    else:
        text = small_font.render("Presiona", True, RED)
        screen.blit(text, (info_x, HEIGHT // 2 - 10))
        text2 = small_font.render("ESPACIO", True, RED)
        screen.blit(text2, (info_x, HEIGHT // 2 + 5))
        text3 = small_font.render("para tirar", True, RED)
        screen.blit(text3, (info_x, HEIGHT // 2 + 20))

def hit_test(hitmap, pos):
    """Detecta qué punto fue clickeado"""
    for idx, rect in hitmap.items():
        if rect.collidepoint(pos):
            return idx
    return None

def main():
    pygame.init()
    pygame.display.set_caption("Backgammon")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)
    names = []
    for prompt in ["Jugador 1 (Blancas)", "Jugador 2 (Negras)"]:
        name = ""
        entering = True
        while entering:
            screen.fill(BG)
            title_font = pygame.font.SysFont(None, 36)
            title = title_font.render(prompt, True, BLACK)
            screen.blit(title, title.get_rect(center=(WIDTH//2, HEIGHT//2 - 50)))
            name_text = title_font.render(name + "_", True, BLACK)
            screen.blit(name_text, name_text.get_rect(center=(WIDTH//2, HEIGHT//2)))
            instr = font.render("Presiona ENTER para continuar", True, BLACK)
            screen.blit(instr, instr.get_rect(center=(WIDTH//2, HEIGHT//2 + 60)))
            pygame.display.flip()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        entering = False
                    elif e.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif e.unicode.isprintable() and len(name) < 20:
                        name += e.unicode
        names.append(name if name else f"Player {len(names) + 1}")
    game = BackgammonGame()
    game.start_new_game(names[0], names[1])
    hitmap = {}
    selected = None
    no_moves_message = None
    message_timer = 0
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif e.key == pygame.K_SPACE and not game.get_remaining_moves():
                    game.roll_dice()
                    if not game.has_valid_moves():
                        print("Sin movimientos válidos")
                        no_moves_message = "¡Sin movimientos válidos! Pasando turno..."
                        message_timer = 180
                        game.switch_player()
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if game.get_remaining_moves():
                    idx = hit_test(hitmap, e.pos)
                    if idx is not None:
                        from_pos = 25 if idx == 24 else idx + 1
                        if selected is None:
                            selected = from_pos
                            print(f"Origen: {from_pos}" + (" (BAR)" if from_pos == 25 else ""))
                        else:
                            if idx == 24:
                                to_pos = 25
                            elif idx == 25 or idx == 26:
                                to_pos = 0
                            else:
                                to_pos = idx + 1
                            if selected == 25:
                                current_player = game.get_current_player()
                                if current_player.get_color() == "W":
                                    die_value = to_pos
                                else:
                                    die_value = 25 - to_pos
                            elif to_pos == 0:
                                current_player = game.get_current_player()
                                remaining_moves = game.get_remaining_moves()
                                success = False
                                for die_value in remaining_moves:
                                    if game.make_move(selected, die_value):
                                        print(f"Movimiento: {selected} -> OFF (dado {die_value})")
                                        if not game.get_remaining_moves():
                                            game.switch_player()
                                        success = True
                                        break
                                if not success:
                                    print("Movimiento inválido")
                                selected = None
                                continue
                            else:
                                die_value = abs(to_pos - selected)
                            if game.make_move(selected, die_value):
                                dest_text = "OFF" if to_pos == 0 else str(to_pos)
                                print(f"Movimiento: {selected} -> {dest_text} (dado {die_value})")
                                if not game.get_remaining_moves():
                                    game.switch_player()
                            else:
                                print("Movimiento inválido")
                            selected = None
        hitmap = render_board(screen, game, font)
        if message_timer > 0:
            message_timer -= 1
            title_font = pygame.font.SysFont(None, 36)
            text = title_font.render(no_moves_message, True, RED)
            text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
            bg_rect = text_rect.inflate(40, 20)
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
            bg_surface.fill(WHITE)
            bg_surface.set_alpha(220)
            screen.blit(bg_surface, bg_rect)
            screen.blit(text, text_rect)
        winner = game.check_winner()
        if winner:
            title_font = pygame.font.SysFont(None, 48)
            text = title_font.render(f"¡{winner.get_name()} GANÓ!", True, RED)
            screen.blit(text, text.get_rect(center=(WIDTH//2, HEIGHT//2)))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()