from random import choices, randint

# CONTENTS
# - greeting
# - choose a race
# - choose a class
# - roll stats

### Define functions
def fancy(string):
    string = f"   {string}   "
    return f"\n{'*'*len(string)}\n{string}\n{'*'*len(string)}\n"

def make_selection(category):
      
    # Print choice list
    print(fancy(f"CHOOSE A {category['category_type'].upper()}"))
    for i in category['category_choices']:
        print(f"{str(category['category_choices'].index(i)+1)}. {i}")

    # Accept choice input and print result
    while True:
        try:
            choice_number = input('\nEnter the number of your choice: ')
            if choice_number == '0':
                raise IndexError("Choice doesn't exist! Try again.\n")
            else:
                selection = category['category_choices'][int(choice_number)-1]
                return selection;
        except IndexError:
            print("Choice doesn't exist! Try again.\n")
            continue

def roll_stat():
    
    # Determine suffix
    loop_number = len(stats)+1
    if loop_number == 1:
        suffix = 'st'
    elif loop_number == 2:
        suffix = 'nd'
    elif loop_number == 3:
        suffix = 'rd'
    else:
        suffix = 'th'
    
    print(f'Press ENTER to roll your {len(stats)+1}{suffix} stat.')
    input()
    rolls = [randint(1, 6), randint(1, 6), randint(1, 6), randint(1, 6)]
    print(f'You rolled: {rolls}')
    rolls.sort()
    rolls.pop(0)
    print(f'Removing the lowest roll leaves us with: {rolls}')
    roll = rolls[0] + rolls[1] + rolls[2]
    print(f'Adding those gives us a total of: {roll}')
    stats.append(roll)
    print(f'So far, your stat rolls are: {stats}\n')

#####
##### Start main script
#####

# GREETING
print(fancy('Hello! Welcome to the character generator for the Seven Shards of Vaelith-Tir.'))

# Define categories of choices to be made
categories = [
    {
        'category_type':'race',
        'category_choices':['Halfling', 'Dwarf', 'Triton', 'Tiefling', 'Elf', 'Goliath', 'Human']
    },
    {
        'category_type':'class',
        'category_choices':['Barbarian', 'Bard', 'Cleric', 'Druid', 'Fighter', 'Monk', 'Paladin', 'Ranger', 'Rogue', 'Sorcerer', 'Warlock', 'Wizard']
    }
]

# For each category, execute the make_selection function
# This will add a new key to each item in the categories array
for i in categories:
    i.update({'category_selection':make_selection(i)})


player_race = categories[0]["category_selection"]
player_class = categories[1]["category_selection"]

print(fancy(f"You chose a {player_race} {player_class}!"))


# Roll ability scores
print(fancy('ROLL ABILITY SCORES'))
print("You will roll six times, and then assign each of the six scores to an ability.\n")

stats = []
while len(stats) < 6:
    roll_stat()

print(f'Great! Your final stat rolls are: {stats}')



## Define abilities list
#abilities = ['strength', 'dexterity', 'constitution', 'wisdom', 'intelligence']
#
## Create empty abilities dict
#abilities_dict = {}
#
#for i in abilities:
#    # The stat number will increase with each iteration through the index, starting from 0 (+1)
#    loop_number = abilities.index(i)+1
#    if loop_number == 1:
#        suffix = 'st'
#    elif loop_number == 2:
#        suffix = 'nd'
#    elif loop_number == 3:
#        suffix = 'rd'
#    else:
#        suffix = 'th'
#    
#    input()
#    roll_stat()
#
#
#
#print('Now, let\'s assign these scores to your abilities.')
#
#choice = input('Which score would you like to assign to STRENGTH? ')
#
#if int(choice) in stats:
#    strength = int(choice)
#    stats.remove(int(choice))
#    print('You chose ' + choice + '. Your STRENGTH score is now ' + choice + ' and your remaining options are', stats)
#
#choice = input('Which score would you like to assign to DEXTERITY? ')
#
#if int(choice) in stats:
#    dexterity = int(choice)
#    stats.remove(int(choice))
#    print('You chose ' + choice + '. Your DEXTERITY score is now ' + choice + ' and your remaining options are', stats)
#
#choice = input('Which score would you like to assign to CONSTITUTION? ')
#
#if int(choice) in stats:
#    constitution = int(choice)
#    stats.remove(int(choice))
#    print('You chose ' + choice + '. Your CONSTITUTION score is now ' + choice + ' and your remaining options are', stats)
#
#choice = input('Which score would you like to assign to WISDOM? ')
#
#if int(choice) in stats:
#    wisdom = int(choice)
#    stats.remove(int(choice))
#    print('You chose ' + choice + '. Your WISDOM score is now ' + choice + ' and your remaining options are', stats)
#
#choice = input('Which score would you like to assign to INTELLIGENCE? ')
#
#if int(choice) in stats:
#    intelligence = int(choice)
#    stats.remove(int(choice))
#    charisma = stats[0]
#    print('You chose ' + choice + '. Your INTELLIGENCE score is now ' + choice + ', and your CHARISMA score is ' + str(stats[0]) +'.')
#
#input()
#
#print('Alright! Here\'s how you assigned your scores:')
#print('STRENGTH:', strength)
#print('DEXTERITY:', dexterity)
#print('CONSTITUTION:', constitution)
#print('WISDOM:', wisdom)
#print('INTELLIGENCE', intelligence)
#print('CHARISMA', charisma)
#
#input()
#
#
#
#
#
#