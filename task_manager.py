'''
Program:     Task Manager
Description: Creates and manages simple tasks using text files

Author:      Ben Hopper
Date:        15/05/2026
Version:     1.0
'''

'''
.task file structure:
line 0: 'task name'
line 1: 'creation date'
line 2: 'priority' (low, medium or high)
line 3: 'status' (complete or imcomplete)
line 4: 'description'
'''

import os
import glob
import readline
from datetime import date


# Makes list of all task files in the folder
task_dir = './Tasks/'
task_list = glob.glob(f'{task_dir}*.task')


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

a: add a task or edit an existing task
l: list all tasks
c: mark a task as complete
d: delete a task
d-all: delete all completed tasks
q: quit
    ''')


# runs specified option
def do_option(option):
    if option == 'a':
        add_task()
    elif option == 'l':
        list_tasks()
    elif option == 'c':
        complete_task()
    elif option == 'd':
        delete_task()
    elif option == 'd-all':
        delete_complete()


# add task to manager
def add_task():
    clear_term()
    #gets task name
    print('(enter to exit)')
    task_name = input('\nEnter task name: ')

    # if task already exists:
    if os.path.isfile(f'{task_dir}{task_name}.task'):
        print(f'\nediting: {task_name}')

        #reads existing task into lines[]
        with open(f'{task_dir}{task_name}.task', 'r') as task_file:
            lines = task_file.readlines()
        
        # sets task priority
        print('''
Enter the new priority of the task:
low, medium or high
(enter to leave unchanged)
        ''')
        
        while True:
            priority = input_default('Priority: ', lines[2].removeprefix('priority: ').strip())
            if priority == 'low':
                lines[2] = 'priority: low\n'
                break
            elif priority == 'medium':
                lines[2] = 'priority: medium\n'
                break
            elif priority == 'high':
                lines[2] = 'priority: high\n'
                break
            elif priority == '':
                break
            else:
                print('Error: invalid priority')

        # sets completion status
        print('''
Enter the new completion status:
complete or incomplete
(enter to leave unchanged)
        ''')

        while True:
            priority = input_default('Status: ', lines[3].removeprefix('status: ').strip())
            if priority == 'incomplete':
                lines[3] = 'status: incomplete\n'
                break
            elif priority == 'complete':
                lines[3] = 'status: complete\n'
                break
            elif priority == '':
                break
            else:
                print('Error: invalid status')
        
        # edits description
        description = input_default('\nDescription: ', lines[4].removeprefix('description: ').strip())
        lines[4] = f'description: {description}'

        # writes lines[] to task file
        with open(f'{task_dir}{task_name}.task', 'w') as task_file:
            for L in lines:
                task_file.write(f'{L}')

    # exit function
    elif task_name == '':
        return
    
    # if task doesn't exist:
    else:
        print(f'\nCreating task: {task_name}')
        lines = []

        # sets task title
        lines.append(task_name)

        # sets task creation date
        lines.append(f'created at: {date.today()}')

        # sets task priority
        print('''
enter the priority of the task:
low, medium or high
        ''')
        
        while True:
            priority = input('priority: ')
            if priority == 'low':
                lines.append('priority: low')
                break
            elif priority == 'medium':
                lines.append('priority: medium')
                break
            elif priority == 'high':
                lines.append('priority: high')
                break
            else:
                print('Error: invalid pr' -',iority')
        
        # sets completion to incomplete
        lines.append('status: incomplete')

        # sets description
        description = input('\nDescription: ')
        lines.append(f'description: {description}')

        # writes lines[] to task file
        with open(f'{task_dir}{task_name}.task', 'w') as task_file:
            for L in lines:
                task_file.write(f'{L}\n')

    print_options()


def list_tasks():
    clear_term()
    print('\nTask list:\n')

    # reads all task file names from ./Tasks into files[]
    files = glob.glob('Tasks/*.task')
    
    # for each task:
    for task in files:

        # reads and prints each line in task
        with open(task, 'r') as task_file:
            lines = task_file.readlines()
            for L in lines:
                print(L.strip())
            print()

    # waits for user input
    input('(enter to continue)')

    print_options()


def complete_task():
    clear_term()
    print('\nTasks:\n')
    # reads all task file names from ./Tasks into files[]
    files = glob.glob('Tasks/*.task')
    
    # for each task:
    for task in files:

        # reads and prints the task name of each task
        with open(task, 'r') as task_file:
            lines = task_file.readlines()
            print(' -', lines[0].strip() + ',', lines[3].removeprefix('status: '))
                  
    # gets task name
    while True:
        print('(enter to exit)')
        task_name = input('Task to complete: ')

        # reads task into lines[]
        if os.path.isfile(f'{task_dir}{task_name}.task'):
            with open(f'{task_dir}{task_name}.task', 'r') as task_file:
                lines = task_file.readlines()
            break

        # exits program
        elif task_name == '':
            print_options()
            return
        
        # task doesn't exist
        else:
            print('Error: task does not exist')
    
    # sets completion status
    print('''
Enter the new completion status:
complete or incomplete
    ''')

    while True:
        priority = input_default('Status: ', 'complete')
        if priority == 'incomplete':
            lines[3] = 'status: incomplete\n'
            break
        elif priority == 'complete':
            lines[3] = 'status: complete\n'
            break
        elif priority == '':
            print_options()
            return
        else:
            print('Error: invalid status')
    
# writes lines[] to task file
    with open(f'{task_dir}{task_name}.task', 'w') as task_file:
        for L in lines:
            task_file.write(f'{L}')
    
    print_options()


def delete_task():
    clear_term()
    print('\nTasks:\n')

    # reads all task file names from ./Tasks into files[]
    files = glob.glob('Tasks/*.task')
    
    # for each task:
    for task in files:

        # reads and prints the task name of each task
        with open(task, 'r') as task_file:
            lines = task_file.readlines()
            print(' -', lines[0].strip() + ',', lines[3].removeprefix('status: '))

    # deletes task            
    while True:

        # gets task name
        print('(enter to exit)')
        task_name = input('Task to delete: ')

        # if task exists:
        if os.path.isfile(f'{task_dir}{task_name}.task'):
            
            # reads task into lines[] and prints the task
            print()
            with open(f'{task_dir}{task_name}.task', 'r') as task_file:
                lines = task_file.readlines()
                for L in lines:
                    print(L.strip())
            
            # check if user is sure before deleting task
            while True:
                del_confirm = input(f'\nAre you sure you want to delete {task_name}? (PERMENENT) (yes/no)')
                if del_confirm == 'yes':
                    os.remove(f'{task_dir}{task_name}.task')
                    print(f'Task: {task_name} deleted')
                    return
                elif del_confirm == 'no':
                    print_options()
                    return
                else:
                    print('\nError: not valid response')
        
        # exits function
        elif task_name == '':
            print_options()
            return
        
        # task doesn't exist
        else:
            print('\nError: task does not exist\n')


def delete_complete():
    clear_term()
    print('\nTasks:\n')

    # reads all task file names from ./Tasks into files[]
    files = glob.glob('Tasks/*.task')
    
    # for each task:
    for task in files:

        # reads and prints the task name of each task
        with open(task, 'r') as task_file:
            lines = task_file.readlines()
            print(' -', lines[0].strip() + ',', lines[3].removeprefix('status: '))
    
     # check if user is sure before deleting task
    while True:
        del_confirm = input(f'Are you sure you want to delete all completed tasks? (PERMENENT) (yes/no) ')
        if del_confirm == 'yes':
            for task in files:
                with open(task, 'r') as task_file:
                    lines = task_file.readlines()
                if lines[3] == 'status: complete\n':
                    os.remove(task)
                    print(f'Task: {task.removesuffix('.task').removeprefix('Tasks/')} deleted')
                else:
                    continue
            # waits for user input
            input('(enter to continue)')
            print_options()
            return
        elif del_confirm == 'no':
            print_options()
            return
        else:
            print('\nError: not valid response')


# Welcome message
clear_term()
print('''
Welcome to Task Manager

Please choose an option:

a: add a task or edit an existing task
l: list all tasks
c: mark a task as complete
d: delete a task
d-all: delete all completed tasks
q: quit
    ''')

# Valid options
valid_options = ('a', 'l', 'c', 'd', 'd-all', 'q')

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