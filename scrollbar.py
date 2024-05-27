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
import unit

selected_tests = []

# Function to display the test names
def display_test_names(option):
    # Clear the listbox
    listbox.delete(0, tk.END)

    # List test names based on the selected option
    if option == "Option 1":
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
    elif option == "Option 2":
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
    selected_test_frame.config(highlightbackground="black", highlightcolor="black", highlightthickness=2, padx=10, pady=10)

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
    branch_name = f"test_branch_{timestamp}"

    # Initialize a Git repository in the current directory
    subprocess.run(["git", "init"])

    # Add all files to the Git staging area
    subprocess.run(["git", "add", "."])

    # Commit changes
    subprocess.run(["git", "commit", "-m", "Initial commit"])

    # Create and checkout the temporary branch
    subprocess.run(["git", "checkout", "-b", branch_name])

    # Push the branch to GitHub
    subprocess.run(["git", "remote", "add", "origin", "https://github.com/PonnagantiHemanth/GitHubActions.git"])
    subprocess.run(["git", "push", "-u", "origin", branch_name])

    # Run selected tests on the created branch
    search_url(branch_name)


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
            time.sleep(200)  # Add a delay for the action to complete

        except Exception as e:
            print("Failed to click the buttons:", e)

        # Close the ChromeDriver instance
        driver.quit()

    # Example usage
    open_and_click_actions_tab()


# Set up the main application window
root = tk.Tk()
root.title("Scroll Bar")
root.attributes("-topmost", True)
root.configure(bg="lightblue")  # Set background color

# Create a heading label and center it
heading_label = tk.Label(root, text="Test Category", font=("Helvetica", 16), padx=20, pady=10, bg="lightblue")
heading_label.grid(row=0, column=0, columnspan=2, sticky="w")

# Create a Combobox (dropdown menu) after the label
dropdown_values = ["Option 1", "Option 2"]
combobox = ttk.Combobox(root, values=dropdown_values, state="readonly")
combobox.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="w")
combobox.current(0)  # Set the default selection

# Bind the combobox selection event to update the test list
combobox.bind("<<ComboboxSelected>>", update_tests)

# Create a frame for the listboxes
listboxes_frame = tk.Frame(root, bg="lightblue")
listboxes_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="w")  # Anchor the frame to the left side

# Create a listbox to display the test names
listbox = tk.Listbox(listboxes_frame, width=40, height=10, highlightthickness=0, borderwidth=5)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
listbox.config(width=50, height=20, bg="lightblue")  # Set fixed width and height for the listbox

# Bind the event to display the selected test
listbox.bind("<<ListboxSelect>>", display_selected_test)

# Create a scrollbar for the listbox
scrollbar = tk.Scrollbar(listboxes_frame, orient=tk.VERTICAL)
scrollbar.pack(side=tk.LEFT, fill=tk.Y)
scrollbar.config(command=listbox.yview)
listbox.config(yscrollcommand=scrollbar.set)

# Create a placeholder column between the listboxes
tk.Label(root, text="", bg="lightblue").grid(row=2, column=1)

# Create a frame to contain both selected tests and the additional box
combined_frame = tk.Frame(root, bg="lightblue")
combined_frame.grid(row=2, column=3, rowspan=2, padx=400, pady=(0, 20), sticky="w")  # Anchor the frame to the left side

# Create a frame for the selected test listbox with initial padding
selected_test_frame = tk.Frame(combined_frame, highlightthickness=0, bg="lightblue")
selected_test_frame.pack(fill=tk.BOTH, expand=True)

# Create a label for the selected test
selected_test_label = tk.Label(selected_test_frame, text="Selected Tests:", font=("Helvetica", 14), bg="lightblue")
selected_test_label.pack(anchor="w")

# Create a listbox to display the selected tests
selected_test_listbox = tk.Listbox(selected_test_frame, width=40, height=10, highlightthickness=0, borderwidth=5)
selected_test_listbox.pack(fill=tk.BOTH, expand=True)
selected_test_listbox.config(height=10, width=100, bg="lightblue")  # Set fixed width for the selected test listbox

# Add a scrollbar to the selected test listbox
selected_test_scrollbar = tk.Scrollbar(selected_test_frame, orient=tk.VERTICAL, command=selected_test_listbox.yview)
selected_test_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
selected_test_listbox.config(yscrollcommand=selected_test_scrollbar.set)

# Create a frame for the additional box below the selected tests
additional_frame = tk.Frame(combined_frame, bg="lightblue")
additional_frame.pack(fill=tk.BOTH, expand=True, pady=(100, 0))

# Create a label for the additional box
device_name_label_1 = tk.Label(additional_frame, text="Device Name 1:", font=("Helvetica", 14), bg="lightblue")
device_name_label_1.grid(row=0, column=0, sticky="w")

# Create a Combobox for device name 1 inside the additional box
device_name_values = ["Mouse", "Keyboard", "Drifter"]
device_combobox_1 = ttk.Combobox(additional_frame, values=device_name_values, state="readonly")
device_combobox_1.grid(row=0, column=1, padx=(10,0), pady=8, sticky="w")
device_combobox_1.current(0)  # Set the default selection

# Create another label for the additional box
device_name_label_2 = tk.Label(additional_frame, text="Patch_No:", font=("Helvetica", 14), bg="lightblue")
device_name_label_2.grid(row=0, column=2, sticky="s")

# Create an Entry box for device name 2 inside the additional box
device_entry_2 = tk.Entry(additional_frame, font=("Helvetica", 14))
device_entry_2.grid(row=0, column=3, sticky="w")

# Create another label for the additional box
device_name_label_3 = tk.Label(additional_frame, text="Test  Bed:", font=("Helvetica", 14), bg="lightblue")
device_name_label_3.grid(row=2, column=1, sticky="w", padx=8)

# Create a Combobox for device name 3 inside the additional box
device_name_values2 = ["Kosmos","OtherDevices"]
device_combobox_3 = ttk.Combobox(additional_frame, values=device_name_values2, state="readonly")
device_combobox_3.grid(row=2, column=2, padx=(10, 0), pady=50, sticky="w")
device_combobox_3.current(0)  # Set the default selection

username_label = tk.Label(additional_frame, text="GitHub Username:", bg="lightblue", font=("Helvetica", 12))
username_label.grid(row=3, column=0, pady=(10, 5), padx=10, sticky='w')

username_entry = tk.Entry(additional_frame, width=30, font=("Helvetica", 10))
username_entry.grid(row=3, column=1, pady=(10, 5), padx=10, sticky='w')

password_label = tk.Label(additional_frame, text="GitHub Password:", bg="lightblue", font=("Helvetica", 12))
password_label.grid(row=3, column=2, pady=(10, 5), padx=10, sticky='e')

password_entry = tk.Entry(additional_frame, width=30, font=("Helvetica", 10), show='*')
password_entry.grid(row=3, column=3, pady=(10, 5), padx=10, sticky='e')

button = tk.Button(root, text="Start Test", command=start_test, activebackground="green", activeforeground="white",
                   anchor="center", bd=3, bg="lightgray", cursor="hand2", disabledforeground="green", fg="green",
                   font=("Arial", 8), height=1, highlightbackground="black", highlightcolor="green",
                   highlightthickness=2, justify="center", overrelief="raised", padx=8, pady=5, width=15,
                   wraplength=100)
button.grid(row=4, column=3)

root.mainloop()
