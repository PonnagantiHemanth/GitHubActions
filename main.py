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

def add_tests(repo):
    selected_tests = []
    for var, test_name in checkbox_vars:
        if var.get():
            selected_tests.append(test_name)
    if selected_tests:
        add_tests_to_filter(selected_tests)  # Update testfilter.txt with selected tests
        # Change directory to the project directory
        path = [r"C:\Users\hponnaganti\Documents\UI\GitHubActions"]
        # Define Git commands based on the selected repository
        if repo == "main":
            git_command = ['git checkout main', 'git pull', 'git status', 'git add --all', 'git commit -m "Ci Test"', 'git push origin main']
        elif repo == "perso/hemanth/UI":
            git_command = ['git checkout perso/hemanth/UI', 'git pull', 'git status', 'git add --all', 'git commit -m "Ci Test"', 'git push origin perso/hemanth/UI']
        else:
            print("Invalid repository choice")
            return

        # Execute Git commands
        for command in git_command:
            print(command)
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print_result(result)
            time.sleep(2)
    else:
        print("No tests selected.")

def create_checkboxes():
    test_names = [name for name in dir(unit.TestAddition) if name.startswith('test_')]
    for test_name in test_names:
        var = tk.BooleanVar()
        checkbox = tk.Checkbutton(root, text=test_name, variable=var)
        checkbox.pack(anchor='w')
        checkbox_vars.append((var, test_name))

def select_repo():
    repo = repo_var.get()
    add_tests(repo)

root = tk.Tk()
root.title("Select Tests to Add to Filter")
root.configure(bg="#f0f0ff")  # Set background color

checkbox_vars = []

# Create checkboxes for selecting tests
create_checkboxes()

# Create a dropdown menu for selecting repositories
repo_var = tk.StringVar(root)
repos = ["main", "perso/hemanth/UI"]  # List of available repositories
repo_var.set(repos[0])  # Set the default repository
repo_dropdown = tk.OptionMenu(root, repo_var, *repos)
repo_dropdown.pack()

# Add a button to add selected tests and push to the selected repository
run_button = tk.Button(root, text="Add Selected Tests to Filter and Push to Git", command=select_repo)
run_button.pack(side="bottom", pady=10)  # Position button at the bottom

root.mainloop()
