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
        path = r"C:\Users\hponnaganti\Documents\UI\GitHubActions"
        os.chdir(path)

        # Stage all changes
        subprocess.run('git add .', shell=True)

        # Commit changes
        subprocess.run('git commit -m "Update test filter"', shell=True)

        # Switch to the selected branch
        subprocess.run(f'git checkout {repo}', shell=True)

        # Push changes to the selected branch
        subprocess.run(f'git push origin {repo}', shell=True)

        print("Changes pushed successfully.")
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
