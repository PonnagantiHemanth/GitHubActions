import tkinter as tk
import subprocess
import os
import time

import unit
def add_tests_to_filter(selected_tests):
    with open("testfilter.txt", "w") as file:
        file.write("[" + ", ".join([f"'{test}'" for test in selected_tests]) + "]")
    print("Selected tests added to the filter successfully.")


def print_result(results):
    if results.returncode == 0:
        print(results.stdout)
    else:
        print('Git command failed:')
        print(results.stderr)


def add_tests():
    selected_tests = []
    for var, test_name in checkbox_vars:
        if var.get():
            selected_tests.append(test_name)
    if selected_tests:
        add_tests_to_filter(selected_tests)  # Update testfilter.txt with selected tests
    else:
        print("No tests selected.")


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
