# main.py
# By: NathanGr33n
# Updated: July 2025
# Main entry point for the Idle Game with GUI, upgrades, save/load, achievements, and a main menu.


#Importing Libraries
import pygame
import time
import sys
from config import WIDTH, HEIGHT
from data import upgrades, achievements
from state import save_game, load_game
from logic import try_purchase, check_achievements
from ui import draw_ui, draw_menu, get_button_rects

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Idle Game GUI")
clock = pygame.time.Clock()

# Load saved game state
funds, funds_per_second = load_game(upgrades, achievements)
state = {
    'funds': funds,
    'funds_per_second': funds_per_second,
    'upgrades': upgrades
}

# Timers for income generation and auto-save
last_tick = time.time()
last_save = time.time()

# Track which screen is currently active ('menu' or 'game')
current_screen = "menu"

running = True

# Main Game Loop
while running:
    now = time.time()

    # Passive income and auto-saving only in the game screen
    if current_screen == "game":
        if now - last_tick >= 1:
            state['funds'] += state['funds_per_second']
            check_achievements(state, achievements)
            last_tick = now

        if now - last_save >= 30:
            save_game(state['funds'], state['funds_per_second'], upgrades, achievements)
            last_save = now

    # Handle events for both screens
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_game(state['funds'], state['funds_per_second'], upgrades, achievements)
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            buttons = get_button_rects()

            # Handle clicks in the main menu
            if current_screen == "menu":
                if buttons.get("Start Game") and buttons["Start Game"].collidepoint(pos):
                    current_screen = "game"
                elif buttons.get("Exit") and buttons["Exit"].collidepoint(pos):
                    save_game(state['funds'], state['funds_per_second'], upgrades, achievements)
                    running = False

            # Handle clicks in the game screen
            elif current_screen == "game":
                if buttons.get("Back to Menu") and buttons["Back to Menu"].collidepoint(pos):
                    current_screen = "menu"
                else:
                    # Check upgrade buttons
                    for name in upgrades:
                        if buttons.get(name) and buttons[name].collidepoint(pos):
                            try_purchase(name, state)

    # Render the appropriate screen
    if current_screen == "menu":
        draw_menu(screen)
    elif current_screen == "game":
        draw_ui(screen, state, upgrades, achievements)

    pygame.display.flip()
    clock.tick(60)

# Clean exit
pygame.quit()
sys.exit()
