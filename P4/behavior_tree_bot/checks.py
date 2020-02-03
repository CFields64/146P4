import logging, traceback, sys, os, inspect

def if_neutral_planet_available(state):
    return any(state.neutral_planets())

def low_planets_check(state):
    return len(state.my_planets()) <= 5

def have_most_planets(state):
    return len(state.my_planets()) > len(state.enemy_planets())

def have_least_planets(state):
    return len(state.my_planets()) < len(state.enemy_planets())

def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())

def have_smallest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           < sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())
