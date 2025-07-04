# ui.py
# By: NathanGr33n
# Updated: July 2025
# Handles all drawing and rendering in the Pygame window, including Main Menu, Game UI, Achievements screen, and the offline earnings popup.

import pygame
import math  # For animated glow effects
from config import (WIDTH, HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT, PADDING,
                    MARGIN_TOP, BG_COLOR, BUTTON_COLOR, TEXT_COLOR,
                    BORDER_COLOR, FONT_SIZE, GLOW_COLOR)

# Dictionary to store all clickable button rectangles (used for click detection)
button_rects = {}

def draw_text(surface, text, x, y, color=TEXT_COLOR):
    """Draw a line of text onto the screen at position (x, y)."""
    font = pygame.font.SysFont(None, FONT_SIZE)  # Create the font (safe after pygame.init())
    label = font.render(text, True, color)  # Render text onto surface
    surface.blit(label, (x, y))  # Draw text onto the screen

def draw_ui(screen, state, upgrades, achievements):
    """Draws the in-game UI, including funds, upgrade buttons, achievements, and back button."""
    screen.fill(BG_COLOR)  # Clear screen with background color

    # Draw player's current funds and income per second
    draw_text(screen, f"Funds: ${int(state['funds'])}", 30, 20)
    draw_text(screen, f"Funds/sec: {state['funds_per_second']}", 30, 50)

    # Animate a glowing background behind upgrade buttons (using sine wave for glow effect)
    tick = pygame.time.get_ticks() / 1000.0  # Time in seconds
    glow_alpha = int(80 + 50 * math.sin(tick * 2))  # Alpha value oscillates smoothly

    y = MARGIN_TOP  # Starting y-coordinate for upgrade buttons
    button_rects.clear()  # Clear previous button rects before redrawing

    for name, data in upgrades.items():
        rect = pygame.Rect(30, y, BUTTON_WIDTH, BUTTON_HEIGHT)  # Button position and size
        button_rects[name] = rect  # Store rect for click detection

        # Draw animated glowing background
        glow = pygame.Surface((BUTTON_WIDTH, BUTTON_HEIGHT), pygame.SRCALPHA)
        glow.fill((*GLOW_COLOR, glow_alpha))  # Semi-transparent glow color
        screen.blit(glow, rect.topleft)

        # Draw button background and border
        pygame.draw.rect(screen, BUTTON_COLOR, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 2)

        # Draw button label showing upgrade details
        label = f"{name}: {data['owned']} owned | +{data['cps']} cps | Cost: ${data['cost']}"
        draw_text(screen, label, rect.x + 10, rect.y + 18)

        y += BUTTON_HEIGHT + PADDING  # Move down for next button

    # Draw "Back to Menu" button at the bottom of the screen
    back_rect = pygame.Rect(30, HEIGHT - 70, BUTTON_WIDTH, BUTTON_HEIGHT)
    button_rects["Back to Menu"] = back_rect
    pygame.draw.rect(screen, BUTTON_COLOR, back_rect)
    pygame.draw.rect(screen, BORDER_COLOR, back_rect, 2)
    draw_text(screen, "Back to Menu", back_rect.x + 15, back_rect.y + 18)

    # Display unlocked achievements on the right side
    draw_text(screen, "Achievements Unlocked:", WIDTH - 320, 20)
    y2 = 50
    for name, data in achievements.items():
        if data["unlocked"]:
            draw_text(screen, f"\u2714 {name}", WIDTH - 320, y2)  # ✔ symbol for unlocked
            y2 += 25

def draw_menu(screen):
    """Draw the Main Menu screen with Start, Achievements, and Exit buttons."""
    screen.fill((15, 15, 15))  # Dark background for menu

    # Draw title
    draw_text(screen, "Idle Game Main Menu", WIDTH // 2 - 140, 100)

    # "Start Game" button
    start_rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, 200, BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(screen, BUTTON_COLOR, start_rect)
    pygame.draw.rect(screen, BORDER_COLOR, start_rect, 2)
    draw_text(screen, "Start Game", start_rect.x + 15, start_rect.y + 18)
    button_rects["Start Game"] = start_rect

    # "Achievements" button
    achievements_rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, 280, BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(screen, BUTTON_COLOR, achievements_rect)
    pygame.draw.rect(screen, BORDER_COLOR, achievements_rect, 2)
    draw_text(screen, "Achievements", achievements_rect.x + 15, achievements_rect.y + 18)
    button_rects["Achievements"] = achievements_rect
    
    # "Toggle Theme" button
    theme_rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, 440, BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(screen, BUTTON_COLOR, theme_rect)
    pygame.draw.rect(screen, BORDER_COLOR, theme_rect, 2)
    draw_text(screen, "Toggle Theme", theme_rect.x + 15, theme_rect.y + 18)
    button_rects["Toggle Theme"] = theme_rect

    # "Exit" button
    exit_rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, 360, BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(screen, BUTTON_COLOR, exit_rect)
    pygame.draw.rect(screen, BORDER_COLOR, exit_rect, 2)
    draw_text(screen, "Exit", exit_rect.x + 15, exit_rect.y + 18)
    button_rects["Exit"] = exit_rect

def draw_achievements_screen(screen, achievements):
    """Draws the Achievements screen showing all achievements with status and description."""
    screen.fill((25, 25, 25))  # Darker background for achievements screen

    # Draw title
    draw_text(screen, "Achievements", WIDTH // 2 - 100, 40)

    # Display all achievements with their status and descriptions
    y = 100
    for name, data in achievements.items():
        # Checkmark if unlocked, lock icon otherwise
        status = "\u2714" if data["unlocked"] else "\U0001F512"  # ✔ or 🔒
        draw_text(screen, f"{status} {name}", 50, y)  # Achievement name with status icon
        y += 30
        draw_text(screen, data["description"], 70, y)  # Description indented below
        y += 40  # Spacing between achievements

    # Draw "Back to Menu" button at bottom
    back_rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT - 80, BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(screen, BUTTON_COLOR, back_rect)
    pygame.draw.rect(screen, BORDER_COLOR, back_rect, 2)
    draw_text(screen, "Back to Menu", back_rect.x + 15, back_rect.y + 18)
    button_rects["Back to Menu"] = back_rect

def draw_offline_popup(screen, offline_earnings, offline_seconds):
    """Draws a popup window showing offline earnings with a Close button."""
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)  # Transparent overlay
    overlay.fill((0, 0, 0, 180))  # Semi-transparent black
    screen.blit(overlay, (0, 0))

    # Define popup dimensions and center it
    popup_width = 500
    popup_height = 200
    popup_rect = pygame.Rect(
        (WIDTH - popup_width) // 2,
        (HEIGHT - popup_height) // 2,
        popup_width,
        popup_height
    )

    # Draw popup background and border
    pygame.draw.rect(screen, BUTTON_COLOR, popup_rect)
    pygame.draw.rect(screen, BORDER_COLOR, popup_rect, 3)

    # Draw popup text lines
    lines = [
        "Welcome Back!",
        f"You earned ${offline_earnings} while offline",
        f"for {offline_seconds} seconds."
    ]
    y = popup_rect.y + 20
    for line in lines:
        draw_text(screen, line, popup_rect.x + 20, y)
        y += 40

    # Draw "Close" button inside popup
    close_rect = pygame.Rect(popup_rect.centerx - 60, popup_rect.bottom - 50, 120, 40)
    pygame.draw.rect(screen, BUTTON_COLOR, close_rect)
    pygame.draw.rect(screen, BORDER_COLOR, close_rect, 2)
    draw_text(screen, "Close", close_rect.x + 30, close_rect.y + 10)

    return close_rect  # Return close button rect for click detection

def get_button_rects():
    """Returns the latest button rectangles for click detection."""
    return button_rects
