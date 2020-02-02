import logging, traceback, sys, os, inspect
sys.path.insert(0, '../')
from planet_wars import issue_order
from math import inf, sqrt


def attack_weakest_enemy_planet(state):
    # (1) If we have too many active fleets, just do nothing.
    if len(state.my_fleets()) >= 3:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send enough ships to capture and occupy the planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)


def spread_to_weakest_neutral_planet(state):
    # (1) If we have too many active fleets, just do nothing.
    if len(state.my_fleets()) >= 3:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send enough ships to capture and occupy the planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)

def reinforce_weakest_planet(state):
    # (1) If we have too many active fleets, just do nothing.
    if len(state.my_fleets()) >= 3:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find my weakest planet.
    weakest_planet = min(state.my_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send one third of the ships from my strongest planet to reinforce my weakest planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 3)

def occupy_nearest_neutral_planet(state):
    logging.info('Occupying Nearest Neutral Planet.')
    # (1) If we have too many active fleets, just do nothing.
    if len(state.my_fleets()) >= 3:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find nearest neutral planet.
    base_x = strongest_planet.x
    base_y = strongest_planet.y

    nearest_neutral = None
    distance = inf

    for planet in state.neutral_planets():
        check_x = planet.x
        check_y = planet.y

        test_dist = sqrt(((check_x-base_x)**2) + ((check_y-base_y)**2))

        if test_dist < distance:
            distance = test_dist
            nearest_neutral = planet

    if not strongest_planet or not nearest_neutral:
        # No legal source or desitnation.
        return False
    else:
        # (4) Send enough ships to capture and occupy the planet.
        occupying_ships = max(strongest_planet.num_ships / 2, neutral_planet.num_ships + 10)
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, occupying_ships)
