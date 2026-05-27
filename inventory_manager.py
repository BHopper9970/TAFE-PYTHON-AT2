'''
Program:     Inventory Manager
Description: Creates and manages Inventories using text files

Author:      Ben Hopper
Date:        27/05/2026
Version:     1.0
'''

'''
.item file structure:
line 0: 'item name'
line 1: 'quantity'
line 2: 'price'
'''

import os
import glob
import readline


# Makes list of all item files in the folder
inv_dir = './Inventory/'
item_list = glob.glob(f'{inv_dir}*.item')


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

a: add an item or edit an existing item
l: list all items
v: change item stock quantity
d: delete an item
q: quit
    ''')


# runs specified option
def do_option(option):
    if option == 'a':
        add_item()
    elif option == 'l':
        list_items()
    elif option == 'v':
        change_stock()
    elif option == 'd':
        delete_item()


# add item to manager
def add_item():
    clear_term()
    #gets item name
    print('(enter to exit)')
    item_name = input('\nEnter item name: ')

    # if item already exists:
    if os.path.isfile(f'{inv_dir}{item_name}.item'):
        print(f'\nediting: {item_name}')

        #reads existing item into lines[]
        with open(f'{inv_dir}{item_name}.item', 'r') as item_file:
            lines = item_file.readlines()
        
        # sets item quantity
        print('''
Enter the current stock quantity of this item
(enter to leave unchanged)
        ''')
        
        while True:
            quantity = input_default('Quantity: ', lines[1].removeprefix('quantity: ').strip())
           
            try: 
                quantity = int(quantity)
                break
            except:
                print('Error: quantity is not an integer')

        lines[1] = f'quantity: {quantity}\n'
        
        
        # sets item price
        print('''
Enter the price of this item
(enter to leave unchanged)
        ''')

        while True:
            price = input_default('Cost: $', lines[2].removeprefix('price: $').strip())
           
            try: 
                price = float(price)
                break
            except:
                print('Error: price is not a float')

        lines[2] = f'price: ${price}\n'

        # writes lines[] to item file
        with open(f'{inv_dir}{item_name}.item', 'w') as item_file:
            for L in lines:
                item_file.write(f'{L}')

    # exit function
    elif item_name == '':
        return
    
    # if item doesn't exist:
    else:
        print(f'\nCreating item: {item_name}')
        lines = []

        # sets item title
        lines.append(item_name)

        # sets item quantity
        print('''
Enter the stock quantity of this item
(enter blank to exit without saving)
        ''')
        while True:
            quantity = input('Quantity: ')
            
            # exits without saving
            if quantity == '':
                print_options()
                return
           
            try: 
                quantity = int(quantity)
                break
            except:
                print('Error: quantity is not an integer')

        lines.append(f'quantity: {quantity}')
        
        
        # sets item price
        print('''
Enter the price of this item
(enter blank to exit without saving)
        ''')

        while True:
            price = input('Price: $')
            
            # exits without saving
            if price == '':
                print_options()
                return
           
            try: 
                price = float(price)
                break
            except:
                print('Error: price is not a float')

        lines.append(f'price: ${price}')

        # writes lines[] to item file
        with open(f'{inv_dir}{item_name}.item', 'w') as item_file:
            for L in lines:
                item_file.write(f'{L}\n')

    print_options()


# list all items
def list_items():
    clear_term()
    print('\nItem list:\n')

    # reads all item file names from ./Inventorys into files[]
    files = glob.glob(f'{inv_dir}*.item')
    
    # for each item:
    for item in files:

        # reads and prints each line in item
        with open(item, 'r') as item_file:
            lines = item_file.readlines()
            for L in lines:
                print(L.strip())
            total_value = int(lines[1].removeprefix('quantity: ').strip()) * float(lines[2].removeprefix('price: $').strip())
            print(f'Total Value: ${total_value}\n')

    # waits for user input
    input('(enter to continue)')

    print_options()


# modify item quantity
def change_stock():
    clear_term()
    print('\nItems:\n')
    # reads all item file names from ./Inventorys into files[]
    files = glob.glob(f'{inv_dir}*.item')
    
    # for each item:
    for item in files:

        # reads and prints the item name of each item
        with open(item, 'r') as item_file:
            lines = item_file.readlines()
            print(f' - {lines[0].strip()}, {lines[1]}')
                  
    # gets item name
    while True:
        print('(enter to exit)')
        item_name = input('Item to modify: ')

        # reads item into lines[]
        if os.path.isfile(f'{inv_dir}{item_name}.item'):
            with open(f'{inv_dir}{item_name}.item', 'r') as item_file:
                lines = item_file.readlines()
            break

        # exits program
        elif item_name == '':
            print_options()
            return
        
        # item doesn't exist
        else:
            print('Error: item does not exist')
    
   # sets item quantity
    print('''
Enter the current stock quantity of this item
(enter to leave unchanged)
        ''')
        
    while True:
        quantity = input_default('Quantity: ', lines[1].removeprefix('quantity: ').strip())
        
        try: 
            quantity = int(quantity)
            break
        except:
            print('Error: quantity is not an integer')

    lines[1] = f'quantity: {quantity}\n'
    
# writes lines[] to item file
    with open(f'{inv_dir}{item_name}.item', 'w') as item_file:
        for L in lines:
            item_file.write(f'{L}')
    
    print_options()


# deletes a given item
def delete_item():
    clear_term()
    print('\nItems:\n')

    # reads all item file names from ./Inventory into files[]
    files = glob.glob(f'{inv_dir}*.item')
    
    # for each item:
    for item in files:

        # reads and prints the item name of each item
        with open(item, 'r') as item_file:
            lines = item_file.readlines()
            print(' -', lines[0].strip())
    print()

    # deletes item            
    while True:

        # gets item name
        print('(enter to exit)')
        item_name = input('Item to delete: ')

        # if item exists:
        if os.path.isfile(f'{inv_dir}{item_name}.item'):
            
            # reads item into lines[] and prints the item
            print()
            with open(f'{inv_dir}{item_name}.item', 'r') as item_file:
                lines = item_file.readlines()
                for L in lines:
                    print(L.strip())
            
            # check if user is sure before deleting item
            while True:
                del_confirm = input(f'\nAre you sure you want to delete {item_name}? (PERMENENT) (yes/no) ')
                if del_confirm == 'yes':
                    os.remove(f'{inv_dir}{item_name}.item')
                    print(f'Item: {item_name} deleted')
                    if item_name == 'System32':
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
        elif item_name == '':
            print_options()
            return
        
        # item doesn't exist
        else:
            print('\nError: item does not exist\n')


if not os.path.exists(inv_dir):
    os.mkdir(inv_dir)

# Welcome message
clear_term()
print('''
Welcome to Item Manager

Please choose an option:

a: add an item or edit an existing item
l: list all items
v: change item stock quantity
d: delete an item
q: quit
    ''')

# Valid options
valid_options = ('a', 'l', 'v', 'd', 'q')

# loops over user inputs, breaks on q
while True:
    user_input = input('Enter option: ')
    if user_input not in valid_options:
        print('Error: itemalid option')
        continue
    elif user_input == 'q':
        print('\nGoodbye!\n')
        break
    else:
        do_option(user_input)