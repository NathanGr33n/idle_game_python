# config.py
# By: NathanGr33n
# June 22, 2025
# Configuration constants for layout and appearance

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Button layout
BUTTON_WIDTH = WIDTH - 60
BUTTON_HEIGHT = 60
PADDING = 10
MARGIN_TOP = 100

# Colors
BG_COLOR = (30, 30, 30)
BUTTON_COLOR = (34, 94, 58)
TEXT_COLOR = (255, 255, 255)
GLOW_COLOR = (0, 255, 0)
BORDER_COLOR = (255, 255, 255)

# Save file
SAVE_FILE = "idle_save.json"

# Font size
FONT_SIZE = 28

#Light and Dark Themes
THEMES = {
	"light": {
	   "BG_COLOR": (240, 240, 240),
        "BUTTON_COLOR": (200, 200, 200),
        "TEXT_COLOR": (10, 10, 10),
        "BORDER_COLOR": (50, 50, 50)
        },
   	"dark": {
        "BG_COLOR": (30, 30, 30),
        "BUTTON_COLOR": (70, 130, 180),
        "TEXT_COLOR": (255, 255, 255),
        "BORDER_COLOR": (255, 255, 255)
    }
}