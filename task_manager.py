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


# imput with default text written by https://stackoverflow.com/users/56338/sth
def input_default(prompt, prefill=''):
   readline.set_startup_hook(lambda: readline.insert_text(prefill).strip())
   try:
      return input(prompt)  # or raw_input in Python 2
   finally:
      readline.set_startup_hook()


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
    #gets task name
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
            priority = input('Priority: ')
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
            priority = input('Status: ')
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
        description = input_default('\nDescription: ', lines[4].removeprefix('description: '))
        lines[4] = f'description: {description}'

        # writes lines[] to task file
        with open(f'{task_dir}{task_name}.task', 'w') as task_file:
            for L in lines:
                task_file.write(f'{L}')
    
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
                print('Error: invalid priority')
        
        # sets completion to incomplete
        lines.append('status: incomplete')

        # sets description
        description = input('Description: ')
        lines.append(f'description: {description}')

        # writes lines[] to task file
        with open(f'{task_dir}{task_name}.task', 'w') as task_file:
            for L in lines:
                task_file.write(f'{L}\n')

    # prints new option selecter
    print('''
Please choose an option:

a: add a task or edit an existing task
l: list all tasks
c: mark a task as complete
d: delete a task
d-all: delete all completed tasks
q: quit
    ''')
    return


def list_tasks():
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

    # prints new option selecter
    print('''
Please choose an option:

a: add a task or edit an existing task
l: list all tasks
c: mark a task as complete
d: delete a task
d-all: delete all completed tasks
q: quit
    ''')
    return

def complete_task():
    print('\nTasks:\n')

    # reads all task file names from ./Tasks into files[]
    files = glob.glob('Tasks/*.task')
    
    # for each task:
    for task in files:

        # reads and prints the task name of each task
        with open(task, 'r') as task_file:
            lines = task_file.readlines()
            print(lines[0].strip() + ',', lines[3].removeprefix('status: '))
                  
    # gets task name
    while True:
        task_name = input('Task name: ')

        # reads task into lines[]
        if os.path.isfile(f'{task_dir}{task_name}.task'):
            with open(f'{task_dir}{task_name}.task', 'r') as task_file:
                lines = task_file.readlines()
            break
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
            break
        else:
            print('Error: invalid status')
    
    # writes lines[] to task file
        with open(f'{task_dir}{task_name}.task', 'w') as task_file:
            for L in lines:
                task_file.write(f'{L}')
    
    # prints new option selecter
    print('''
Please choose an option:

a: add a task or edit an existing task
l: list all tasks
c: mark a task as complete
d: delete a task
d-all: delete all completed tasks
q: quit
    ''')
    return


# Welcome message
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