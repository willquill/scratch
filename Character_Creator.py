# CONTENTS
# - greeting
# - choose a race
# - choose a class
# - roll stats

### Define functions
def detect_race():

    # Create array/list of all possible races
    all_races = ['Halfling', 'Dwarf', 'Triton', 'Tiefling', 'Elf', 'Goliath', 'Human']

    # Loop through each race in the all_races array to find the one that matches the number
    # The array starts at 0 and has 7 items, so the index values are between 0 and 6
    # i.e. Halfling is 0, Dwarf is 1, Human is 6.
    # For each item in the all_races list, where the first item starts at 0
    for race in all_races:
        # If the entered number minus 1 is equal to the index value 
        if int(choice) - 1 == all_races.index(race):
            # Then set the player_race to that item in the index
            player_race = race
            print('You chose:', player_race)
            # Then break out of the function with a "return"
            # Without including this return, it will continue to loop through all races!
            # And then your output would look like this:
            #    Enter the number of your choice: 1
            #    Sorry, that is not one of the options.
            #    Sorry, that is not one of the options.
            #    Sorry, that is not one of the options.
            #    Sorry, that is not one of the options.
            #    Sorry, that is not one of the options.
            #    Sorry, that is not one of the options.
            #    You chose: Halfling
            return
        else:
            # This gets hit if the choice-1 doesn't match an item in the index
            # For example, user enters 8. 8-1=7, but the items only go from 0-6 (Halfling to Human)
            print('Sorry, that is not one of the options.')    

def roll_stat():
    rolls = [randint(1, 6), randint(1, 6), randint(1, 6), randint(1, 6)]
    print('You rolled:', rolls)
    rolls.sort()
    rolls.pop(0)
    print('Removing the lowest roll leaves us with:', rolls)
    roll = rolls[0] + rolls[1] + rolls[2]
    print('Adding those gives us a total of:', roll)
    stats.append(roll)
    if len(stats) < 6:
        print('So far, your stat rolls are:', stats)
    elif len(stats) == 6:
        print('Great! Your final stat rolls are:', stats)


### Start main script

# GREETING
print('Hello! Welcome to the character generator for the Seven Shards of Vaelith-Tir.')
input()

# CHOOSE A RACE
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

# Execute detect_race function
detect_race()

input()

# CHOOSE A CLASS

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

input()

print('Okay, great! You are a ' + player_race, player_class + '!')

input()

# FUNCTION FOR ROLLING STATS

from random import randint

stats = []


# ROLL STATS

print('Now, let\'s roll your ability scores. You will roll six times, and then assign each of the six scores to an ability.')

print('Press ENTER to roll your first stat.')
input()
roll_stat()

print('Press ENTER to roll your second stat.')
input()
roll_stat()

print('Press ENTER to roll your third stat.')
input()
roll_stat()

print('Press ENTER to roll your fourth stat.')
input()
roll_stat()

print('Press ENTER to roll your fifth stat.')
input()
roll_stat()

print('Press ENTER to roll your sixth and final stat.')
input()
roll_stat()

input()

print('Now, let\'s assign these scores to your abilities.')

choice = input('Which score would you like to assign to STRENGTH? ')

if int(choice) in stats:
    strength = int(choice)
    stats.remove(int(choice))
    print('You chose ' + choice + '. Your STRENGTH score is now ' + choice + ' and your remaining options are', stats)

choice = input('Which score would you like to assign to DEXTERITY? ')

if int(choice) in stats:
    dexterity = int(choice)
    stats.remove(int(choice))
    print('You chose ' + choice + '. Your DEXTERITY score is now ' + choice + ' and your remaining options are', stats)

choice = input('Which score would you like to assign to CONSTITUTION? ')

if int(choice) in stats:
    constitution = int(choice)
    stats.remove(int(choice))
    print('You chose ' + choice + '. Your CONSTITUTION score is now ' + choice + ' and your remaining options are', stats)

choice = input('Which score would you like to assign to WISDOM? ')

if int(choice) in stats:
    wisdom = int(choice)
    stats.remove(int(choice))
    print('You chose ' + choice + '. Your WISDOM score is now ' + choice + ' and your remaining options are', stats)

choice = input('Which score would you like to assign to INTELLIGENCE? ')

if int(choice) in stats:
    intelligence = int(choice)
    stats.remove(int(choice))
    charisma = stats[0]
    print('You chose ' + choice + '. Your INTELLIGENCE score is now ' + choice + ', and your CHARISMA score is ' + str(stats[0]) +'.')

input()

print('Alright! Here\'s how you assigned your scores:')
print('STRENGTH:', strength)
print('DEXTERITY:', dexterity)
print('CONSTITUTION:', constitution)
print('WISDOM:', wisdom)
print('INTELLIGENCE', intelligence)
print('CHARISMA', charisma)

input()











