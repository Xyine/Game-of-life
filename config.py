class Config:
    DEAD: int = 0
    ALIVE: int = 1
    ZOMBIE: int = 2
    CELL_SIZE = 15
    BUTTON_HEIGHT = 40
    BUTTON_WIDTH = 100
    MARGIN = 10
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 600
    UI_WIDTH = 200
    GAME_WIDTH = WINDOW_WIDTH - UI_WIDTH
    SCROLL_SPEED = 20
    MIN_CELL_SIZE = 5
    MAX_CELL_SIZE = 60
    ZOOM_FACTOR = 2
    CELL_COLORS = {
        ALIVE: (255, 255, 255),
        ZOMBIE: (0, 200, 0)
    }
    BOARD_FILES = {
        "Blinker": "board_file/blinker.json",
        "Pulsar": "board_file/pulsar.json",
        "LWS": "board_file/lws.json"
    }
    BOARD_SIZES = {
        "Small": (53, 53),
        "Medium": (200, 200),
        "Big": (1000, 1000)
    }
    SPEEDS = {
        "Fast": 0.5,
        "Medium": 1,
        "Slow": 3
    }