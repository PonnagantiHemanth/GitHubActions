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


def add_tests_and_push():
    selected_tests = []
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
        result = subprocess.run(git_status_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True)
        if "UI.py" in result.stdout:
            print("Local changes detected in UI.py. Committing changes before switching branches...")
            commit_changes("UI.py")
        if "testfilter.txt" in result.stdout:
            print("Local changes detected in testfilter.txt. Committing changes before switching branches...")
            commit_changes("testfilter.txt")

        # Pull changes from the remote branch and rebase your local changes
        subprocess.run('git pull --rebase origin HEAD', shell=True)

        # Check if there are changes to commit before pushing to the remote repository
        git_commit_check_command = 'git diff-index --quiet HEAD'
        commit_check_result = subprocess.run(git_commit_check_command, shell=True, stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE, text=True)
        if commit_check_result.returncode != 0:
            print("Changes detected. Committing changes before pushing...")
            git_commit_command = 'git commit -am "Ci Test"'
            subprocess.run(git_commit_command, shell=True)

        # Push changes to the selected branch
        repo = repo_var.get()
        subprocess.run(f'git push origin HEAD:{repo} --force', shell=True)  # Force push to the selected branch

        print("Changes pushed successfully.")

        # Automatically trigger button click event once after manual button click
        global button_clicked_manually
        if button_clicked_manually:
            button_clicked_manually = False  # Reset the flag
            run_button.invoke()

    else:
        print("No tests selected.")


def search_url():
    url = url_entry.get()
    branch_name = branch_entry.get()  # Get the branch name entered by the user

    if not url:
        messagebox.showerror("Error", "Please enter a URL.")
        return
    if not branch_name:
        messagebox.showerror("Error", "Please enter a branch name.")
        return

    # Function to open the link and click on the "Actions" tab
    def open_and_click_actions_tab(url):
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
            username_field.send_keys("hemanthponnaganti1@gmail.com")

            # Add a delay to allow the username to be filled
            time.sleep(2)

            # Find and fill the password field
            password_field = driver.find_element(By.ID, "password")
            password_field.send_keys("ponna@123")  # Replace with your password

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
            branch_dropdown = driver.find_element(By.CSS_SELECTOR,
                                                   'summary[data-view-component="true"] span[data-menu-button]')
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
            time.sleep(80)  # Add a delay for the action to complete

        except Exception as e:
            print("Failed to click the buttons:", e)

        # Close the ChromeDriver instance
        driver.quit()

    # Example usage
    open_and_click_actions_tab(url)


root = tk.Tk()
root.title("Ui")
root.configure(bg="#f0f0ff")  # Set background color

# Create a frame for the first UI section containing checkboxes
frame1 = tk.Frame(root, bg="#f0f0ff")
frame1.pack(pady=10)

checkbox_vars = []

# Create checkboxes for selecting tests
unit_test_names = [name for name in dir(unit.TestAddition) if name.startswith('test_')]
for test_name in unit_test_names:
    var = tk.BooleanVar()
    checkbox = tk.Checkbutton(frame1, text=test_name, variable=var)
    checkbox.pack(anchor='w')
    checkbox_vars.append((var, test_name))

# Create a frame for the second UI section containing entry fields and branch dropdown
frame2 = tk.Frame(root, bg="#f0f0ff")
frame2.pack(pady=10)

repo_var = tk.StringVar(frame2)
repos = ["main", "perso/hemanth/UI"]  # List of available repositories
repo_var.set(repos[0])  # Set the default repository
repo_dropdown = tk.OptionMenu(frame2, repo_var, *repos)
repo_dropdown.pack(pady=5)


# Add a button to add selected tests and push to the selected repository
run_button = tk.Button(frame2, text="Start Test", command=add_tests_and_push)
run_button.pack(pady=5)

# Entry fields for entering URL and branch name
url_entry = tk.Entry(frame2, width=50)
url_entry.pack(pady=5)
branch_entry = tk.Entry(frame2, width=50)
branch_entry.pack(pady=5)




# Bind the Enter key to the search function
branch_entry.bind("<Return>", lambda event: search_url())

# Create a button to trigger the search
search_button = tk.Button(frame2, text="Search", command=search_url)
search_button.pack(pady=5)

button_clicked_manually = False




root.mainloop()
