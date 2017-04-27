"""View functions that provide user interaction via terminal."""

import os
import sys
from time import sleep

from core_wifi_locator import log_location, evaluate_all_models, \
                              predict_current_location, stream_location, locations

                              
def main_menu():
    clear_screen()
    print("WIFI-LOCATOR MAIN MENU.\n")
    for key in menu_actions.keys():
        print('%s: %s' % (key, menu_actions[key][0]))
    choice = input('\nChoose an option: ')
    
    if choice not in menu_actions.keys():
        print('Please choose from the list of options.')
    else:
        # call functions in menu_actions
        clear_screen()
        print('Chosen action: %s.\n' % menu_actions[choice][0])
        menu_actions[choice][1]()
    # unless executed 'sys.exit()', return to main menu
    print('\nHit ENTER to return to main menu.')
    input()    
    main_menu()
    
def clear_screen():
    operating_system = os.name
    if operating_system == 'nt':
        os.system('CLS')
    if operating_system == 'posix':
        os.system('clear')
    
def get_and_log_location():
    """Get location from user (options in script parameters) and trigger logging.""" 
    print('Where are you currently located? \n')
    for i in range(0, len(locations)):
        print("%i - %s" % (i, locations[i]))
    choice = int(input('\nCurrent location: '))
    location = locations[choice]
    print('Logging location "%s" ... ' % location)
    sleep(2)
    log_location(location)

    
menu_actions = {'1': ['Log current location', get_and_log_location],
                '2': ['Evaluate classification accuracy', evaluate_all_models],
                '0': ['Exit', sys.exit],
                }

        
if __name__ == '__main__':
    """User interaction via terminal."""
    main_menu()
        