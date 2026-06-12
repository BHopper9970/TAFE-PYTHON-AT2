'''
Program:     Contact Manager
Description: Creates and manages contacts using text files

Author:      Ben Hopper
Date:        24/05/2026
Version:     1.0
'''

'''
.cont file structure:
line 0: 'contact name'
line 1: 'phone number' (10 characters)
line 2: 'email'
line 3: 'attachment' (family or friend)
'''

import os
import glob
import readline


# Makes list of all cont files in the folder
cont_dir = './Contacts/'


# input with default text written by https://stackoverflow.com/users/56338/sth
def input_default(prompt, prefill=''):
    readline.set_startup_hook(lambda: readline.insert_text(prefill).strip())
    try:
        return input(prompt)  # or raw_input in Python 2
    finally:
      readline.set_startup_hook()


# clears the terminal window
def clear_term():
    print("\033[H\033[J", end="")


# prints the main UI options
def print_options():
    clear_term()
    print('''
Please choose an option:

a: add a contact or edit an existing contact
l: list all contacts
d: delete a contact
q: quit
    ''')


# runs specified option
def do_option(option):
    if option == 'a':
        add_or_edit_cont()
    elif option == 'l':
        list_conts()
    elif option == 'd':
        delete_cont()


# add cont to manager
def add_or_edit_cont():
    clear_term()

    #gets cont name
    print('(enter to exit)')
    cont_name = input('\nEnter contact name: ')
    lines = []

    # exit function
    if cont_name == '':
        print_options()
        return
    
    # if cont exists:
    elif os.path.isfile(f'{cont_dir}{cont_name}.cont'):
        files = glob.glob('Contacts/*.cont')
        while True:
            edit_or_add = input('do you want to edit the existing contact or add another? (a for add, e for edit) ')
            if edit_or_add == 'e':
                edit_cont(cont_name)
                break
            elif edit_or_add == 'a':
                if cont_name[-1].isdigit() and cont_name[-2] == '-':
                    while f'Contacts/{cont_name}.cont' in files:
                        cont_name = cont_name[:-1] + str(int(cont_name[-1]) + 1)
                    add_cont(cont_name)
                else:
                    cont_name = cont_name + '-1'
                    while f'Contacts/{cont_name}.cont' in files:
                        cont_name = cont_name[:-1] + str(int(cont_name[-1]) + 1)
                    add_cont(cont_name)
                break
            else:
                print('Error: invalid option')
                

    # if cont doesn't exist:
    else:
        add_cont(cont_name)

def add_cont(cont_name):
    print(f'\nCreating contact: {cont_name}')
    lines = []

    # sets cont name
    lines.append(cont_name)

    # sets cont phone number
    print('''
Enter the phone number of the contact:
    ''')
    
    while True:
        phone_number = input('Phone number: ')

        # checks if phone number is a number
        try:
            tryint = int(phone_number)
        except:
            print('Error: not a number')
            continue

        # checks if phone number is too short, too long or correct length
        if phone_number == '':
            lines.append('number: ')
            break
        elif len(phone_number) < 10:
            print('Error: phone number too short')
            continue
        elif len(phone_number) == 10:
            lines.append(f'number: {phone_number}')
            break
        elif len(phone_number) > 10:
            print('Error: phone number too long')
            continue
        else:
            print('Error: invalid phone number')

    # sets email
    print('''
Enter the Email:
(enter to leave blank)
    ''')

    email = input('Email: ')
    lines.append(f'email: {email}')
    
    # edits attachment
    print('''
Enter the attachment:
Family or Friend
(enter blank to exit without saving)
    ''')
    while True:
        attachment = input('Attachment: ')
        if attachment == 'Family':
            lines.append('attachment: Family')
            break
        elif attachment == '':
            print_options()
            return
        elif attachment == 'Friend':
            lines.append('attachment: Friend')
            break
        else:
            print('Error: invalid attachment')

    # writes lines[] to cont file
    with open(f'{cont_dir}{cont_name}.cont', 'w') as cont_file:
        for L in lines:
            cont_file.write(f'{L}\n')

    print_options()


def edit_cont(cont_name):  
    print(f'\nediting: {cont_name}')

    #reads existing cont into lines[]
    lines = []
    with open(f'{cont_dir}{cont_name}.cont', 'r') as cont_file:
        for L in cont_file:
            lines.append(L)
        
    # sets cont phone number
    print('''
Enter the new phone number of the contact:
(enter to leave unchanged)
        ''')
        
    while True:
        phone_number = input_default('Phone number: ', lines[1].removeprefix('number: ').strip())

        # checks if phone number is a number
        try:
            tryint = int(phone_number)
        except:
            print('Error: not a number')
            continue

            # checks if phone number is too short, too long or correct length
        if phone_number == '':
            break
        elif len(phone_number) == 10:
            lines[1] = f'number: {phone_number}\n'
            break
        elif len(phone_number) > 10:
            print('Error: phone number too long')
            continue
        elif len(phone_number) < 10:
            print('Error: phone number too short')

    # sets email
    print('''
Enter the new Email:
(enter to leave unchanged)
    ''')

    email = input_default('Email: ', lines[2].removeprefix('email: ').strip())
    lines[2] = f'email: {email}\n'
    
    # edits attachment
    print('''
Enter the new attachment:
Family or Friend
(enter blank to exit without saving)
    ''')
    while True:
        attachment = input_default('Attachment: ', lines[3].removeprefix('attachment: ').strip())
        if attachment == 'Family':
            lines[3] = 'attachment: Family\n'
            break
        elif attachment == 'Friend':
            lines[3] = 'attachment: Friend\n'
            break
        elif attachment == '':
            print_options()
            return
        else:
            print('Error: invalid attachment')

    # writes lines[] to cont file
    with open(f'{cont_dir}{cont_name}.cont', 'w') as cont_file:
        for L in lines:
            cont_file.write(L)
    print_options()


# list all conts
def list_conts():
    clear_term()
    print('\nContact list:\n')

    # reads all cont file names from ./Contacts into files[]
    files = glob.glob('Contacts/*.cont')
    
    # for each cont:
    for cont in files:
        lines = []
        # reads and prints each line in cont
        with open(cont, 'r') as cont_file:
            for L in cont_file:
                lines.append(L)
            for L in lines:
                print(L.strip())
            print()

    # waits for user input
    while True:
        list_input = input('(enter to continue, f for family, b for friends) ')

        # if input: f, print all family conts
        if list_input == 'f':
            clear_term()
            print('\nFamily contacts:\n')
            for cont in files:

                # reads and prints each line in cont if family
                lines = []
                with open(cont, 'r') as cont_file:
                    for L in cont_file:
                        lines.append(L)
                    if lines[3] != 'attachment: Family\n':
                        continue
                    for L in lines:
                        print(L.strip())
                    print()
        
         # if input: b, print all friend conts
        elif list_input == 'b':
            clear_term()
            print('\nFriend contacts:\n')
            for cont in files:

                # reads and prints each line in cont if friend
                lines = []
                with open(cont, 'r') as cont_file:
                    for L in cont_file:
                        lines.append(L)
                    if lines[3] != 'attachment: Friend\n':
                        continue
                    for L in lines:
                        print(L.strip())
                    print()
        else:
            print_options()
            return
        


# deletes a given cont
def delete_cont():
    clear_term()
    print('\nContacts:\n')

    # reads all cont file names from ./Contacts into files[]
    files = glob.glob(f'{cont_dir}*.cont')
    
    # for each cont:
    for cont in files:

        # reads and prints the cont name of each cont
        lines = []
        with open(cont, 'r') as cont_file:
            for L in cont_file:
                lines.append(L)
            print(' -', lines[0].strip() + ',', lines[3].removeprefix('attachment: '), lines[2].removeprefix('email: '))

    # deletes cont            
    while True:

        # gets cont name
        print('(enter to exit)')
        cont_name = input('Contact to delete: ')

        # if cont exists:
        if os.path.isfile(f'{cont_dir}{cont_name}.cont'):
            
            # reads cont into lines[] and prints the cont
            print()
            lines = []
            with open(f'{cont_dir}{cont_name}.cont', 'r') as cont_file:
                for L in cont_file:
                    lines.append(L)
                for L in lines:
                    print(L.strip())
            
            # check if user is sure before deleting cont
            while True:
                del_confirm = input(f'\nAre you sure you want to delete {cont_name}? (PERMENENT) (enter to exit) (yes/no)')
                if del_confirm == 'yes':
                    os.remove(f'{cont_dir}{cont_name}.cont')
                    print(f'Contact: {cont_name} deleted')
                    if cont_name == 'System32':
                        print('OH NO!')
                    # waits for user input (allows user to see what was deleted)
                    input('(enter to continue)')
                    print_options()
                    return
                elif del_confirm == 'no':
                    print_options()
                    return
                else:
                    print('\nError: not valid response')
        
        # exits function
        elif cont_name == '':
            print_options()
            return
        
        # cont doesn't exist
        else:
            print('\nError: cont does not exist\n')


# Creates cont folder if it doesn't exist
if not os.path.exists(cont_dir):
    os.mkdir(cont_dir)

# Welcome message
clear_term()
print('''
Welcome to Contact Manager

Please choose an option:

a: add a contact or edit an existing contact
l: list all contacts
d: delete a contact
q: quit
    ''')

# Valid options
valid_options = ('a', 'l', 'd', 'q')

# loops over user inputs, breaks on q
while True:
    user_input = input('Enter option: ')
    if user_input not in valid_options:
        print('Error: invalid option')
        continue
    elif user_input == 'q':
        print('\nGoodbye!\n')
        break
    else:
        do_option(user_input)