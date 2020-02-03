#!/usr/bin/env python
#

"""
// There is already a basic strategy in place here. You can use it as a
// starting point, or you can throw it out entirely and replace it with your
// own.
"""
import logging, traceback, sys, os, inspect
logging.basicConfig(filename=__file__[:-3] +'.log', filemode='w', level=logging.DEBUG)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from behavior_tree_bot.behaviors import *
from behavior_tree_bot.checks import *
from behavior_tree_bot.bt_nodes import Selector, Sequence, Action, Check

from planet_wars import PlanetWars, finish_turn

# You have to improve this tree or create an entire new one that is capable
# of winning against all the 5 opponent bots
def setup_behavior_tree():
    logging.info('Setting Up Behavior Tree')
    # Top-down construction of behavior tree
    root = Selector(name='High Level Ordering of Strategies')
    logging.info('Root Defined')

    play_offensively = Sequence(name='Offensive Tactics')
    winning_check = Check(have_most_planets)
    play_defensively = Sequence(name='Defensive Tactics')
    losing_check = Check(have_least_planets)
    logging.info('Offensive - Defensive Check Defined')

    early_occupy = Sequence(name='Early Occupation of Neutrals')
    owned_planets_check = Check(low_planets_check)
    occupy = Action(occupy_nearest_neutral_planet)
    early_occupy.child_nodes = [owned_planets_check, occupy]
    logging.info('Occupation Strategy Defined')

    offensive_plan = Sequence(name='Offensive Strategy')
    largest_fleet_check = Check(have_largest_fleet)
    attack = Action(attack_weakest_enemy_planet)
    offensive_plan.child_nodes = [largest_fleet_check, attack]
    logging.info('Offensive Strategy Defined')

    spread_sequence = Sequence(name='Spread Strategy')
    neutral_planet_check = Check(if_neutral_planet_available)
    spread_action = Action(spread_to_weakest_neutral_planet)
    spread_sequence.child_nodes = [neutral_planet_check, spread_action]
    logging.info('Spread Sequence Defined')

    defensive_plan = Sequence(name='Defensive Strategy')
    smallest_fleet_check = Check(have_smallest_fleet)
    reinforce = Action(reinforce_weakest_planet)
    defensive_plan.child_nodes = [smallest_fleet_check, reinforce]
    logging.info('Defensive Strategy Defined')

    play_offensively.child_nodes = [winning_check, early_occupy, offensive_plan, spread_sequence]
    play_defensively.child_nodes = [losing_check, early_occupy, defensive_plan, spread_sequence]

    root.child_nodes = [play_offensively, play_defensively, occupy.copy()]
    logging.info('Children Assigned')

    logging.info('\n' + root.tree_to_string())
    return root

# You don't need to change this function
def do_turn(state):
    behavior_tree.execute(planet_wars)

if __name__ == '__main__':
    logging.basicConfig(filename=__file__[:-3] + '.log', filemode='w', level=logging.DEBUG)

    logging.info('Setting Up Behavior Tree')
    behavior_tree = setup_behavior_tree()
    try:
        map_data = ''
        while True:
            current_line = input()
            if len(current_line) >= 2 and current_line.startswith("go"):
                planet_wars = PlanetWars(map_data)
                do_turn(planet_wars)
                finish_turn()
                map_data = ''
            else:
                map_data += current_line + '\n'

    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
    except Exception:
        traceback.print_exc(file=sys.stdout)
        logging.exception("Error in bot.")
