import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import subprocess
import os
import time
import unit

def add_tests_to_filter(selected_tests):
    with open("testfilter.txt", "w") as file:
        file.write("[" + ", ".join([f"'{test}'" for test in selected_tests]) + "]")
    print("Selected tests added to the filter successfully.")
    # Stage and commit the changes for testfilter.txt
    subprocess.run('git add testfilter.txt', shell=True)
    subprocess.run('git commit -m "Update testfilter.txt"', shell=True)

def commit_changes(file):
    # Commit changes to the specified file
    git_add_command = f'git add {file}'
    git_commit_command = f'git commit -m "Committing changes to {file} before branch switch"'
    subprocess.run(git_add_command, shell=True)
    subprocess.run(git_commit_command, shell=True)

def handle_rebase_conflict():
    messagebox.showerror("Rebase Conflict", "A rebase conflict has occurred. Please resolve the conflict manually.")
    subprocess.run('git rebase --abort', shell=True)
    print("Rebase conflict detected. Please resolve the conflict manually.")
    exit(1)

def add_tests_and_push():
    selected_tests = []
    origin_branch = "main"
    for var, test_name in checkbox_vars:
        if var.get():
            selected_tests.append(test_name)
    if selected_tests:
        add_tests_to_filter(selected_tests)  # Update testfilter.txt with selected tests

        # Change directory to the project directory
        path = r"C:\Users\hponnaganti\Documents\UI\GitHubActions"
        os.chdir(path)

        # Check if there are local changes that need to be committed before switching branches
        git_status_command = 'git status'
        result = subprocess.run(git_status_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if "UI.py" in result.stdout:
            print("Local changes detected in UI.py. Committing changes before switching branches...")
            commit_changes("UI.py")
        if "testfilter.txt" in result.stdout:
            print("Local changes detected in testfilter.txt. Committing changes before switching branches...")
            commit_changes("testfilter.txt")

        # Stash any untracked files and changes before rebasing
        subprocess.run('git add .', shell=True)
        subprocess.run('git stash', shell=True)

        # Pull changes from the remote branch and rebase your local changes
        try:
            subprocess.run('git pull --rebase origin HEAD', shell=True, check=True)
        except subprocess.CalledProcessError:
            handle_rebase_conflict()

        # Unstash any stashed changes after rebasing
        subprocess.run('git stash pop', shell=True)

        # Check if there are changes to commit before pushing to the remote repository
        git_commit_check_command = 'git diff-index --quiet HEAD'
        commit_check_result = subprocess.run(git_commit_check_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if commit_check_result.returncode != 0:
            print("Changes detected. Committing changes before pushing...")
            git_commit_command = 'git commit -am "Ci Test"'
            subprocess.run(git_commit_command, shell=True)

        # Get the branch name from the entry field
        branch_name = branch_entry.get() + "/" + patch_entry.get() + "/" + device_entry.get()  ## device name

        # Create a new branch
        subprocess.run(f'git checkout -b {branch_name}', shell=True)

        # Push the new branch to the remote repository
        subprocess.run(f'git push origin {branch_name}', shell=True)

        subprocess.run(f'git checkout {origin_branch}', shell=True)
        print("Changes pushed successfully.")

        # Automatically trigger button click event once after manual button click
        # global button_clicked_manually
        # if button_clicked_manually:
        #     button_clicked_manually = False  # Reset the flag
        #     run_button.invoke()

        # Call function to automate web interaction
        # search_url(branch_name)

        # Add function to delete the branch after the tests are completed
        # delete_branch(branch_name)

    else:
        print("No tests selected.")

def delete_branch(branch_name):
    # Change directory to the project directory
    path = r"C:\Users\hponnaganti\Documents\UI\GitHubActions"
    os.chdir(path)

    # Delete the branch locally and remotely
    subprocess.run(f'git branch -d {branch_name}', shell=True)
    subprocess.run(f'git push origin --delete {branch_name}', shell=True)

    print(f"Branch {branch_name} deleted successfully.")

def search_url(branch_name):
    url = "https://github.com/PonnagantiHemanth/GitHubActions"  # The URL is constant
    # Function to open the link and click on the "Actions" tab
    def open_and_click_actions_tab():
        # Configure Chrome options
        options = Options()
        options.headless = True  # Run Chrome in headless mode (no GUI)

        driver = webdriver.Chrome(options=options)

        driver.get(url)

        driver.maximize_window()

        time.sleep(5)  # Adjust the wait time as needed

        actions_tab_element = driver.find_element(By.ID, 'actions-tab')
        actions_tab_element.click()

        time.sleep(5)

        try:
            driver.execute_script("document.querySelector('a[href^=\"/login?\"]').click();")

            username_field = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "login_field"))
            )

            # Fill the username field
            username_field.send_keys(username_entry.get())

            # Add a delay to allow the username to be filled
            time.sleep(2)

            # Find and fill the password field
            password_field = driver.find_element(By.ID, "password")
            password_field.send_keys(password_entry.get())  # Use the password from entry

            # Wait for the sign in button to be clickable
            sign_in_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "js-sign-in-button"))
            )

            # Click the sign in button
            sign_in_button.click()

            # Add a delay for the sign-in process
            time.sleep(8)

            # Click the "Actions" tab again
            actions_tab_element = driver.find_element(By.ID, 'actions-tab')
            actions_tab_element.click()
            time.sleep(5)  # Add a delay for the tab switch to complete

            # Click the "Run Tests" link
            run_tests_link = driver.find_element(By.XPATH, '//a[contains(@href, "/actions/workflows/actions.yml")]')
            run_tests_link.click()
            time.sleep(7)  # Add a delay for the new page to load

            # Click the "Run workflow" button
            run_workflow_button = driver.find_element(By.XPATH, '//summary[contains(text(), "Run workflow")]')
            run_workflow_button.click()
            time.sleep(7)  # Add a delay for the action to complete

            # Click the "Branch" dropdown using CSS selector
            branch_dropdown = driver.find_element(By.CSS_SELECTOR, 'summary[data-view-component="true"] span[data-menu-button]')
            branch_dropdown.click()
            time.sleep(5)  # Add a delay for the dropdown to open

            # Enter the branch name in the input field
            branch_input = driver.find_element(By.ID, 'context-commitish-filter-field')
            branch_input.send_keys(branch_name)
            time.sleep(2)  # Add a delay for the branch name to be entered

            # Press Enter to confirm the branch selection
            branch_input.send_keys(Keys.RETURN)
            time.sleep(5)  # Add a delay for the branch selection to be applied

            # Click the "Run workflow" button
            run_workflow_button = driver.find_element(By.XPATH, '//button[contains(text(), "Run workflow")]')
            run_workflow_button.click()
            time.sleep(100)  # Add a delay for the action to complete

        except Exception as e:
            print("Failed to click the buttons:", e)

        # Close the ChromeDriver instance
        driver.quit()

    # Example usage
    open_and_click_actions_tab()

root = tk.Tk()
root.title("UI for GitHub Actions")
root.configure(bg="#d9e5ff")  # Set background color

# Create a label for the checkbox section
test_label = tk.Label(root, text="List of tests", bg="#d9e5ff", font=("Helvetica", 20, "bold"))
test_label.pack(pady=(10, 5))

# Create a frame for the first UI section containing checkboxes
frame1 = tk.Frame(root, bg="#d9e5ff", pady=10)
frame1.pack()

checkbox_vars = []

# Create checkboxes for selecting tests
unit_test_names = [name for name in dir(unit.TestAddition) if name.startswith('test_')]
for test_name in unit_test_names:
    var = tk.BooleanVar()
    checkbox = tk.Checkbutton(frame1, text=test_name, variable=var, bg="#d9e5ff", font=("Helvetica", 15))
    checkbox.pack(anchor='w', padx=10, pady=5)
    checkbox_vars.append((var, test_name))

# Add a canvas widget for the line separator
canvas = tk.Canvas(root, height=2, bg="black", highlightthickness=0)
canvas.create_line(0, 0, 500, 0, fill="black")
canvas.pack(fill='x', pady=20)

# Create a frame for the second UI section
frame2 = tk.Frame(root, bg="#d9e5ff")
frame2.pack()

# Add a label for users to input their desired branch name
branch_label = tk.Label(frame2, text="Test Bed", bg="#d9e5ff", font=("Helvetica", 12))
branch_label.grid(row=1, column=0, pady=(30, 5), padx=10, sticky='w')  # Increased pady

# Add an entry field for users to input branch name
branch_entry = tk.Entry(frame2, width=30, font=("Helvetica", 10))
branch_entry.grid(row=1, column=1, pady=(30, 5), padx=10, sticky='w')  # Increased pady and changed sticky to 'w'

# Add a label for users to input their desired device name
device_label = tk.Label(frame2, text="Patch NO", bg="#d9e5ff", font=("Helvetica", 12))
device_label.grid(row=0, column=2, pady=(10, 5), padx=10, sticky='e')

# Add an entry field for users to input device name
device_entry = tk.Entry(frame2, width=30, font=("Helvetica", 10))
device_entry.grid(row=0, column=3, pady=(10, 5), padx=10, sticky='e')

# Add a label for the Patch Link
patch_link_label = tk.Label(frame2, text="Device Name:", bg="#d9e5ff", font=("Helvetica", 12))
patch_link_label.grid(row=0, column=0, pady=(10, 5), padx=10, sticky='w')

# Add an entry field for users to input the patch link
patch_entry = tk.Entry(frame2, width=30, font=("Helvetica", 10))
patch_entry.grid(row=0, column=1, pady=(10, 5), padx=10, sticky='w')

# Add labels and entry fields for GitHub login
username_label = tk.Label(frame2, text="GitHub Username:", bg="#d9e5ff", font=("Helvetica", 12))
username_label.grid(row=3, column=0, pady=(10, 5), padx=10, sticky='w')

username_entry = tk.Entry(frame2, width=30, font=("Helvetica", 10))
username_entry.grid(row=3, column=1, pady=(10, 5), padx=10, sticky='w')

password_label = tk.Label(frame2, text="GitHub Password:", bg="#d9e5ff", font=("Helvetica", 12))
password_label.grid(row=3, column=2, pady=(10, 5), padx=10, sticky='e')

password_entry = tk.Entry(frame2, width=30, font=("Helvetica", 10), show='*')
password_entry.grid(row=3, column=3, pady=(10, 5), padx=10, sticky='e')

# Add a button to add selected tests and push to the selected repository
run_button = tk.Button(frame2, text="Start Test", command=add_tests_and_push, bg="#4CAF50", fg="white",
                       font=("Helvetica", 12, "bold"))
run_button.grid(row=4, column=0, columnspan=4, pady=10)

button_clicked_manually = False
root.geometry("1600x1050")
root.mainloop()