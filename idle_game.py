# idle_game.py
# By: NathanGr33n
# Updated: June 22, 2025
# A GUI idle game using Pygame with Save/Load, Auto-Save, and Animated Glowing Upgrade Buttons

# -------- Import Libraries --------
import pygame               # GUI framework
import time                 # Used for timing
import sys                  # Clean program exit
import json                 # Save/load game data
import os                   # Check if save file exists
import math                 # Used for sine wave animation for glowing effect

# -------- Initialize Pygame --------
pygame.init()                                                   # Initialize all Pygame modules
WIDTH, HEIGHT = 800, 600                                        # Screen dimensions
screen = pygame.display.set_mode((WIDTH, HEIGHT))               # Create game window
pygame.display.set_caption("Idle Game GUI")                     # Set window title
clock = pygame.time.Clock()                                     # Frame rate manager
font = pygame.font.SysFont(None, 28)                            # Default font for text

# -------- Game State Variables --------
funds = 0                                                       # Total funds player owns
funds_per_second = 1                                            # Passive income per second

# Dictionary of upgrade definitions (cost, cps = income rate, owned = how many player owns)
upgrades = {
    "Employment": {"cost": 25, "cps": 2, "owned": 0},
    "Treasury Bonds": {"cost": 100, "cps": 4, "owned": 0},
    "Certificates of Deposit (CD)": {"cost": 500, "cps": 6, "owned": 0},
    "Index Funds": {"cost": 1000, "cps": 9, "owned": 0},
    "eCommerce Business": {"cost": 2000, "cps": 15, "owned": 0},
    "Crypto": {"cost": 10000, "cps": 22, "owned": 0},
    "Real Estate": {"cost": 50000, "cps": 35, "owned": 0},
}

SAVE_FILE = "idle_save.json"                                     # Save file path

# -------- UI Layout Settings --------
BUTTON_WIDTH = WIDTH - 60                                       # Button spans nearly full width
BUTTON_HEIGHT = 60                                              # Taller button
PADDING = 10                                                    # Space between buttons
MARGIN_TOP = 100                                                # Vertical offset for upgrade buttons
button_rects = {}                                               # Store clickable areas for buttons

# -------- Save and Load Functions --------

def save_game():
    """Save current game state to a file."""
    data = {
        "funds": funds,
        "funds_per_second": funds_per_second,
        "upgrades": upgrades
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print("Game saved.")

def load_game():
    """Load game state from save file if it exists."""
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
        print("Game loaded.")
    else:
        print("No save file found. Starting new game.")

# -------- UI Drawing --------

def draw_text(text, x, y, color=(255, 255, 255)):
    """Draw a line of text at position (x, y) in specified color."""
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

def draw_ui():
    """Draw UI with animated glowing upgrade buttons."""
    screen.fill((30, 30, 30))                                   # Fill background with dark gray

    draw_text(f"Funds: ${int(funds)}", 30, 20)                  # Display current funds
    draw_text(f"Funds/sec: {funds_per_second}", 30, 50)         # Display income rate

    # Calculate glow transparency using sine wave (pulsing effect)
    tick = pygame.time.get_ticks() / 1000.0                     # Time in seconds
    glow_alpha = int(80 + 50 * math.sin(tick * 2))              # Pulsing between 30–130

    y = MARGIN_TOP                                              # Start button vertical position
    for name, data in upgrades.items():
        rect = pygame.Rect(30, y, BUTTON_WIDTH, BUTTON_HEIGHT)  # Create button rectangle
        button_rects[name] = rect                               # Save for click detection

        # Create semi-transparent green glow
        glow_surface = pygame.Surface((BUTTON_WIDTH, BUTTON_HEIGHT), pygame.SRCALPHA)
        glow_surface.fill((0, 255, 0, glow_alpha))              # Bright green glow w/ variable alpha
        screen.blit(glow_surface, rect.topleft)                 # Draw glow beneath button

        pygame.draw.rect(screen, (34, 94, 58), rect)            # Draw dark green button background
        pygame.draw.rect(screen, (255, 255, 255), rect, 2)      # Draw white border around button

        label = f"{name}: {data['owned']} owned | +{data['cps']} cps | Cost: ${data['cost']}"
        draw_text(label, rect.x + 15, rect.y + 18)              # Draw upgrade text
        y += BUTTON_HEIGHT + PADDING                           # Move down for next button

# -------- Game Logic --------

def try_purchase(name):
    """Try to purchase an upgrade if player has enough funds."""
    global funds, funds_per_second
    item = upgrades[name]
    if funds >= item["cost"]:
        funds -= item["cost"]
        item["owned"] += 1
        funds_per_second += item["cps"]
        item["cost"] = int(item["cost"] * 1.125)               # Increase future cost

# -------- Initialize Game --------
load_game()                                                    # Load save on startup
last_tick = time.time()                                        # Timer for income generation
last_auto_save = time.time()                                   # Timer for auto-saving
running = True                                                 # Main loop condition

# -------- Main Game Loop --------
while running:
    now = time.time()                                          # Get current time

    # Passive income (1 fund tick per second)
    if now - last_tick >= 1:
        funds += funds_per_second
        last_tick = now

    # Auto-save every 30 seconds
    if now - last_auto_save >= 30:
        save_game()
        last_auto_save = now

    # Handle user input events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_game()                                        # Save on quit
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            for name, rect in button_rects.items():
                if rect.collidepoint(pos):
                    try_purchase(name)

    draw_ui()                                                  # Draw the interface
    pygame.display.flip()                                      # Update the screen
    clock.tick(60)                                             # Cap frame rate to 60 FPS

# -------- Clean Exit --------
pygame.quit()                                                  # Close Pygame
sys.exit()                                                     # End program
