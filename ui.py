# ui.py
# By: NathanGr33n
# June 22, 2025
# Handles all drawing and rendering in the Pygame window

import pygame
from config import (WIDTH, HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT, PADDING,
                    MARGIN_TOP, BG_COLOR, BUTTON_COLOR, TEXT_COLOR, BORDER_COLOR, FONT_SIZE)

# Load font globally
#font = pygame.font.SysFont(None, FONT_SIZE)

# Dictionary to hold clickable upgrade buttons
button_rects = {}

def draw_text(surface, text, x, y, color=TEXT_COLOR):
    """Draw a line of text to the screen."""
    font = pygame.font.SysFont(None, FONT_SIZE)  # Now initialized at runtime
    label = font.render(text, True, color)
    surface.blit(label, (x, y))

def draw_ui(screen, state, upgrades, achievements):
    """Render the full game UI, including funds, buttons, and achievements."""
    screen.fill(BG_COLOR)  # Fill background

    # Display funds and income
    draw_text(screen, f"Funds: ${int(state['funds'])}", 30, 20)
    draw_text(screen, f"Funds/sec: {state['funds_per_second']}", 30, 50)

    # Draw upgrade buttons
    y = MARGIN_TOP
    button_rects.clear()
    for name, data in upgrades.items():
        rect = pygame.Rect(30, y, BUTTON_WIDTH, BUTTON_HEIGHT)
        button_rects[name] = rect
        pygame.draw.rect(screen, BUTTON_COLOR, rect)               # Button background
        pygame.draw.rect(screen, BORDER_COLOR, rect, 2)           # Button border
        label = f"{name}: {data['owned']} owned | +{data['cps']} cps | Cost: ${data['cost']}"
        draw_text(screen, label, rect.x + 10, rect.y + 18)
        y += BUTTON_HEIGHT + PADDING

    # Draw unlocked achievements on the right
    draw_text(screen, "Achievements Unlocked:", WIDTH - 320, 20)
    y2 = 50
    for name, data in achievements.items():
        if data["unlocked"]:
            draw_text(screen, f"\u2714 {name}", WIDTH - 320, y2)  # Checkmark + name
            y2 += 25

def get_button_rects():
    """Return the latest button positions for click detection."""
    return button_rects
