# PACKAGES NEEDED:
# pip install pygame

# IMPORTS
import pygame
import socket
import colors
import figure

from random import randint
from math import floor
from board import initialize_board, DefaultFigureCodec
from threading import Thread


# GLOBAL VARS
pygame.init()
pygame.font.init()
DISPLAY_INFO = pygame.display.Info()
SCREEN_W = 1536 # DISPLAY_INFO.current_w*0.8
SCREEN_H = 864 # DISPLAY_INFO.current_h*0.8
SCREEN = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("CHESS")
CLOCK = pygame.time.Clock()
XL_FONT = pygame.font.SysFont("Arial", 64)
L_FONT = pygame.font.SysFont("Arial", 48)
M_FONT = pygame.font.SysFont("Arial", 30)
S_FONT = pygame.font.SysFont("Arial", 18)
FPS = 60
GAME_DEBUG = True
TRANSMISSION_DEBUG = True
LAST_REC_DATA = None
LAST_REC_ADDR = None
CLICKED_TILE = None
POSSIBLE_MOVES = []
MOVE_PLAYED = None
MOVE_REQUESTED = False


# OBJECT CLASSES
# SIMPLE BORDER BUTTON
class Button:
    def __init__(self, pos_x, pos_y, width, height, b_text = "", font_color=colors.WHITE, border_color=colors.WHITE,
                 border=0, border_radius=-1):
        self.x = pos_x
        self.y = pos_y
        self.w = width
        self.h = height
        self.rect = pygame.Rect(pos_x, pos_y, width, height)
        self.b_text = b_text
        self.b_text_len = len(b_text)
        self.font_color = font_color
        self.border_color = border_color
        self.border = border
        self.border_radius = border_radius
        self.clicked = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        pygame.draw.rect(SCREEN, self.border_color, self.rect, self.border, self.border_radius)

        b_text_obj = None
        w_char_s = 0
        center_height_offset = 0

        if self.h < 40:
            b_text_obj = S_FONT.render(self.b_text, True, self.font_color)
            center_height_offset = 11
            w_char_s = 12

        elif self.h < 64:
            b_text_obj = M_FONT.render(self.b_text, True, self.font_color)
            center_height_offset = 18
            w_char_s = 21

        elif self.h < 100:
            b_text_obj = L_FONT.render(self.b_text, True, self.font_color)
            center_height_offset = 29
            w_char_s = 32

        else:
            b_text_obj = XL_FONT.render(self.b_text, True, self.font_color)
            center_height_offset = 40
            w_char_s = 44

        SCREEN.blit(b_text_obj, (self.x + self.w/2 - self.b_text_len*w_char_s/2.66, self.y + self.h/2 -
                                 center_height_offset))
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        return action


# BOARD TILE
class BoardTile:
    def __init__(self, tile_pos, tile_size, tile_color):
        self.pos_x = tile_pos[0]
        self.pox_y = tile_pos[1]
        self.size = tile_size
        self.color = tile_color
        self.rect = pygame.Rect(self.pos_x, self.pox_y, self.size, self.size)
        self.clicked = False

    def draw(self):
        pygame.draw.rect(SCREEN, self.color, self.rect)
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] == 1:
                if not self.clicked:
                    self.clicked = True
                    return False
            else:
                if self.clicked:
                    self.clicked = False
                    return True
                else:
                    return False
        else:
            self.clicked = False
            return False

    def sketch(self):
        pygame.draw.rect(SCREEN, self.color, self.rect)


# FUNCTIONS
# RENDER STRING TO SCREEN
def render_text(screen_text, screen_pos_x, screen_pos_y, size, font_color=colors.WHITE):
    text_obj = None

    if size.lower() == "s":
        text_obj = S_FONT.render(screen_text, True, font_color)
    elif size.lower() == "m":
        text_obj = M_FONT.render(screen_text, True, font_color)
    elif size.lower() == "l":
        text_obj = L_FONT.render(screen_text, True, font_color)
    else:
        text_obj = XL_FONT.render(screen_text, True, font_color)

    SCREEN.blit(text_obj, (screen_pos_x, screen_pos_y))


# THREADING RECEIVE AT SOCKET FROM ENDPOINT
def conn_rec(t_socket):
    global LAST_REC_DATA, LAST_REC_ADDR
    t_data, LAST_REC_ADDR = t_socket.recvfrom(1024)
    LAST_REC_DATA = t_data.decode("utf-8")
    if TRANSMISSION_DEBUG: print(f"In: {LAST_REC_DATA}")


# THREADING SEND FROM SOCKET TO ENDPOINT
def conn_send(t_socket, msg, t_endpoint):
    t_socket.sendto(msg.encode("utf-8"), t_endpoint)
    if TRANSMISSION_DEBUG: print(f"Out: {msg}")


# INIT BOARD
def init_board(board_pos, board_square_size, board_base_color, board_square_color):
    board_tile_matrix = [[None for i in range(8)] for j in range(8)]
    for i in range(len(board_tile_matrix)):
        for j in range(len(board_tile_matrix[i])):
            if (i % 2 == 0) == (j % 2 == 1):
                board_tile_matrix[i][j] = BoardTile((i * board_square_size + board_pos[0], (7 - j) * board_square_size + board_pos[1]), board_square_size, board_base_color)
            else:
                board_tile_matrix[i][j] = BoardTile((i * board_square_size + board_pos[0], (7 - j) * board_square_size + board_pos[1]), board_square_size, board_square_color)
    return board_tile_matrix


# CALC POSSIBLE MOVES
def calc_possible_moves(bm, fp, iw, codec = DefaultFigureCodec):
    clicked_fig = bm[fp[0]][fp[1]]
    pm = []

    # WHITE PAWN
    if clicked_fig == codec.w_p:
        pm += figure.pawn_moves(bm, fp, iw)

    # BLACK PAWN
    elif clicked_fig == codec.b_p:
        pm += figure.pawn_moves(bm, fp, iw)

    # CASTLE
    elif clicked_fig == codec.w_r or clicked_fig == codec.b_r:
        pm += figure.rook_moves(bm, fp, iw)

    # HORSE
    elif clicked_fig == codec.w_kn or clicked_fig == codec.b_kn:
        pm += figure.knight_moves(bm, fp, iw)

    # SNIPER
    elif clicked_fig == codec.w_b or clicked_fig == codec.b_b:
        pm += figure.bishop_moves(bm, fp, iw)

    # KING
    elif clicked_fig == codec.w_k or clicked_fig == codec.b_k:
        pm += figure.king_moves(bm, fp, iw)

    # QUEEN
    elif clicked_fig == codec.w_q or clicked_fig == codec.b_q:
        pm += figure.queen_moves(bm, fp, iw)

    return pm


# DRAW BOARD
def draw_board(board_m, board_tm, board_pos, board_square_size, playing_as_white, move_able = True):
    global CLICKED_TILE, POSSIBLE_MOVES, MOVE_PLAYED
    new_click = None
    for i in range(len(board_tm)):
        for j in range(len(board_tm[i])):
            if playing_as_white:
                if board_tm[i][j].draw():
                    new_click = [i, j]
            else:
                if board_tm[7 - i][7 - j].draw():
                    new_click = [i, j]

            if board_m[i][j] > 0:
                tile_text = L_FONT.render(str(board_m[i][j]), True, colors.BLACK)
                if playing_as_white:
                    SCREEN.blit(tile_text, (i * board_square_size + board_pos[0] + board_square_size * 0.25, (7 - j) * board_square_size + board_pos[1] + board_square_size * 0.2))
                else:
                    SCREEN.blit(tile_text, ((7 - i) * board_square_size + board_pos[0] + board_square_size * 0.25, j * board_square_size + board_pos[1] + board_square_size * 0.2))

    if new_click and move_able:
        if CLICKED_TILE:
            if new_click == CLICKED_TILE:
                CLICKED_TILE = None
                POSSIBLE_MOVES = []
            elif new_click in POSSIBLE_MOVES:
                board_m[new_click[0]][new_click[1]] = board_m[CLICKED_TILE[0]][CLICKED_TILE[1]]
                board_m[CLICKED_TILE[0]][CLICKED_TILE[1]] = 0
                MOVE_PLAYED = [CLICKED_TILE, new_click]
                CLICKED_TILE = None
                POSSIBLE_MOVES = []
            else:
                if playing_as_white and 0 < board_m[new_click[0]][new_click[1]] < 10 or not playing_as_white and 10 < board_m[new_click[0]][new_click[1]]:
                    CLICKED_TILE = new_click
                    POSSIBLE_MOVES = calc_possible_moves(board_m, new_click, playing_as_white)
        else:
            if playing_as_white and 0 < board_m[new_click[0]][new_click[1]] < 10 or not playing_as_white and 10 < board_m[new_click[0]][new_click[1]]:
                CLICKED_TILE = new_click
                POSSIBLE_MOVES = calc_possible_moves(board_m, new_click, playing_as_white)

    if CLICKED_TILE and move_able:
        if playing_as_white:
            BoardTile((CLICKED_TILE[0] * board_square_size + board_pos[0],
                       (7 - CLICKED_TILE[1]) * board_square_size + board_pos[1]), board_square_size, colors.GREEN).sketch()
            tile_text = L_FONT.render(str(board_m[CLICKED_TILE[0]][CLICKED_TILE[1]]), True, colors.BLACK)
            SCREEN.blit(tile_text, (CLICKED_TILE[0] * board_square_size + board_pos[0] + board_square_size * 0.25,
                                    (7 - CLICKED_TILE[1]) * board_square_size + board_pos[1] + board_square_size * 0.2))
        else:
            BoardTile(((7 - CLICKED_TILE[0]) * board_square_size + board_pos[0],
                       CLICKED_TILE[1] * board_square_size + board_pos[1]), board_square_size,
                      colors.GREEN).sketch()
            tile_text = L_FONT.render(str(board_m[CLICKED_TILE[0]][CLICKED_TILE[1]]), True, colors.BLACK)
            SCREEN.blit(tile_text, ((7 - CLICKED_TILE[0]) * board_square_size + board_pos[0] + board_square_size * 0.25,
                                    CLICKED_TILE[1] * board_square_size + board_pos[1] + board_square_size * 0.2))

        for tile in POSSIBLE_MOVES:
            if playing_as_white:
                BoardTile((tile[0] * board_square_size + board_pos[0], (7 - tile[1]) * board_square_size + board_pos[1]), board_square_size, colors.RED).sketch()
                if board_m[tile[0]][tile[1]] > 0:
                    tile_text = L_FONT.render(str(board_m[tile[0]][tile[1]]), True, colors.BLACK)
                    SCREEN.blit(tile_text, (tile[0] * board_square_size + board_pos[0] + board_square_size * 0.25, (7 - tile[1]) * board_square_size + board_pos[1] + board_square_size * 0.2))
            else:
                BoardTile(
                    ((7 - tile[0]) * board_square_size + board_pos[0], tile[1] * board_square_size + board_pos[1]), board_square_size, colors.RED).sketch()
                if board_m[tile[0]][tile[1]] > 0:
                    tile_text = L_FONT.render(str(board_m[tile[0]][tile[1]]), True, colors.BLACK)
                    SCREEN.blit(tile_text, ((7 - tile[0]) * board_square_size + board_pos[0] + board_square_size * 0.25, tile[1] * board_square_size + board_pos[1] + board_square_size * 0.2))


# MAIN LOOP
def main():

    # GLOBAL VARS
    global LAST_REC_DATA, LAST_REC_ADDR, MOVE_PLAYED, MOVE_REQUESTED

    # SOCKET VARS
    local_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    conn_socket = None

    # MAIN VARS
    running = True
    game_phase = 0
    host_mode = None

    # PHASE 1 VARS
    local_port = 0
    local_port_locked = False
    local_port_error = False
    conn_port = 0
    conn_addr = ""
    conn_port_locked = False
    conn_addr_locked = False
    conn_port_error = False
    conn_addr_error = False
    conn_started = False
    conn_established = False

    # PHASE 2 VARS
    board_matrix = initialize_board()
    board_tile_matrix = None
    board_tile_matrix_generated = False
    playing_as_white = False
    game_ongoing = True
    game_moves = 0
    game_result = ""

    # GAME LOOP
    while running:
        # CLEAR AFTER FLIP
        SCREEN.fill(colors.BLACK)

        # EVENT CATCHES
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # GAME PHASE 1 KEY OPTIONS
                if game_phase == 1:
                    if event.dict["key"] == 13:
                        if not local_port_locked:
                            if 1024 < local_port < 65535:
                                local_port_locked = True

                        elif not conn_port_locked:
                            if 1024 < conn_port < 65535:
                                conn_port_locked = True

                        elif not conn_addr_locked:
                            conn_addr_parts = conn_addr.split(".")
                            if len(conn_addr_parts) == 4:
                                addr_valid = True
                                for addr_part in conn_addr_parts:
                                    if int(addr_part) > 255:
                                        addr_valid = False
                                        break
                                if addr_valid:
                                    conn_addr_locked = True

                    elif event.dict["key"] == 8:
                        if not local_port_locked:
                            local_port_error = False
                            if local_port > 10:
                                local_port = floor(local_port / 10)
                            else:
                                local_port = 0

                        elif not conn_port_locked:
                            conn_port_error = False
                            if conn_port > 10:
                                conn_port = floor(conn_port / 10)
                            else:
                                conn_port = 0

                        elif not conn_addr_locked:
                            conn_addr_error = False
                            if len(conn_addr) > 0:
                                conn_addr = conn_addr[:-1]
                                if conn_addr[-1:] == ".":
                                    conn_addr = conn_addr[:-1]

                    elif event.dict["key"] == 46:
                        if not conn_addr_locked:
                            conn_addr_error = False
                            addr_split = conn_addr.split(".")
                            if len(addr_split) < 4 and len(addr_split[-1]) > 0:
                                conn_addr += "."

                    else:
                        if not local_port_locked:
                            if event.dict["unicode"].isnumeric() and local_port * 10 + int(event.dict["unicode"]) < 65535:
                                local_port = local_port * 10 + int(event.dict["unicode"])
                                local_port_error = False
                            else:
                                local_port_error = True

                        elif not conn_port_locked:
                            if event.dict["unicode"].isnumeric() and conn_port * 10 + int(event.dict["unicode"]) < 65535:
                                conn_port = conn_port * 10 + int(event.dict["unicode"])
                                conn_port_error = False
                            else:
                                conn_port_error = True

                        elif not conn_addr_locked:
                            addr_split = conn_addr.split(".")
                            if event.dict["unicode"].isnumeric() and len(conn_addr) < 15 and len(addr_split) < 5:
                                if not len(addr_split) == 4 or not len(addr_split[-1]) == 3:
                                    if len(addr_split[-1]) == 3:
                                        conn_addr += "."
                                    conn_addr += event.dict["unicode"]
                                    conn_addr_error = False
                                else:
                                    conn_addr_error = True
                            else:
                                conn_addr_error = True

        # GAME LOGIC: PHASE SEPARATED
        # PHASE 0: CHOOSE HOST/JOIN
        if game_phase == 0 and not GAME_DEBUG:

            host_btn = Button(SCREEN_W*0.25, SCREEN_H*0.2, SCREEN_W*0.25, SCREEN_H*0.6, "HOST", colors.WHITE, colors.WHITE, 2)
            join_btn = Button(SCREEN_W*0.55, SCREEN_H*0.2, SCREEN_W*0.25, SCREEN_H*0.6, "JOIN", colors.WHITE, colors.WHITE, 2)

            render_text("CHOOSE CONNECTION MODE:", SCREEN_W*0.33, SCREEN_H*0.1, "L")

            if host_btn.draw():
                host_mode = True
                game_phase = 1
            if join_btn.draw():
                host_mode = False
                game_phase = 1

        # PHASE 1: UDP CONN SETUP
        elif game_phase == 1 and not GAME_DEBUG:
            # HOST CONN SETUP
            if host_mode:
                if not local_port_locked:
                    render_text("Enter port for UDP socket (confirm with enter): ", 0.1*SCREEN_W, 0.1*SCREEN_H, "l")
                    if local_port > 0:
                        render_text(f"{local_port}", 0.65 * SCREEN_W, 0.1 * SCREEN_H, "l")
                    if local_port_error:
                        render_text(f"Possible ports are in range 1024 - 65535", 0.1 * SCREEN_W, 0.2 * SCREEN_H, "l", colors.RED)
                elif not conn_established:
                    if LAST_REC_DATA == "PyChessByNicoConnReq":
                        LAST_REC_DATA = None
                        conn_established = True
                        conn_socket = LAST_REC_ADDR
                        paw = randint(1, 2)
                        Thread(target=conn_send, args=(local_socket, f"PyChessByNicoConnAcc.{paw}", conn_socket)).start()
                        if paw == 1:
                            playing_as_white = True
                        else:
                            playing_as_white = False
                        game_phase = 2
                    if not conn_started:
                        conn_started = True
                        local_socket.bind(("", local_port))
                        Thread(target=conn_rec, args=(local_socket,)).start()
                    render_text("Waiting for a connection...", SCREEN_W*0.33, SCREEN_H*0.1, "L")

            # CLIENT CONN SETUP
            else:
                if not local_port_locked:
                    render_text("Enter port for UDP socket (confirm with enter): ", 0.1 * SCREEN_W, 0.1 * SCREEN_H, "l")
                    if local_port > 0:
                        render_text(f"{local_port}", 0.65 * SCREEN_W, 0.1 * SCREEN_H, "l")
                    if local_port_error:
                        render_text(f"Possible ports are in range 1024 - 65535", 0.1 * SCREEN_W, 0.2 * SCREEN_H, "l", colors.RED)

                elif not conn_port_locked:
                    render_text("Enter host port (confirm with enter): ", 0.1 * SCREEN_W, 0.1 * SCREEN_H, "l")
                    if conn_port > 0:
                        render_text(f"{conn_port}", 0.52 * SCREEN_W, 0.1 * SCREEN_H, "l")
                    if conn_port_error:
                        render_text(f"Possible ports are in range 1024 - 65535", 0.1 * SCREEN_W, 0.2 * SCREEN_H, "l", colors.RED)

                elif not conn_addr_locked:
                    render_text("Enter host ip (confirm with enter): ", 0.1 * SCREEN_W, 0.1 * SCREEN_H, "l")
                    if conn_addr:
                        render_text(f"{conn_addr}", 0.5 * SCREEN_W, 0.1 * SCREEN_H, "l")
                    if conn_addr_error:
                        render_text(f"IP has to be like ###.###.###.###", 0.1 * SCREEN_W, 0.2 * SCREEN_H, "l", colors.RED)
                        render_text(f"With each ### < 256", 0.1 * SCREEN_W, 0.3 * SCREEN_H, "l", colors.RED)

                elif not conn_established:
                    if LAST_REC_DATA is not None and LAST_REC_DATA.split(".")[0] == "PyChessByNicoConnAcc":
                        if LAST_REC_DATA.split(".")[1] == "1":
                            playing_as_white = False
                        else:
                            playing_as_white = True
                        LAST_REC_DATA = None
                        conn_established = True
                        conn_socket = LAST_REC_ADDR
                        game_phase = 2
                    if not conn_started:
                        conn_started = True
                        local_socket.bind(("", local_port))
                        Thread(target=conn_send, args=(local_socket, "PyChessByNicoConnReq", (conn_addr, conn_port))).start()
                        Thread(target=conn_rec, args=(local_socket,)).start()
                    render_text("Establishing connection...", SCREEN_W * 0.33, SCREEN_H * 0.1, "L")

        # PHASE 2: ...
        elif game_phase == 2 and not GAME_DEBUG:
            # GENERATE BOARD TILES
            if not board_tile_matrix_generated:
                board_tile_matrix = init_board((368, 32), 100, colors.WHITE, colors.DARK_BLUE)
                board_tile_matrix_generated = True

            if game_ongoing:
                # ROUND IF WHITE
                if game_moves % 2 == 0 and playing_as_white or game_moves % 2 == 1 and not playing_as_white:
                    draw_board(board_matrix, board_tile_matrix, (368, 32), 100, playing_as_white)
                    if MOVE_PLAYED is not None:
                        Thread(target=conn_send, args=(local_socket, f"{MOVE_PLAYED[0][0]}.{MOVE_PLAYED[0][1]}-{MOVE_PLAYED[1][0]}.{MOVE_PLAYED[1][1]}", conn_socket)).start()
                        MOVE_REQUESTED = False
                        MOVE_PLAYED = None
                        game_moves += 1

                # ROUND IF BLACK
                else:
                    draw_board(board_matrix, board_tile_matrix, (368, 32), 100, playing_as_white, False)
                    if not MOVE_REQUESTED:
                        Thread(target=conn_rec, args=(local_socket,)).start()
                        MOVE_REQUESTED = True
                    if LAST_REC_DATA is not None:
                        rds = LAST_REC_DATA.split("-")
                        ds1 = rds[0].split(".")
                        ds2 = rds[1].split(".")
                        board_matrix[int(ds2[0])][int(ds2[1])] = board_matrix[int(ds1[0])][int(ds1[1])]
                        board_matrix[int(ds1[0])][int(ds1[1])] = 0
                        LAST_REC_DATA = None
                        game_moves += 1

                # CHECK IF GAME ENDED
                bkf = wkf = False
                for i in board_matrix:
                    for j in i:
                        if j == 5:
                            wkf = True
                        elif j == 15:
                            bkf = True

                if not wkf and playing_as_white or not bkf and not playing_as_white:
                    game_result = "YOU LOST!"
                    game_ongoing = False
                    game_phase = 3
                elif not wkf and not playing_as_white or not bkf and playing_as_white:
                    game_result = "YOU WON!"
                    game_ongoing = False
                    game_phase = 3

        # PHASE 3
        elif game_phase == 3 or GAME_DEBUG:
            gg_text = XL_FONT.render(game_result, True, colors.WHITE)
            SCREEN.blit(gg_text, (SCREEN_W * 0.4, SCREEN_H * 0.4))

        # OUTPUT SCREEN IN 60 FPS
        pygame.display.flip()
        CLOCK.tick(FPS)

    # EXIT
    pygame.quit()
    exit()

if __name__ == "__main__":
    main()
