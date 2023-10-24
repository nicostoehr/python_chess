# pip install pygame
import math

import pygame
import socket
import colors
import connection_setup


# GLOBAL VARS
pygame.init()
pygame.font.init()
DISPLAY_INFO = pygame.display.Info()
SCREEN_W = DISPLAY_INFO.current_w*0.8
SCREEN_H = DISPLAY_INFO.current_h*0.8
SCREEN = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("CHESS")
CLOCK = pygame.time.Clock()
XL_FONT = pygame.font.SysFont("Arial", 64)
L_FONT = pygame.font.SysFont("Arial", 48)
M_FONT = pygame.font.SysFont("Arial", 30)
S_FONT = pygame.font.SysFont("Arial", 18)
FPS = 60


# OBJECT CLASSES
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
        center_height_offset = 0
        w_char_s = 0

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


# FUNCTIONS
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


# MAIN LOOP
def main():

    # MAIN VARS
    RUNNING = True
    game_phase = 0
    host_mode = None
    local_port = 0
    local_port_locked = False
    port_error = False


    # GAME LOOP
    while RUNNING:
        # CLEAR AFTER FLIP
        SCREEN.fill(colors.BLACK)

        # EVENT CATCHES
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
            if event.type == pygame.KEYDOWN:
                # GAME PHASE 1 KEY OPTIONS
                if game_phase == 1:
                    if event.dict["key"] == 13:
                        if 1024 < local_port < 65535:
                            local_port_locked = True
                    elif event.dict["key"] == 8:
                        port_error = False
                        if local_port > 10:
                            local_port = math.floor(local_port / 10)
                        else:
                            local_port = 0

                    else:
                        if event.dict["unicode"].isnumeric() and local_port * 10 + int(event.dict["unicode"]) < 65535:
                            local_port = local_port * 10 + int(event.dict["unicode"])
                            port_error = False
                        else:
                            port_error = True

        # GAME LOGIC: PHASE SEPARATED
        # PHASE 0: CHOOSE HOST/JOIN
        if game_phase == 0:

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
        if game_phase == 1:
            # HOST CONN SETUP
            if host_mode:
                if not local_port_locked:
                    render_text("Enter port for UDP socket (confirm with enter): ", 0.1*SCREEN_W, 0.1*SCREEN_H, "l")
                    if local_port > 0:
                        render_text(f"{local_port}", 0.65 * SCREEN_W, 0.1 * SCREEN_H, "l")
                    if port_error:
                        render_text(f"Possible ports are in range 1024 - 65535", 0.1 * SCREEN_W, 0.2 * SCREEN_H, "l", colors.RED)

            # CLIENT CONN SETUP
            else:
                if not local_port_locked:
                    render_text("Enter port for UDP socket (confirm with enter): ", 0.1 * SCREEN_W, 0.1 * SCREEN_H, "l")
                    if local_port > 0:
                        render_text(f"{local_port}", 0.65 * SCREEN_W, 0.1 * SCREEN_H, "l")
                    if port_error:
                        render_text(f"Possible ports are in range 1024 - 65535", 0.1 * SCREEN_W, 0.2 * SCREEN_H, "l", colors.RED)

        # OUTPUT SCREEN IN 60 FPS
        pygame.display.flip()
        CLOCK.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
