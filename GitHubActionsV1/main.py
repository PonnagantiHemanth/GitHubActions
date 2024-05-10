import unit
import tkinter as tk
import subprocess
import os
import time


def add_tests_to_filter(selected_tests):
    with open("testfilter.txt", "w") as file:
        file.write('\n'.join(selected_tests))


def print_result(results):
    if results.returncode == 0:
        print(results.stdout)
    else:
        print('Git command failed:')
        print(results.stderr)


def run_selected_tests(selected_tests):
    suite = unittest.TestSuite()
    for test_name in selected_tests:
        test_method = getattr(unit.TestAddition, test_name)
        test_instance = unit.TestAddition()
        suite.addTest(
            unittest.FunctionTestCase(test_method, setUp=test_instance.setUp, tearDown=test_instance.tearDown))
    unittest.TextTestRunner().run(suite)


def add_tests():
    selected_tests = []
    for var, test_name in checkbox_vars:
        if var.get():
            selected_tests.append(test_name)
    add_tests_to_filter(selected_tests)  # Update testfilter.txt with selected tests

    # Git commands
    path = r"C:\Users\hponnaganti\Documents\UI\GitHubActions\GitHubActionsV1"
    os.chdir(path)
    git_commands = [
        'git status',
        'git add --all',
        'git commit -m "Ci Test"',
        'git push origin perso/hemanth/UI'  # Assuming perso/hemanth/UI is your branch name
    ]

    for command in git_commands:
        print(command)
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print_result(result)
        time.sleep(2)


def create_checkboxes():
    test_names = [name for name in dir(unit.TestAddition) if name.startswith('test_')]
    for test_name in test_names:
        var = tk.BooleanVar()
        checkbox = tk.Checkbutton(root, text=test_name, variable=var)
        checkbox.pack(anchor='w')
        checkbox_vars.append((var, test_name))


root = tk.Tk()
root.title("Select Tests to Add to Filter")
root.configure(bg="#f0f0ff")  # Set background color

checkbox_vars = []

run_button = tk.Button(root, text="Add Selected Tests to Filter and Push to Git", command=add_tests)
run_button.pack(side="bottom", pady=10)  # Position button at the bottom
create_checkboxes()
root.mainloop()

