# state.py
# By: NathanGr33n
# Updated: July 2025
# Handles saving and loading game state to and from a file, now with passive offline income support.

import json  # For saving and loading JSON files
import os    # To check file existence
import time  # For handling timestamps
from config import SAVE_FILE  # Save file path from config

def save_game(funds, funds_per_second, upgrades, achievements):
    """Save the entire game state to a file, including last played timestamp."""
    data = {
        "funds": funds,  # Player's total funds
        "funds_per_second": funds_per_second,  # Passive income rate
        "upgrades": upgrades,  # Upgrade data (cost, cps, owned)
        "achievements": {k: v["unlocked"] for k, v in achievements.items()},  # Achievement states
        "last_played": time.time()  # Current timestamp for offline income calculation
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)  # Write data to save file with pretty formatting
    print("Game saved.")  # Console confirmation

def load_game(default_upgrades, default_achievements):
    """
    Load game state from save file, merge into current data, 
    and return funds, funds_per_second, and last_played timestamp.
    """
    if os.path.exists(SAVE_FILE):  # Check if save file exists
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)  # Load JSON data

            # Load funds and income rate
            funds = data.get("funds", 0)
            funds_per_second = data.get("funds_per_second", 1)

            # Load upgrades and merge with defaults
            saved_upgrades = data.get("upgrades", {})
            for name in default_upgrades:
                if name in saved_upgrades:
                    default_upgrades[name].update(saved_upgrades[name])

            # Load achievements and merge with defaults
            saved_achievements = data.get("achievements", {})
            for name in default_achievements:
                default_achievements[name]["unlocked"] = saved_achievements.get(name, False)

            # Load last played timestamp (default to now if missing)
            last_played = data.get("last_played", time.time())

            print("Game loaded.")  # Console confirmation
            return funds, funds_per_second, last_played  # Return state inclu_
