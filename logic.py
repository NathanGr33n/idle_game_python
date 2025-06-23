# logic.py
# By: Nathan Green
# June 22, 2025
# Core gameplay logic including purchases and achievement checks

def try_purchase(name, state):
    """
    Attempt to purchase an upgrade. Modifies the state dict.
    state = {
        'funds': int,
        'funds_per_second': int,
        'upgrades': upgrades dict
    }
    """
    item = state['upgrades'][name]
    if state['funds'] >= item['cost']:
        state['funds'] -= item['cost']                      # Deduct cost from funds
        item['owned'] += 1                                  # Increase count
        state['funds_per_second'] += item['cps']            # Increase income rate
        item['cost'] = int(item['cost'] * 1.125)            # Raise cost for future purchases
        return True
    return False

def check_achievements(state, achievements):
    """Iterate through achievements and unlock any that qualify."""
    for name, data in achievements.items():
        if not data['unlocked'] and data['condition'](state):
            data['unlocked'] = True
            print(f"Achievement Unlocked: {name} - {data['description']}")
