# main.py
# By: NathanGr33n
# Updated: July 2025
# Main entry point for the Idle Game with GUI, upgrades, save/load, achievements, a main menu, and a passive offline earnings popup.

# -------- Import Libraries --------
import pygame                   # Pygame for GUI and event handling
import time                     # For time tracking and offline earnings calculation
import sys                      # For cleanly exiting the program
from config import WIDTH, HEIGHT  # Screen dimensions from config
from data import upgrades, achievements  # Game data definitions (upgrades and achievements)
from state import save_game, load_game   # Game state save/load functions
from logic import try_purchase, check_achievements  # Core game logic (purchases, achievements)
from ui import (draw_ui, draw_menu, get_button_rects, draw_offline_popup)  # Drawing functions including the new offline popup
                
# -------- Initialize Pygame & Music --------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Idle Game GUI")
clock = pygame.time.Clock()

# Initialize Pygame mixer for music
pygame.mixer.init()

# Load background music from your provided file
pygame.mixer.music.load("music/8bit_background_music.mp3")

# Start playing the music on loop (-1 means infinite loop)
pygame.mixer.music.play(-1)


# -------- Initialize Pygame --------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Set up the game window
pygame.display.set_caption("Idle Game GUI")        # Set window title
clock = pygame.time.Clock()                        # Clock to control frame rate

# -------- Load Game State --------
# Load saved game data: funds, income rate, upgrades, achievements, and last played timestamp
funds, funds_per_second, last_played = load_game(upgrades, achievements)

# Initialize the game state dictionary
state = {
    'funds': funds,
    'funds_per_second': funds_per_second,
    'upgrades': upgrades  # Current upgrade data after loading
}

# -------- Calculate Offline Earnings --------
current_time = time.time()  # Current time
offline_seconds = int(current_time - last_played)  # Time elapsed since last play (in seconds)
offline_earnings = offline_seconds * funds_per_second  # Total offline earnings
state['funds'] += offline_earnings  # Add offline earnings to player's funds

# Show popup if offline earnings exist
showing_offline_popup = offline_seconds > 0  # Flag to show the popup
offline_popup_close_button = None  # Store the close button rect for click detection

# -------- Timers for Passive Income & Auto-Save --------
last_tick = time.time()  # Last time funds were generated
last_save = time.time()  # Last time game was auto-saved

# -------- Screen Manager --------
current_screen = "menu"  # Start with the main menu

# -------- Main Game Loop --------
running = True
while running:
    now = time.time()  # Get the current time each frame

    # Passive income and auto-save only in the game screen and when popup is closed
    if current_screen == "game" and not showing_offline_popup:
        if now - last_tick >= 1:
            state['funds'] += state['funds_per_second']  # Add passive income
            check_achievements(state, achievements)      # Check achievements
            last_tick = now

        if now - last_save >= 30:
            save_game(state['funds'], state['funds_per_second'], state['upgrades'], achievements)
            last_save = now

    # -------- Handle Events --------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Save and exit on window close
            save_game(state['funds'], state['funds_per_second'], state['upgrades'], achievements)
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            pos = event.pos  # Get click position

            # Handle clicks on the offline popup (blocks other clicks)
            if showing_offline_popup and offline_popup_close_button:
                if offline_popup_close_button.collidepoint(pos):
                    showing_offline_popup = False  # Dismiss the popup
            elif not showing_offline_popup:
                buttons = get_button_rects()  # Get current button positions

                # Handle main menu buttons
                if current_screen == "menu":
                    if buttons.get("Start Game") and buttons["Start Game"].collidepoint(pos):
                        current_screen = "game"  # Switch to game screen
                    elif buttons.get("Exit") and buttons["Exit"].collidepoint(pos):
                        save_game(state['funds'], state['funds_per_second'], state['upgrades'], achievements)
                        running = False  # Exit game

                # Handle in-game buttons
                elif current_screen == "game":
                    if buttons.get("Back to Menu") and buttons["Back to Menu"].collidepoint(pos):
                        current_screen = "menu"  # Return to menu
                    else:
                        # Handle upgrade purchases
                        for name in state['upgrades']:
                            if buttons.get(name) and buttons[name].collidepoint(pos):
                                try_purchase(name, state)

    # -------- Draw the Current Screen --------
    if current_screen == "menu":
        draw_menu(screen)  # Draw main menu
    elif current_screen == "game":
        draw_ui(screen, state, state['upgrades'], achievements)  # Draw game UI

    # Draw offline earnings popup on top if active (blocks gameplay)
    if showing_offline_popup:
        offline_popup_close_button = draw_offline_popup(screen, offline_earnings, offline_seconds)
    else:
        offline_popup_close_button = None  # No popup active

    # -------- Update Display --------
    pygame.display.flip()
    clock.tick(60)  # Limit to 60 frames per second

# -------- Clean Exit --------
pygame.quit()  # Shut down Pygame
sys.exit()     # Exit Python
