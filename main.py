# main.py
# By: NathanGr33n
# Updated: July 2025
# Main entry point for the Idle Game with GUI, upgrades, save/load, achievements, offline income popup, background music, and Achievements screen.

# -------- Import Libraries --------
import pygame                   # Pygame for GUI and event handling
import time                     # For time tracking and offline income
import sys                      # For system exit
from config import WIDTH, HEIGHT  # Screen size from config file
from data import upgrades, achievements  # Game data: upgrades and achievements
from state import save_game, load_game   # Save/load functions
from logic import try_purchase, check_achievements  # Core game logic
from ui import (draw_ui, draw_menu, draw_achievements_screen, get_button_rects,
                draw_offline_popup)  # UI functions including popup and achievements screen

# -------- Initialize Pygame and Music --------
pygame.init()  # Initialize Pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Set up window with configured width and height
pygame.display.set_caption("Idle Game GUI")  # Set window title
clock = pygame.time.Clock()  # Clock to control frame rate

pygame.mixer.init()  # Initialize Pygame mixer for audio
pygame.mixer.music.load("music/8bit_background_music.mp3")  # Load background music
pygame.mixer.music.play(-1)  # Play music on loop (-1 = infinite looping)

# -------- Load Game State --------
funds, funds_per_second, last_played = load_game(upgrades, achievements)  # Load saved game state
state = {  # Initialize state dictionary for runtime game state
    'funds': funds,
    'funds_per_second': funds_per_second,
    'upgrades': upgrades
}

# -------- Calculate Offline Earnings --------
current_time = time.time()  # Get current time
offline_seconds = int(current_time - last_played)  # Calculate seconds since last play
offline_earnings = offline_seconds * funds_per_second  # Calculate offline income
state['funds'] += offline_earnings  # Add offline income to funds

showing_offline_popup = offline_seconds > 0  # Flag to control popup visibility
offline_popup_close_button = None  # Will hold close button rect

# -------- Timers for Passive Income & Auto-Save --------
last_tick = time.time()  # Last time passive income was added
last_save = time.time()  # Last time game state was auto-saved

# -------- Screen Manager --------
current_screen = "menu"  # Track current active screen: 'menu', 'game', or 'achievements'

# -------- Main Game Loop --------
running = True  # Game loop control flag
while running:
    now = time.time()  # Current time this frame

    # Passive income and auto-save only on game screen, and when popup is dismissed
    if current_screen == "game" and not showing_offline_popup:
        if now - last_tick >= 1:  # Add funds every second
            state['funds'] += state['funds_per_second']
            check_achievements(state, achievements)  # Check for new achievements
            last_tick = now

        if now - last_save >= 30:  # Auto-save every 30 seconds
            save_game(state['funds'], state['funds_per_second'], state['upgrades'], achievements)
            last_save = now

    # -------- Handle Events --------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Quit event (window close)
            save_game(state['funds'], state['funds_per_second'], state['upgrades'], achievements)
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Handle left click
            pos = event.pos  # Get mouse position

            # If popup is shown, only handle popup close button
            if showing_offline_popup and offline_popup_close_button:
                if offline_popup_close_button.collidepoint(pos):
                    showing_offline_popup = False  # Close popup
            elif not showing_offline_popup:
                buttons = get_button_rects()  # Get clickable button rectangles

                # Handle Main Menu buttons
                if current_screen == "menu":
                    if buttons.get("Start Game") and buttons["Start Game"].collidepoint(pos):
                        current_screen = "game"  # Switch to game screen
                    elif buttons.get("Achievements") and buttons["Achievements"].collidepoint(pos):
                        current_screen = "achievements"  # Switch to achievements screen
                    elif buttons.get("Exit") and buttons["Exit"].collidepoint(pos):
                        save_game(state['funds'], state['funds_per_second'], state['upgrades'], achievements)
                        running = False  # Exit game

                # Handle Game Screen buttons
                elif current_screen == "game":
                    if buttons.get("Back to Menu") and buttons["Back to Menu"].collidepoint(pos):
                        current_screen = "menu"  # Return to menu
                    else:
                        # Handle upgrade purchases
                        for name in state['upgrades']:
                            if buttons.get(name) and buttons[name].collidepoint(pos):
                                try_purchase(name, state)  # Attempt to purchase upgrade

                # Handle Achievements Screen buttons
                elif current_screen == "achievements":
                    if buttons.get("Back to Menu") and buttons["Back to Menu"].collidepoint(pos):
                        current_screen = "menu"  # Return to menu

    # -------- Draw Current Screen --------
    if current_screen == "menu":
        draw_menu(screen)  # Draw Main Menu
    elif current_screen == "game":
        draw_ui(screen, state, state['upgrades'], achievements)  # Draw Game UI
    elif current_screen == "achievements":
        draw_achievements_screen(screen, achievements)  # Draw Achievements Screen

    # Draw offline earnings popup (always on top if active)
    if showing_offline_popup:
        offline_popup_close_button = draw_offline_popup(screen, offline_earnings, offline_seconds)
    else:
        offline_popup_close_button = None

    # -------- Update Display --------
    pygame.display.flip()  # Update the window with everything drawn
    clock.tick(60)  # Limit frame rate to 60 FPS

# -------- Clean Exit --------
pygame.quit()  # Quit Pygame safely
sys.exit()     # Exit the program cleanly
