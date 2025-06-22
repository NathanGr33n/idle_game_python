# idle_game.py
# By: NathanGr33n
# Updated: June 22, 2025
# A GUI version of the idle game using Pygame

# -------- Import Libraries --------
import pygame               # Pygame is used for creating the GUI
import time                 # Time is used for tracking the passage of time between fund increments
import sys                  # Used to cleanly exit the game when the window is closed

# -------- Initialize Pygame Window --------
pygame.init()                                       # Initialize all imported Pygame modules
WIDTH, HEIGHT = 800, 600                            # Set the dimensions of the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))   # Create a window with the given dimensions
pygame.display.set_caption("Idle Game GUI")         # Set the title of the game window
clock = pygame.time.Clock()                         # Create a clock to manage frame rate
font = pygame.font.SysFont(None, 28)                # Use default font with size 28 for on-screen text

# -------- Game State Variables --------
funds = 0                                            # Current total amount of funds the player has
funds_per_second = 1                                 # Number of funds gained every second

# Dictionary containing all upgrade options and their properties
upgrades = {
    "Employment": {"cost": 25, "cps": 8, "owned": 0},                  # Each upgrade has a cost, cps (funds/sec), and owned count
    "Treasury Bonds": {"cost": 100, "cps": 4, "owned": 0},
    "Certificates of Deposit (CD)": {"cost": 500, "cps": 5, "owned": 0},
    "Index Funds": {"cost": 1000, "cps": 9, "owned": 0},
    "eCommerce Business": {"cost": 2000, "cps": 15, "owned": 0},
    "Crypto": {"cost": 10000, "cps": 22, "owned": 0},
    "Real Estate": {"cost": 50000, "cps": 35, "owned": 0},
}

# -------- Layout and Button Settings --------
BUTTON_WIDTH = 300                                  # Width of upgrade buttons
BUTTON_HEIGHT = 40                                  # Height of upgrade buttons
PADDING = 10                                        # Vertical space between buttons
MARGIN_TOP = 100                                    # Top margin where buttons start
button_rects = {}                                   # Dictionary to store button rectangles by name

# -------- UI Drawing Functions --------

def draw_text(text, x, y, color=(255, 255, 255)):
    """Draw a single line of text at a given (x, y) location."""
    label = font.render(text, True, color)          # Render the text with anti-aliasing and color
    screen.blit(label, (x, y))                      # Draw the rendered text on screen

def draw_ui():
    """Draw the full game interface including funds and upgrade buttons."""
    screen.fill((30, 30, 30))                       # Fill the background with a dark gray color

    # Draw player stats at the top
    draw_text(f"Funds: ${int(funds)}", 30, 20)       # Display total funds
    draw_text(f"Funds/sec: {funds_per_second}", 30, 50)  # Display current funds per second

    # Draw all upgrade buttons in order
    y = MARGIN_TOP                                   # Start drawing buttons from top margin
    for name, data in upgrades.items():              # Loop through each upgrade in the dictionary
        btn_rect = pygame.Rect(30, y, BUTTON_WIDTH, BUTTON_HEIGHT)  # Create a button rectangle
        button_rects[name] = btn_rect                # Store this rect so we can detect clicks later
        pygame.draw.rect(screen, (70, 130, 180), btn_rect)          # Fill button with a bluish color
        pygame.draw.rect(screen, (255, 255, 255), btn_rect, 2)      # Draw white border around button

        # Create the button label text
        upgrade_text = f"{name}: {data['owned']} owned | +{data['cps']} cps | Cost: ${data['cost']}"
        draw_text(upgrade_text, btn_rect.x + 10, btn_rect.y + 10)   # Draw label inside button
        y += BUTTON_HEIGHT + PADDING                # Move to the next vertical position for the next button

# -------- Game Logic --------

def try_purchase(name):
    """Try to buy an upgrade if the player has enough funds."""
    global funds, funds_per_second                   # Reference global game state
    item = upgrades[name]                            # Get the selected upgrade
    if funds >= item["cost"]:                        # If the player has enough funds
        funds -= item["cost"]                        # Deduct the upgrade cost
        item["owned"] += 1                           # Increase the number of owned upgrades
        funds_per_second += item["cps"]              # Increase the funds/sec by the upgrade's cps
        item["cost"] = int(item["cost"] * 1.125)     # Increase cost for next purchase (scaling)

# -------- Main Game Loop --------

last_tick = time.time()                              # Store time of last fund increment
running = True                                       # Control variable for main loop

while running:
    # -------- Passive Fund Generation --------
    now = time.time()                                # Get current time
    if now - last_tick >= 1:                         # If at least 1 second has passed
        funds += funds_per_second                    # Add current cps to funds
        last_tick = now                              # Reset the last_tick

    # -------- Handle Events --------
    for event in pygame.event.get():                 # Process all events in event queue
        if event.type == pygame.QUIT:                # If window is closed
            running = False                          # Stop the loop to quit the game

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # If left mouse click
            mouse_pos = event.pos                    # Get position of the mouse click
            for name, rect in button_rects.items():  # Check each upgrade button
                if rect.collidepoint(mouse_pos):     # If mouse is inside the button
                    try_purchase(name)               # Attempt to purchase the upgrade

    # -------- Draw Everything --------
    draw_ui()                                        # Redraw the interface and buttons
    pygame.display.flip()                            # Update the full display
    clock.tick(60)                                   # Cap the frame rate at 60 FPS

# -------- Clean Exit --------
pygame.quit()                                        # Close Pygame resources
sys.exit()                                           # Exit the Python interpreter
