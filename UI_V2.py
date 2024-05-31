import tkinter as tk
from tkinter import ttk
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

selected_tests = []

# Function to display the test names
def display_test_names(option):
    # Clear the listbox
    listbox.delete(0, tk.END)

    # List test names based on the selected option
    if option == "Mouse":
        test_names = [
            "test_positive",
            "test_negative",
            "test_mixed_positive_negative",
            "test_zero",
            "test_large_numbers",
            "test_decimal_numbers",
            "test_string_concatenation",
            "test_list_concatenation",
            "test_tuple_concatenation",
            "test_invalid_input"
        ]
    elif option == "Keyboard":
        test_names = [
            "test_fibonacci_5",
            "test_string_concatenation",
            "test_list_concatenation",
            "test_tuple_concatenation",
            "test_invalid_input",
            "test_string_concatenation",
            "test_list_concatenation",
            "test_tuple_concatenation",
            "test_invalid_input",
            "test_string_concatenation",
            "test_list_concatenation",
            "test_tuple_concatenation",
            "test_invalid_input",
            "test_string_concatenation",
            "test_list_concatenation",
            "test_tuple_concatenation",
            "test_invalid_input",
            "test_invalid_input",
            "test_string_concatenation",
            "test_list_concatenation",
            "test_tuple_concatenation",
            "test_invalid_input"
        ]

    # Insert test names into the listbox
    for test_name in test_names:
        listbox.insert(tk.END, test_name)


# Function to display the selected tests in the selected test listbox
def display_selected_test(event):
    # Get the selected test indices
    selected_indices = listbox.curselection()

    # Extract the corresponding test names and append them to the selected tests list
    for index in selected_indices:
        test_name = listbox.get(index)
        if test_name not in selected_tests:
            selected_tests.append(test_name)

    # Clear the selected test listbox
    selected_test_listbox.delete(0, tk.END)

    # Insert the selected tests into the selected test listbox
    for test_name in selected_tests:
        selected_test_listbox.insert(tk.END, test_name)

    # Apply a border around the selected test listbox
    selected_test_frame.config(highlightbackground="black", highlightcolor="black", highlightthickness=2)

    # Write selected tests to file
    write_selected_tests_to_file()


# Function to update the test list when the combobox selection changes
def update_tests(event):
    selected_option = combobox.get()
    display_test_names(selected_option)


# Function to write selected tests to file
def write_selected_tests_to_file():
    with open("testfilter.txt", "w") as file:
        file.write(str(selected_tests))


def start_test():
    # Get the selected tests
    selected_tests_str = ','.join(selected_tests)

    # Create a temporary branch name based on current time
    timestamp = int(time.time())
    branch_name = combobox.get() + device_entry_2.get() + device_combobox_3.get()

    # Initialize a Git repository in the current directory
    subprocess.run(["git", "init"])

    # Add all files to the Git staging area
    subprocess.run(["git", "add", "."])

    # Commit changes
    subprocess.run(["git", "commit", "-m", "Initial commit"])

    # Check if the remote already exists
    remote_output = subprocess.run(["git", "remote"], capture_output=True, text=True)
    if "origin" not in remote_output.stdout.splitlines():
        # Add the remote only if it doesn't already exist
        subprocess.run(["git", "remote", "add", "origin", "https://github.com/PonnagantiHemanth/GitHubActions.git"])
    else:
        print("Remote 'origin' already exists. Skipping adding remote.")

    # Create and checkout the temporary branch
    subprocess.run(["git", "checkout", "-b", branch_name])

    # Push the branch to GitHub
    subprocess.run(["git", "push", "-u", "origin", branch_name])

    # Run selected tests on the created branch
    search_url(branch_name)

    # Delete the temporary branch both locally and remotely
    delete_branch(branch_name)


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

        time.sleep(3)  # Adjust the wait time as needed

        actions_tab_element = driver.find_element(By.ID, 'actions-tab')
        actions_tab_element.click()

        time.sleep(3)

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
            time.sleep(5)

            # Click the "Actions" tab again
            actions_tab_element = driver.find_element(By.ID, 'actions-tab')
            actions_tab_element.click()
            time.sleep(5)  # Add a delay for the tab switch to complete

            # Click the "Run Tests" link
            run_tests_link = driver.find_element(By.XPATH, '//a[contains(@href, "/actions/workflows/actions.yml")]')
            run_tests_link.click()
            time.sleep(5)  # Add a delay for the new page to load

            # Click the "Run workflow" button
            run_workflow_button = driver.find_element(By.XPATH, '//summary[contains(text(), "Run workflow")]')
            run_workflow_button.click()
            time.sleep(5)  # Add a delay for the action to complete

            # Click the "Branch" dropdown using CSS selector
            branch_dropdown = driver.find_element(By.CSS_SELECTOR, 'summary[data-hotkey="b"]')
            branch_dropdown.click()
            time.sleep(2)

            # Search for the branch name
            search_input = driver.find_element(By.CSS_SELECTOR, 'input[name="filter-ref-list"]')
            search_input.send_keys(branch_name)
            time.sleep(2)

            # Click on the branch name in the dropdown
            branch_option = driver.find_element(By.CSS_SELECTOR, f'div[data-target^="/PonnagantiHemanth/GitHubActions/actions/runs/{branch_name}"]')
            branch_option.click()
            time.sleep(2)

            # Click the "Run workflow" button again
            run_workflow_button = driver.find_element(By.XPATH, '//button[contains(text(), "Run workflow")]')
            run_workflow_button.click()
            time.sleep(5)  # Add a delay for the action to complete

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

        finally:
            driver.quit()

    # Open the link and click the "Actions" tab
    open_and_click_actions_tab()


def delete_branch(branch_name):
    # Switch to the main branch
    subprocess.run(["git", "checkout", "main"])

    # Delete the local branch
    subprocess.run(["git", "branch", "-D", branch_name])

    # Delete the remote branch
    subprocess.run(["git", "push", "origin", "--delete", branch_name])


# Create the main window
window = tk.Tk()
window.title("GitHub Actions UI")

# Add a label
label = ttk.Label(window, text="Select the type of test:")
label.grid(row=0, column=0, padx=10, pady=10)

# Add a combobox to select the type of test
options = ["Mouse", "Keyboard"]
combobox = ttk.Combobox(window, values=options)
combobox.grid(row=0, column=1, padx=10, pady=10)
combobox.current(0)  # Set default selection
combobox.bind("<<ComboboxSelected>>", update_tests)

# Add a listbox to display the test names
listbox = tk.Listbox(window, selectmode=tk.MULTIPLE, width=50, height=10)
listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
display_test_names("Mouse")  # Display test names initially

# Bind a function to the listbox to display the selected test in the selected test listbox
listbox.bind("<<ListboxSelect>>", display_selected_test)

# Add a frame to hold the selected test listbox
selected_test_frame = tk.Frame(window, relief=tk.GROOVE, borderwidth=2)
selected_test_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Add a label for the selected tests
selected_test_label = ttk.Label(selected_test_frame, text="Selected Tests:")
selected_test_label.grid(row=0, column=0, padx=10, pady=10)

# Add a listbox to display the selected tests
selected_test_listbox = tk.Listbox(selected_test_frame, selectmode=tk.MULTIPLE, width=50, height=10)
selected_test_listbox.grid(row=1, column=0, padx=10, pady=10)

# Add scrollbars to the listboxes
listbox_scrollbar = ttk.Scrollbar(window, orient=tk.VERTICAL, command=listbox.yview)
listbox_scrollbar.grid(row=1, column=2, sticky=(tk.N, tk.S))
listbox.config(yscrollcommand=listbox_scrollbar.set)

selected_test_listbox_scrollbar = ttk.Scrollbar(selected_test_frame, orient=tk.VERTICAL, command=selected_test_listbox.yview)
selected_test_listbox_scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
selected_test_listbox.config(yscrollcommand=selected_test_listbox_scrollbar.set)

# Add start button
start_button = ttk.Button(window, text="Start Tests", command=start_test)
start_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Add entries for GitHub credentials
username_label = ttk.Label(window, text="GitHub Username:")
username_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")
username_entry = ttk.Entry(window)
username_entry.grid(row=4, column=1, padx=10, pady=10)

password_label = ttk.Label(window, text="GitHub Password:")
password_label.grid(row=5, column=0, padx=10, pady=10, sticky="e")
password_entry = ttk.Entry(window, show="*")
password_entry.grid(row=5, column=1, padx=10, pady=10)

# Add device entry and combobox
device_label_2 = ttk.Label(window, text="Device:")
device_label_2.grid(row=6, column=0, padx=10, pady=10, sticky="e")
device_entry_2 = ttk.Entry(window)
device_entry_2.grid(row=6, column=1, padx=10, pady=10)

device_combobox_3 = ttk.Combobox(window, values=["Desktop", "Mobile"])
device_combobox_3.grid(row=7, column=0, padx=10, pady=10, sticky="e")
device_combobox_3.current(0)

window.mainloop()
