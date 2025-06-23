# main.py
# By: NathanGr33n
# June 22, 2025
# Main entry point for the Idle Game with GUI, upgrades, save/load, achievements

import pygame
import time
import sys
from config import WIDTH, HEIGHT
from data import upgrades, achievements
from state import save_game, load_game
from logic import try_purchase, check_achievements
from ui import draw_ui, get_button_rects

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Idle Game GUI")
clock = pygame.time.Clock()

# Initialize game state
funds, funds_per_second = load_game(upgrades, achievements)
state = {
    'funds': funds,
    'funds_per_second': funds_per_second,
    'upgrades': upgrades
}

# Track time for income and auto-save
last_tick = time.time()
last_save = time.time()
running = True

# Game loop
while running:
    now = time.time()

    # Passive income every second
    if now - last_tick >= 1:
        state['funds'] += state['funds_per_second']
        check_achievements(state, achievements)
        last_tick = now

    # Auto-save every 30 seconds
    if now - last_save >= 30:
        save_game(state['funds'], state['funds_per_second'], upgrades, achievements)
        last_save = now

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_game(state['funds'], state['funds_per_second'], upgrades, achievements)
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            for name, rect in get_button_rects().items():
                if rect.collidepoint(pos):
                    try_purchase(name, state)

    # Render screen
    draw_ui(screen, state, upgrades, achievements)
    pygame.display.flip()
    clock.tick(60)

# Clean exit
pygame.quit()
sys.exit()
