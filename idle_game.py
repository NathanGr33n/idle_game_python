# idle_game.py
# By: NathanGr33n
# Updated: June 22, 2025
# Idle game with GUI, Save/Load, Auto-Save, Glowing Buttons, and Achievement System

# -------- Import Libraries --------
import pygame               # GUI
import time                 # Timing
import sys                  # Exit
import json                 # Save/load
import os                   # Check file
import math                 # For glow animation

# -------- Initialize Pygame --------
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Idle Game GUI")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)

# -------- Game State Variables --------
funds = 0
funds_per_second = 1

# -------- Upgrade Definitions --------
upgrades = {
    "Employment": {"cost": 25, "cps": 2, "owned": 0},
    "Treasury Bonds": {"cost": 100, "cps": 4, "owned": 0},
    "Certificates of Deposit (CD)": {"cost": 500, "cps": 6, "owned": 0},
    "Index Funds": {"cost": 1000, "cps": 9, "owned": 0},
    "eCommerce Business": {"cost": 2000, "cps": 15, "owned": 0},
    "Crypto": {"cost": 10000, "cps": 22, "owned": 0},
    "Real Estate": {"cost": 50000, "cps": 35, "owned": 0},
}

# -------- Achievement Definitions --------
achievements = {
    "First Hundred": {
        "description": "Earn your first $100!",
        "condition": lambda: funds >= 100,
        "unlocked": False
    },
    "Investor": {
        "description": "Own 1 Index Fund",
        "condition": lambda: upgrades["Index Funds"]["owned"] >= 1,
        "unlocked": False
    },
    "Tycoon": {
        "description": "Reach $10,000 total funds",
        "condition": lambda: funds >= 10000,
        "unlocked": False
    },
    "Real Deal": {
        "description": "Own 1 Real Estate property",
        "condition": lambda: upgrades["Real Estate"]["owned"] >= 1,
        "unlocked": False
    },
}

# -------- Layout Settings --------
BUTTON_WIDTH = WIDTH - 60
BUTTON_HEIGHT = 60
PADDING = 10
MARGIN_TOP = 100
button_rects = {}

SAVE_FILE = "idle_save.json"

# -------- Save/Load Functions --------
def save_game():
    """Save current game state to file."""
    data = {
        "funds": funds,
        "funds_per_second": funds_per_second,
        "upgrades": upgrades,
        "achievements": {k: v["unlocked"] for k, v in achievements.items()}
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print("Game saved.")

def load_game():
    """Load game state from save file."""
    global funds, funds_per_second, upgrades
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            funds = data.get("funds", 0)
            funds_per_second = data.get("funds_per_second", 1)
            saved_upgrades = data.get("upgrades", {})
            for name in upgrades:
                if name in saved_upgrades:
                    upgrades[name].update(saved_upgrades[name])
            unlocked_achievements = data.get("achievements", {})
            for name in achievements:
                achievements[name]["unlocked"] = unlocked_achievements.get(name, False)
        print("Game loaded.")
    else:
        print("No save file found. Starting new game.")

# -------- Achievement Logic --------
def check_achievements():
    """Check and unlock achievements based on current state."""
    for name, data in achievements.items():
        if not data["unlocked"] and data["condition"]():
            data["unlocked"] = True
            print(f"Achievement Unlocked: {name} - {data['description']}")

# -------- UI Functions --------
def draw_text(text, x, y, color=(255, 255, 255)):
    """Render and draw text on screen."""
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

def draw_ui():
    """Draw all UI elements including buttons and achievements."""
    screen.fill((30, 30, 30))  # Background

    # Header
    draw_text(f"Funds: ${int(funds)}", 30, 20)
    draw_text(f"Funds/sec: {funds_per_second}", 30, 50)

    # Animated glow alpha
    tick = pygame.time.get_ticks() / 1000.0
    glow_alpha = int(80 + 50 * math.sin(tick * 2))

    # Draw Upgrade Buttons
    y = MARGIN_TOP
    for name, data in upgrades.items():
        rect = pygame.Rect(30, y, BUTTON_WIDTH, BUTTON_HEIGHT)
        button_rects[name] = rect

        # Glow surface
        glow = pygame.Surface((BUTTON_WIDTH, BUTTON_HEIGHT), pygame.SRCALPHA)
        glow.fill((0, 255, 0, glow_alpha))
        screen.blit(glow, rect.topleft)

        # Button and border
        pygame.draw.rect(screen, (34, 94, 58), rect)
        pygame.draw.rect(screen, (255, 255, 255), rect, 2)

        # Label
        label = f"{name}: {data['owned']} owned | +{data['cps']} cps | Cost: ${data['cost']}"
        draw_text(label, rect.x + 15, rect.y + 18)

        y += BUTTON_HEIGHT + PADDING

    # Draw Unlocked Achievements
    draw_text("Achievements Unlocked:", WIDTH - 320, 20)
    y2 = 50
    for name, data in achievements.items():
        if data["unlocked"]:
            draw_text(f"✔ {name}", WIDTH - 320, y2)
            y2 += 25

# -------- Game Logic --------
def try_purchase(name):
    """Buy an upgrade if affordable."""
    global funds, funds_per_second
    item = upgrades[name]
    if funds >= item["cost"]:
        funds -= item["cost"]
        item["owned"] += 1
        funds_per_second += item["cps"]
        item["cost"] = int(item["cost"] * 1.125)
        check_achievements()  # Check after each purchase

# -------- Game Initialization --------
load_game()
last_tick = time.time()
last_auto_save = time.time()
running = True

# -------- Main Loop --------
while running:
    now = time.time()

    # Add passive income every second
    if now - last_tick >= 1:
        funds += funds_per_second
        last_tick = now
        check_achievements()  # Check on income tick too

    # Auto-save every 30 seconds
    if now - last_auto_save >= 30:
        save_game()
        last_auto_save = now

    # Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_game()
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            for name, rect in button_rects.items():
                if rect.collidepoint(pos):
                    try_purchase(name)

    # Draw the full interface
    draw_ui()
    pygame.display.flip()
    clock.tick(60)

# -------- Clean Exit --------
pygame.quit()
sys.exit()
