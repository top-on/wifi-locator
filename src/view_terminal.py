"""View functions that provide user interaction via terminal."""

import os
import sys

from core_wifi_locator import evaluate_all_models, locations, log_location, \
    predict_current_location


def main_menu():
    """Main menu for user interaction."""
    clear_screen()
    print("WIFI-LOCATOR MAIN MENU.\n")
    for key in sorted(menu_actions.keys()):
        print('%s: %s' % (key, menu_actions[key][0]))
    choice = input('\nChoose an option: ')
    if choice not in menu_actions.keys():
        print('\nPlease choose from the list of options.')
    else:
        # call functions in menu_actions
        clear_screen()
        print('Chosen action: %s.\n' % menu_actions[choice][0])
        menu_actions[choice][1]()
    # return to main menu
    print('\nHit ENTER to return to main menu.')
    input()
    main_menu()


def clear_screen():
    """Clear terminal screen, before printing more."""
    operating_system = os.name
    if operating_system == 'nt':
        os.system('CLS')
    if operating_system == 'posix':
        os.system('clear')


def get_and_log_location():
    """Get location from user and trigger logging for training."""
    print('Where are you currently located? \n')
    for i in range(0, len(locations)):
        print("%i - %s" % (i, locations[i]))
    choice = int(input('\nCurrent location: '))
    location = locations[choice]
    print('Logging location "%s" ... ' % location)
    log_location(location)


menu_actions = {'1': ['Log current location', get_and_log_location],
                '2': ['Evaluate classification accuracy', evaluate_all_models],
                '3': ['Predict current location', predict_current_location],
                '0': ['Exit', sys.exit],
                }


if __name__ == '__main__':
    """User interaction via terminal."""
    main_menu()
