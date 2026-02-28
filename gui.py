import pygame
import time
from config import Config
from game_of_life import GameOfLife
from rules import classic_rules, zombie_rules, von_neumann_rules, respawn_rules


class GameGUI:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT))
        pygame.display.set_caption("Game of Life")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 30)

        self.engine = None
        self.board = None
        self.offset_x = 0
        self.offset_y = 0
        self.cell_size = float(Config.CELL_SIZE)
        self.paused = True
        self.current_view = "game"
        self.running = True

        self.current_speed = "Fast"
        self.last_update = time.time()
        self.current_board_size = "Medium"
        self.RULES = {
            "Classic": classic_rules,
            "Zombie": zombie_rules,
            "Von Neumann": von_neumann_rules,
            "Respawn": respawn_rules
        }
        self.current_rule = "Classic"
        self.current_file = None

        self.start_button = self.create_side_button(0)
        self.settings_button = self.create_side_button(1)
        self.reset_button = self.create_side_button(2)
        self.exit_button = self.create_side_button(3)

        self.speed_buttons = self.create_horizontal_buttons(["Fast", "Medium", "Slow"], 60)
        self.size_buttons = self.create_horizontal_buttons(["Small", "Medium", "Big"], 160)
        self.rule_buttons = self.create_horizontal_buttons(["Classic", "Zombie", "Von Neumann", "Respawn"], 260)
        self.file_buttons = self.create_horizontal_buttons(["Blinker", "Pulsar", "LWS"], 360)

    def create_side_button(self, index):
        return pygame.Rect(
            Config.GAME_WIDTH + Config.MARGIN,
            Config.MARGIN * (index + 1) + Config.BUTTON_HEIGHT * index,
            Config.UI_WIDTH - 2 * Config.MARGIN,
            Config.BUTTON_HEIGHT
        )

    def create_horizontal_buttons(self, labels, start_y):
        buttons = {}
        start_x = 50
        spacing_x = Config.BUTTON_WIDTH + Config.MARGIN

        for i, name in enumerate(labels):
            x = start_x + i * spacing_x
            buttons[name] = pygame.Rect(x, start_y, Config.BUTTON_WIDTH, Config.BUTTON_HEIGHT)
        return buttons

    def create_engine(self):
        width, height = Config.BOARD_SIZES[self.current_board_size]
        rules = self.RULES[self.current_rule]
        file = Config.BOARD_FILES[self.current_file] if self.current_file else None
        self.engine = GameOfLife(width=width, height=height, rules=rules, file=file)
        self.board = self.engine.board

    def reset(self):
        self.engine = None
        self.board = None
        self.offset_x = 0
        self.offset_y = 0
        self.paused = True
        self.last_update = time.time()

    def handle_mouse(self, event):
        if self.start_button.collidepoint(event.pos):
            self.paused = not self.paused
            if self.engine is None:
                self.create_engine()

        elif self.settings_button.collidepoint(event.pos):
            self.current_view = "settings" if self.current_view == "game" else "game"

        elif self.reset_button.collidepoint(event.pos) and self.engine:
            self.reset()

        elif self.exit_button.collidepoint(event.pos):
            self.running = False

        elif self.current_view == "settings":
            self.handle_settings_click(event.pos)

    def handle_settings_click(self, pos):
        for name, rect in self.speed_buttons.items():
            if rect.collidepoint(pos):
                self.current_speed = name

        if self.engine is None:
            for name, rect in self.size_buttons.items():
                if rect.collidepoint(pos):
                    self.current_board_size = name

            for name, rect in self.rule_buttons.items():
                if rect.collidepoint(pos):
                    self.current_rule = name

            for name, rect in self.file_buttons.items():
                if rect.collidepoint(pos):
                    self.current_file = name

    def handle_keyboard(self, event):
        if event.key == pygame.K_LEFT:
            self.offset_x -= Config.SCROLL_SPEED
        elif event.key == pygame.K_RIGHT:
            self.offset_x += Config.SCROLL_SPEED
        elif event.key == pygame.K_UP:
            self.offset_y -= Config.SCROLL_SPEED
        elif event.key == pygame.K_DOWN:
            self.offset_y += Config.SCROLL_SPEED

    def handle_zoom(self, event):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        old_size = self.cell_size

        if event.y > 0:
            self.cell_size = min(self.cell_size * Config.ZOOM_FACTOR, Config.MAX_CELL_SIZE)
        elif event.y < 0:
            self.cell_size = max(self.cell_size / Config.ZOOM_FACTOR, Config.MIN_CELL_SIZE)

        scale = self.cell_size / old_size
        self.offset_x = (self.offset_x + mouse_x) * scale - mouse_x
        self.offset_y = (self.offset_y + mouse_y) * scale - mouse_y

    def update(self):
        if self.engine and not self.paused:
            now = time.time()
            if now - self.last_update >= Config.SPEEDS[self.current_speed]:
                self.engine.step()
                self.board = self.engine.board
                self.last_update = now

    def draw_board(self):
        if not self.board:
            return

        max_x = max(0, len(self.board[0]) * self.cell_size - Config.GAME_WIDTH)
        max_y = max(0, len(self.board) * self.cell_size - Config.WINDOW_HEIGHT)
        self.offset_x = max(0, min(self.offset_x, max_x))
        self.offset_y = max(0, min(self.offset_y, max_y))

        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if cell == Config.DEAD:
                    continue

                color = Config.CELL_COLORS.get(cell, (255, 0, 0))
                x = j * self.cell_size - self.offset_x
                y = i * self.cell_size - self.offset_y

                if -self.cell_size < x < Config.GAME_WIDTH and -self.cell_size < y < Config.WINDOW_HEIGHT:
                    pygame.draw.rect(self.screen, color, (int(x), int(y), int(self.cell_size), int(self.cell_size)))

    def draw_side_panel(self):
        pygame.draw.rect(self.screen, (30, 30, 30), (Config.GAME_WIDTH, 0, Config.UI_WIDTH, Config.WINDOW_HEIGHT))
        self.draw_button(self.start_button, "Start" if self.paused else "Pause", (0, 200, 0) if self.paused else (200, 0, 0))
        self.draw_button(self.settings_button, "Settings", (150, 150, 0))
        self.draw_button(self.reset_button, "Reset", (200, 100, 0))
        self.draw_button(self.exit_button, "Exit", (0, 0, 200))

    def draw_button(self, rect, label, color):
        pygame.draw.rect(self.screen, color, rect)
        text = self.font.render(label, True, (255, 255, 255))
        self.screen.blit(text, (rect.x + 10, rect.y + 5))

    def draw_settings(self):
        self.screen.fill((20, 20, 20))
        self.draw_button_group(self.speed_buttons, self.current_speed, "Speed", 30)
        self.draw_button_group(self.size_buttons, self.current_board_size, "Board Size", 130)
        self.draw_button_group(self.rule_buttons, self.current_rule, "Rules", 230)
        self.draw_button_group(self.file_buttons, self.current_file, "Patterns", 330)

    def draw_button_group(self, buttons, current, title, title_y):
        self.screen.blit(self.font.render(title, True, (255, 255, 255)), (50, title_y))
        for name, rect in buttons.items():
            color = (0, 200, 0) if name == current else (150, 150, 150)
            pygame.draw.rect(self.screen, color, rect)
            text = self.font.render(name, True, (255, 255, 255))
            self.screen.blit(text, (rect.x + 10, rect.y + 5))

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse(event)
                elif event.type == pygame.KEYDOWN:
                    self.handle_keyboard(event)
                elif event.type == pygame.MOUSEWHEEL:
                    self.handle_zoom(event)

            self.update()

            self.screen.fill((0, 0, 0))
            if self.current_view == "game":
                self.draw_board()
            else:
                self.draw_settings()

            self.draw_side_panel()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
