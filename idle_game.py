# idle_game.py
# By: NathanGr33n
# Updated: June 22, 2025
# A GUI idle game using Pygame, now with Save/Load functionality

# -------- Import Libraries --------
import pygame               # GUI library for drawing the game window and UI
import time                 # Used to track elapsed time for passive income
import sys                  # Allows for clean exit from the Python program
import json                 # For saving/loading game data in JSON format
import os                   # Used to check if a file exists

# -------- Initialize Pygame --------
pygame.init()                                           # Initialize all Pygame modules
WIDTH, HEIGHT = 800, 600                                # Set the width and height of the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))       # Create the game window with the given size
pygame.display.set_caption("Idle Game GUI")             # Set the window title
clock = pygame.time.Clock()                             # Create a clock object to control frame rate
font = pygame.font.SysFont(None, 28)                    # Set default font for text (size 28)

# -------- Game State Variables --------
funds = 0                                                # Player's total funds
funds_per_second = 1                                     # How many funds the player earns each second

# Dictionary of upgrades the player can buy
# Each entry has a name, cost, income rate (cps = currency per second), and owned count
upgrades = {
    "Employment": {"cost": 25, "cps": 2, "owned": 0},
    "Treasury Bonds": {"cost": 100, "cps": 4, "owned": 0},
    "Certificates of Deposit (CD)": {"cost": 500, "cps": 6, "owned": 0},
    "Index Funds": {"cost": 1000, "cps": 9, "owned": 0},
    "eCommerce Business": {"cost": 2000, "cps": 15, "owned": 0},
    "Crypto": {"cost": 10000, "cps": 22, "owned": 0},
    "Real Estate": {"cost": 50000, "cps": 35, "owned": 0},
}

SAVE_FILE = "idle_save.json"                             # File name to store saved game state

# -------- Save/Load Functions --------

def save_game():
    """Save the current game state into a JSON file."""
    data = {
        "funds": funds,                                  # Save player's funds
        "funds_per_second": funds_per_second,            # Save current income rate
        "upgrades": upgrades                             # Save owned upgrades and their states
    }
    with open(SAVE_FILE, "w") as f:                      # Open the file in write mode
        json.dump(data, f, indent=4)                     # Write JSON data to file
    print("Game saved.")                                 # Confirm save in console

def load_game():
    """Load game state from the save file if it exists."""
    global funds, funds_per_second, upgrades             # Reference the global game state variables
    if os.path.exists(SAVE_FILE):                        # Check if the save file exists
        with open(SAVE_FILE, "r") as f:                  # Open the file in read mode
            data = json.load(f)                          # Parse JSON data into a Python dictionary
            funds = data.get("funds", 0)                 # Load saved funds or default to 0
            funds_per_second = data.get("funds_per_second", 1)  # Load income or default to 1

            saved_upgrades = data.get("upgrades", {})    # Load saved upgrade states
            for name in upgrades:                        # For each default upgrade
                if name in saved_upgrades:               # If it exists in the saved file
                    upgrades[name].update(saved_upgrades[name])  # Merge saved values into current upgrade
        print("Game loaded.")                            # Confirm load in console
    else:
        print("No save file found. Starting new game.")  # Inform the user if there's no save data

# -------- UI Layout Configuration --------
BUTTON_WIDTH = 300                                       # Width of each upgrade button
BUTTON_HEIGHT = 40                                       # Height of each upgrade button
PADDING = 10                                             # Vertical spacing between buttons
MARGIN_TOP = 100                                         # Top margin for the first button
button_rects = {}                                        # Dictionary to hold clickable button rectangles

# -------- UI Drawing Functions --------

def draw_text(text, x, y, color=(255, 255, 255)):
    """Draw a single line of text at (x, y) using the default font."""
    label = font.render(text, True, color)               # Render the text surface
    screen.blit(label, (x, y))                           # Draw the text on the screen

def draw_ui():
    """Draw the current funds, income rate, and all upgrade buttons."""
    screen.fill((30, 30, 30))                            # Clear the screen with a dark gray background

    draw_text(f"Funds: ${int(funds)}", 30, 20)           # Show the total funds
    draw_text(f"Funds/sec: {funds_per_second}", 30, 50)  # Show the income rate

    y = MARGIN_TOP                                       # Start placing buttons from this y position
    for name, data in upgrades.items():                  # Loop through each upgrade
        rect = pygame.Rect(30, y, BUTTON_WIDTH, BUTTON_HEIGHT)  # Define the button area
        button_rects[name] = rect                        # Save this button's rect for click detection
        pygame.draw.rect(screen, (70, 130, 180), rect)   # Draw the button background
        pygame.draw.rect(screen, (255, 255, 255), rect, 2)  # Draw the white border
        label = f"{name}: {data['owned']} owned | +{data['cps']} cps | Cost: ${data['cost']}"
        draw_text(label, rect.x + 10, rect.y + 10)       # Draw upgrade information inside button
        y += BUTTON_HEIGHT + PADDING                     # Move down for next button

# -------- Game Logic --------

def try_purchase(name):
    """Attempt to buy the upgrade with the given name."""
    global funds, funds_per_second                       # Access global game state
    item = upgrades[name]                                # Get the upgrade dictionary
    if funds >= item["cost"]:                            # Only allow purchase if player can afford it
        funds -= item["cost"]                            # Deduct the upgrade cost from funds
        item["owned"] += 1                               # Increase the number of upgrades owned
        funds_per_second += item["cps"]                  # Increase passive income
        item["cost"] = int(item["cost"] * 1.125)         # Increase future cost of this upgrade

# -------- Main Game Setup --------
load_game()                                              # Attempt to load game state on startup
last_tick = time.time()                                  # Store time of last income generation
running = True                                           # Main game loop condition

# -------- Main Game Loop --------
while running:
    # Passive income system — adds funds once per second
    now = time.time()                                    # Get current time
    if now - last_tick >= 1:                             # If 1+ second has passed
        funds += funds_per_second                        # Add funds based on income rate
        last_tick = now                                  # Reset tick time

    # Handle events like clicks and window close
    for event in pygame.event.get():                     # Loop through all Pygame events
        if event.type == pygame.QUIT:                    # If player tries to close window
            save_game()                                  # Save the game state
            running = False                              # End the main loop
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # If left mouse click
            pos = event.pos                              # Get mouse click position
            for name, rect in button_rects.items():      # Loop through upgrade buttons
                if rect.collidepoint(pos):               # If the click was inside a button
                    try_purchase(name)                   # Try to buy that upgrade

    # Redraw the entire screen with updated data
    draw_ui()                                            # Draw the UI and upgrades
    pygame.display.flip()                                # Update the display with the new frame
    clock.tick(60)                                       # Limit the game to 60 frames per second

# -------- Clean Exit --------
pygame.quit()                                            # Shut down Pygame
sys.exit()                                               # Exit the Python interpreter
