# data.py
# By: NathanGr33n
# June 22, 2025
# Contains the definitions for upgrades and achievements used in the idle game

# Dictionary defining available upgrades with cost, cps (currency/sec), and how many are owned
upgrades = {
    "Employment": {"cost": 25, "cps": 2, "owned": 0},
    "Treasury Bonds": {"cost": 100, "cps": 4, "owned": 0},
    "Certificates of Deposit (CD)": {"cost": 500, "cps": 6, "owned": 0},
    "Index Funds": {"cost": 1000, "cps": 9, "owned": 0},
    "eCommerce Business": {"cost": 2000, "cps": 15, "owned": 0},
    "Crypto": {"cost": 10000, "cps": 22, "owned": 0},
    "Real Estate": {"cost": 50000, "cps": 35, "owned": 0},
}

# Achievement system: each entry defines a description, condition, and unlock state
# Each condition is a lambda that accepts a state dictionary and returns True/False
achievements = {
    "First Hundred": {
        "description": "Earn your first $100!",
        "condition": lambda state: state['funds'] >= 100,
        "unlocked": False
    },
    "Investor": {
        "description": "Own 1 Index Fund",
        "condition": lambda state: state['upgrades']['Index Funds']['owned'] >= 1,
        "unlocked": False
    },
    "Tycoon": {
        "description": "Reach $10,000 total funds",
        "condition": lambda state: state['funds'] >= 10000,
        "unlocked": False
    },
    "Real Deal": {
        "description": "Own 1 Real Estate property",
        "condition": lambda state: state['upgrades']['Real Estate']['owned'] >= 1,
        "unlocked": False
    },
}
