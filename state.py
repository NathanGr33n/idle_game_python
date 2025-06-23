# state.py
# By: NathanGr33n
# June 22, 2025
# Handles saving and loading game state to and from a file

import json
import os
from config import SAVE_FILE

def save_game(funds, funds_per_second, upgrades, achievements):
    """Save game state to a file."""
    data = {
        "funds": funds,
        "funds_per_second": funds_per_second,
        "upgrades": upgrades,
        "achievements": {k: v["unlocked"] for k, v in achievements.items()}
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print("Game saved.")

def load_game(default_upgrades, default_achievements):
    """Load game state from file and merge into current data."""
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)

            funds = data.get("funds", 0)
            funds_per_second = data.get("funds_per_second", 1)

            saved_upgrades = data.get("upgrades", {})
            for name in default_upgrades:
                if name in saved_upgrades:
                    default_upgrades[name].update(saved_upgrades[name])

            saved_achievements = data.get("achievements", {})
            for name in default_achievements:
                default_achievements[name]["unlocked"] = saved_achievements.get(name, False)

            print("Game loaded.")
            return funds, funds_per_second

    print("No save file found. Starting new game.")
    return 0, 1
