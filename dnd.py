#################################################
# First, declare the functions we will use
#################################################

def main():

    print('Hello! Welcome the character generator for the Seven Shards of Vaelith-Tir.')

# CHOOSE A RACE
def playerrace():
    
    input()
    print('''First, let's choose a race:

    1. Halfling
    2. Dwarf
    3. Triton
    4. Tiefling
    5. Elf
    6. Goliath
    7. Human
    ''')

    choice = input('Enter the number of your choice: ')

    player_race = ''

    if int(choice) == 1:
        player_race = 'Halfling'
    elif int(choice) == 2:
        player_race = "Dwarf"
    elif int(choice) == 3:
        player_race = "Triton"
    elif int(choice) == 4:
        player_race = "Tiefling"
    elif int(choice) == 5:
        player_race = "Elf"
    elif int(choice) == 6:
        player_race = "Goliath"
    elif int(choice) == 7:
        player_race = "Human"
    else:
        print('Sorry, that is not one of the options.')

    print('You chose:', player_race)

# CHOOSE A CLASS
def playerclass():
    input()

    print('''Now, let's choose a class:

    1. Barbarian
    2. Bard
    3. Cleric
    4. Druid
    5. Fighter
    6. Monk
    7. Paladin
    8. Ranger
    9. Rogue
    10. Sorcerer
    11. Warlock
    12. Wizard
    ''')

    choice = input('Enter the number of your choice: ')

    classes = ['Barbarian', 'Bard', 'Cleric', 'Druid', 'Fighter', 'Monk', 'Paladin', 'Ranger', 'Rogue', 'Sorcerer', 'Warlock', 'Wizard']

    player_class = classes[int(choice) - 1]

    print('You chose:', player_class)

#################################################
# Start the actual Python code
#################################################

# Set variables to empty strings
player_race = ''
player_class = ''

# Run the main function, which just prints a welcome message
main()

# Run the race function
playerrace()

# Run the class function
playerclass()

# If player_race is still empty, re-run the function.
if player_race == '':
    playerrace()
# Otherwise, if player_class is still empty, re-run the function.
elif player_class == '':
    playerclass()
# Otherwise, print the message
else:
    print('Okay, great! You are a ' + player_race, player_class + '!')
