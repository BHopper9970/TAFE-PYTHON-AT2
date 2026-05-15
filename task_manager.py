'''
Program:     Task Manager
Description: Creates and manages simple tasks using text files

Author:      Ben Hopper
Date:        15/05/2026
Version:     1.0
'''
import os
import glob

'''
.task file structure:
line 1: 'task name'
line 2: 'priority' (low, medium or high)
line 3: 'status' (complete or imcomplete)
line 4+: 'description'
'''

# Makes list of all task files in the folder
task_dir = './Tasks/'
task_list = glob.glob(f'{task_dir}*.task')

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

# adds task to manager
def add_task():
    task_name = input('enter task name:')

    # checks if task already exists
    if os.path.isfile(f'{task_dir}{task_name}.task'):
        print(f'editing: {task_name}')

        #opens existing task
        with open(f'{task_dir}{task_name}.task', 'r') as taskfile:
            lines = taskfile.readlines()
        
        # sets task priority
        print('''
        enter the new priority of the task:
        low, medium or high
        (enter to leave unchanged)
        ''')

        priority = input('priority: ')
        while True:
            if priority == 'low':
                lines[1] = 'priority: low'
                break
            elif priority == 'medium':
                lines[1] = 'priority: medium'
                break
            elif priority == 'high':
                lines[1] = 'priority: high'
                break
            elif priority == '':
                break
            else:
                print('error: invalid priority')
    
    #creates new task
    else:
        print(f'creating task: {task_name}')
        lines = []
        
        # sets task priority
        print('''
        enter the priority of the task:
        low, medium or high
        ''')

        # sets task title
        lines.append(task_name)

        priority = input('priority: ')
        while True:
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
                print('error: invalid priority')
    print(lines)
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
    user_input = input('enter option: ')
    if user_input not in valid_options:
        print('Error: invalid option')
        continue
    elif user_input == 'q':
        print('\nGoodbye!\n')
        break
    else:
        do_option(user_input)