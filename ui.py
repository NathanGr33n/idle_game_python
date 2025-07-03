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
    
def draw_offline_popup(screen, offline_earnings, offline_seconds):
    """Draws an in-game popup showing offline earnings with a Close button."""

    # Create a semi-transparent overlay that darkens the entire screen
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)  # Enable transparency
    overlay.fill((0, 0, 0, 180))  # Semi-transparent black (alpha 180 for 70% opacity)
    screen.blit(overlay, (0, 0))  # Draw the overlay on the screen

    # Define popup window dimensions and center it on the screen
    popup_width = 500
    popup_height = 200
    popup_rect = pygame.Rect(
        (WIDTH - popup_width) // 2,  # Center horizontally
        (HEIGHT - popup_height) // 2,  # Center vertically
        popup_width,
        popup_height
    )

    # Draw the popup background and border
    pygame.draw.rect(screen, BUTTON_COLOR, popup_rect)  # Popup background
    pygame.draw.rect(screen, BORDER_COLOR, popup_rect, 3)  # Popup border with 3px thickness

    # Prepare text lines to display inside the popup
    lines = [
        "Welcome Back!",
        f"You earned ${offline_earnings} while offline",
        f"for {offline_seconds} seconds."
    ]

    # Draw text lines inside the popup with vertical spacing
    y = popup_rect.y + 20  # Starting y position inside popup
    for line in lines:
        draw_text(screen, line, popup_rect.x + 20, y)  # Draw each line
        y += 40  # Move down for next line

    # Define the "Close" button inside the popup
    close_rect = pygame.Rect(
        popup_rect.centerx - 60,  # Center horizontally inside popup
        popup_rect.bottom - 50,   # Near the bottom of popup
        120,                      # Button width
        40                        # Button height
    )

    # Draw the Close button background and border
    pygame.draw.rect(screen, BUTTON_COLOR, close_rect)
    pygame.draw.rect(screen, BORDER_COLOR, close_rect, 2)

    # Draw the text on the Close button
    draw_text(screen, "Close", close_rect.x + 30, close_rect.y + 10)

    # Return the Close button rectangle for click detection in main.py
    return close_rect