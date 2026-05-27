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
cont_list = glob.glob(f'{cont_dir}*.cont')


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
        add_cont()
    elif option == 'l':
        list_conts()
    elif option == 'd':
        delete_cont()


# add cont to manager
def add_cont():
    clear_term()
    #gets cont name
    print('(enter to exit)')
    cont_name = input('\nEnter contact name: ')

    # if cont already exists:
    if os.path.isfile(f'{cont_dir}{cont_name}.cont'):
        print(f'\nediting: {cont_name}')

        #reads existing cont into lines[]
        with open(f'{cont_dir}{cont_name}.cont', 'r') as cont_file:
            lines = cont_file.readlines()
        
        # sets cont phone number
        print('''
Enter the new phone number of the contact:
(enter to leave unchanged)
        ''')
        
        while True:
            phone_number = input_default('Phone number: ', lines[1].removeprefix('number: ').strip())
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

    # exit function
    elif cont_name == '':
        print_options()
        return
    
    # if cont doesn't exist:
    else:
        print(f'\nCreating contact: {cont_name}')
        lines = []

        # sets cont name
        lines.append(cont_name)

        # sets cont phone number
        print('''
Enter the phone number of the contact:
(enter to leave blank)
        ''')
        
        while True:
            phone_number = input('Phone number: ')
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

        email = input_default('Email: ')
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


# list all conts
def list_conts():
    clear_term()
    print('\nContact list:\n')

    # reads all cont file names from ./Contacts into files[]
    files = glob.glob('Contacts/*.cont')
    
    # for each cont:
    for cont in files:

        # reads and prints each line in cont
        with open(cont, 'r') as cont_file:
            lines = cont_file.readlines()
            for L in lines:
                print(L.strip())
            print()

    # waits for user input
    input('(enter to continue)')

    print_options()


# deletes a given cont
def delete_cont():
    clear_term()
    print('\nTasks:\n')

    # reads all cont file names from ./Tasks into files[]
    files = glob.glob('Tasks/*.cont')
    
    # for each cont:
    for cont in files:

        # reads and prints the cont name of each cont
        with open(cont, 'r') as cont_file:
            lines = cont_file.readlines()
            print(' -', lines[0].strip() + ',', lines[3].removeprefix('attachment: '))

    # deletes cont            
    while True:

        # gets cont name
        print('(enter to exit)')
        cont_name = input('Task to delete: ')

        # if cont exists:
        if os.path.isfile(f'{cont_dir}{cont_name}.cont'):
            
            # reads cont into lines[] and prints the cont
            print()
            with open(f'{cont_dir}{cont_name}.cont', 'r') as cont_file:
                lines = cont_file.readlines()
                for L in lines:
                    print(L.strip())
            
            # check if user is sure before deleting cont
            while True:
                del_confirm = input(f'\nAre you sure you want to delete {cont_name}? (PERMENENT) (yes/no) ')
                if del_confirm == 'yes':
                    os.remove(f'{cont_dir}{cont_name}.cont')
                    print(f'Task: {cont_name} deleted')
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