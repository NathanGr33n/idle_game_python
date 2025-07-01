# idle_game_python
By: NathanGr33n
=========================================================================================================================================
An idle/incremental game built using Python and Pygame where the player earns money passively and can purchase various upgrades
to increase income over time. The game also includes achievements, animated GUI, save/load functionality, and a modular code structure.
=========================================================================================================================================
Features:
	- Clickable Upgrade Buttons
	- Passive Income Per Second
	- Achievements with Conditions and Notifications
	- Save/Load progress using JSON
	- Auto-Save every 30secs
	- Animated Glow Effects for Upgrade Buttons
	- Fully Modular Design with Cleanly Separated Files
=========================================================================================================================================
Project Structure:

idle_game/
├── config.py        # UI layout, colors, dimensions, and constants
├── data.py          # Upgrade and achievement definitions
├── logic.py         # Game logic: purchase handling and achievement checks
├── state.py         # Save/load game data to JSON
├── ui.py            # Drawing upgrade buttons, achievements, and text
├── main.py          # Game initialization, loop, and event handling
└── idle_save.json   # Automatically created save file (generated at runtime)
=========================================================================================================================================
Requirements:
	- Python 3.8+
	- Pygame (Install -> pip install pygame)
=========================================================================================================================================
Built by NathanGr33n using Python and Pygame. Contributions and suggestions welcome!

Pygame: https://www.pygame.org/