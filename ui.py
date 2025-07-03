# ui.py
# By: NathanGr33n
# Updated: July 2025
# Handles all drawing and rendering in the Pygame window, including the main menu and game UI.

import pygame
import math  # Used for animated glow effects
from config import (WIDTH, HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT, PADDING,
                    MARGIN_TOP, BG_COLOR, BUTTON_COLOR, TEXT_COLOR,
                    BORDER_COLOR, FONT_SIZE, GLOW_COLOR)

# Dictionary to hold all clickable buttons (both in-game and menu)
button_rects = {}

def draw_text(surface, text, x, y, color=TEXT_COLOR):
    """Draw a line of text to the screen at (x, y) using the default font."""
    font = pygame.font.SysFont(None, FONT_SIZE)  # Runtime font creation (safe after pygame.init())
    label = font.render(text, True, color)
    surface.blit(label, (x, y))

def draw_ui(screen, state, upgrades, achievements):
    """Render the full in-game UI: funds, upgrades, achievements, and Back button."""
    screen.fill(BG_COLOR)  # Fill background

    # Show funds and passive income
    draw_text(screen, f"Funds: ${int(state['funds'])}", 30, 20)
    draw_text(screen, f"Funds/sec: {state['funds_per_second']}", 30, 50)

    # Animate button glow using a sine wave
    tick = pygame.time.get_ticks() / 1000.0
    glow_alpha = int(80 + 50 * math.sin(tick * 2))

    y = MARGIN_TOP
    button_rects.clear()  # Clear button rects before updating
    for name, data in upgrades.items():
        rect = pygame.Rect(30, y, BUTTON_WIDTH, BUTTON_HEIGHT)
        button_rects[name] = rect

        # Draw glowing background
        glow = pygame.Surface((BUTTON_WIDTH, BUTTON_HEIGHT), pygame.SRCALPHA)
        glow.fill((*GLOW_COLOR, glow_alpha))
        screen.blit(glow, rect.topleft)

        # Draw button background & border
        pygame.draw.rect(screen, BUTTON_COLOR, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 2)

        # Button label text
        label = f"{name}: {data['owned']} owned | +{data['cps']} cps | Cost: ${data['cost']}"
        draw_text(screen, label, rect.x + 10, rect.y + 18)

        y += BUTTON_HEIGHT + PADDING

    # Draw "Back to Menu" button at bottom of screen
    back_rect = pygame.Rect(30, HEIGHT - 70, BUTTON_WIDTH, BUTTON_HEIGHT)
    button_rects["Back to Menu"] = back_rect
    pygame.draw.rect(screen, BUTTON_COLOR, back_rect)
    pygame.draw.rect(screen, BORDER_COLOR, back_rect, 2)
    draw_text(screen, "Back to Menu", back_rect.x + 15, back_rect.y + 18)

    # Draw unlocked achievements on the right side
    draw_text(screen, "Achievements Unlocked:", WIDTH - 320, 20)
    y2 = 50
    for name, data in achievements.items():
        if data["unlocked"]:
            draw_text(screen, f"\u2714 {name}", WIDTH - 320, y2)  # ✔ + achievement name
            y2 += 25

def draw_menu(screen):
    """Draw the main menu screen with Start and Exit buttons."""
    screen.fill((15, 15, 15))  # Dark background for the menu

    # Draw menu title
    draw_text(screen, "Idle Game Main Menu", WIDTH // 2 - 140, 100)

    # "Start Game" button
    start_rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, 200, BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(screen, BUTTON_COLOR, start_rect)
    pygame.draw.rect(screen, BORDER_COLOR, start_rect, 2)
    draw_text(screen, "Start Game", start_rect.x + 15, start_rect.y + 18)
    button_rects["Start Game"] = start_rect

    # "Exit" button
    exit_rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, 280, BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(screen, BUTTON_COLOR, exit_rect)
    pygame.draw.rect(screen, BORDER_COLOR, exit_rect, 2)
    draw_text(screen, "Exit", exit_rect.x + 15, exit_rect.y + 18)
    button_rects["Exit"] = exit_rect

def get_button_rects():
    """Return the latest button rectangles for click detection."""
    return button_rects
