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
chrome_options = Options()
chrome_options.add_argument("--headless")
selected_tests = []


# Function to display the test names
def display_test_names(option):
    # Clear the listbox
    listbox.delete(0, tk.END)

    # List test names based on the selected option
    if option == "Mouse":
        test_names = [
            "test_1x009",
            "test_4x008",
            "test_8x007",
            "test_9x009",
            "test_2x007",
            "test_12x009",
            "test_11x007",
            "test_10x005",
            "test_7x007",
            "test_3x004",
            "test_6x004",
            "test_2x007"
        ]
    elif option == "Keyboard":
        test_names = [
            "test_11x007",
            "test_10x005",
            "test_7x007",
            "test_3x004",
            "test_6x004",
            "test_2x007",
            "test_4x008",
            "test_8x007",
            "test_9x009",
            "test_2x007",
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
    selected_test_frame.config(highlightbackground="black", highlightcolor="black", highlightthickness=2, padx=10,
                               pady=10)

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
    branch_name = device_combobox_1.get() + "/"+ device_entry_2.get() + "/" +device_combobox_3.get()
    # branch_name = device_name_values.get() + device_entry_2.get() + device_combobox_3.get()

    # Initialize a Git repository in the current directory
    subprocess.run(["git", "init"])

    # Add all files to the Git staging area
    subprocess.run(["git", "add", "."])

    # Commit changes
    subprocess.run(["git", "commit", "-m", "Initial commit"])

    # Check if the remote already
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
            # username_field.send_keys(username_entry.get())

            # Add a delay to allow the username to be filled
            time.sleep(30)

            # Find and fill the password field
            # password_field = driver.find_element(By.ID, "password")
            # password_field.send_keys(password_entry.get())  # Use the password from entry

            # Wait for the sign in button to be clickable
            #sign_in_button = WebDriverWait(driver, 10).until(
            #    EC.element_to_be_clickable((By.CLASS_NAME, "js-sign-in-button"))
            #)

            # Click the sign in button
            #sign_in_button.click()

            # Add a delay for the sign-in process
            #time.sleep(3)

            # Click the "Actions" tab again
            actions_tab_element = driver.find_element(By.ID, 'actions-tab')
            actions_tab_element.click()
            time.sleep(3)  # Add a delay for the tab switch to complete

            # Click the "Run Tests" link
            run_tests_link = driver.find_element(By.XPATH, '//a[contains(@href, "/actions/workflows/actions.yml")]')
            run_tests_link.click()
            time.sleep(3)  # Add a delay for the new page to load

            # Click the "Run workflow" button
            run_workflow_button = driver.find_element(By.XPATH, '//summary[contains(text(), "Run workflow")]')
            run_workflow_button.click()
            time.sleep(3)  # Add a delay for the action to complete

            # Click the "Branch" dropdown using CSS selector
            branch_dropdown = driver.find_element(By.CSS_SELECTOR,
                                                  'summary[data-view-component="true"] span[data-menu-button]')
            branch_dropdown.click()
            time.sleep(3)  # Add a delay for the dropdown to open

            # Enter the branch name in the input field
            branch_input = driver.find_element(By.ID, 'context-commitish-filter-field')
            branch_input.send_keys(branch_name)
            time.sleep(2)  # Add a delay for the branch name to be entered

            # Press Enter to confirm the branch selection
            branch_input.send_keys(Keys.RETURN)
            time.sleep(3)  # Add a delay for the branch selection to be applied

            # Click the "Run workflow" button
            run_workflow_button = driver.find_element(By.XPATH, '//button[contains(text(), "Run workflow")]')
            run_workflow_button.click()
            time.sleep(50)  # Add a delay for the action to complete

        except Exception as e:
            print("Failed to click the buttons:", e)

        # Close the ChromeDriver instance
        driver.quit()

    # Example usage
    open_and_click_actions_tab()


def delete_branch(branch_name):
    # Delete the branch locally
    subprocess.run(["git", "checkout", "main"])  # Switch to master branch before deletion
    subprocess.run(["git", "branch", "-d", branch_name])

    # Delete the branch remotely
    subprocess.run(["git", "push", "origin", "--delete", branch_name])
    print("Branch deleted")


# Function to delete selected test from the selected test listbox and list
def delete_selected_test(event):
    # Check if any item is selected
    if selected_test_listbox.curselection():
        # Get the index of the selected item
        index = selected_test_listbox.curselection()[0]

        # Remove the selected test from the listbox
        selected_test_listbox.delete(index)

        # Remove the selected test from the selected_tests list
        selected_tests.pop(index)

        # Write updated selected tests to file
        write_selected_tests_to_file()


# Function to display a popup message when Kosmos2 is selected
def display_popup(event):
    if (device_combobox_3.get() == "Kosmos2_Cortado") or device_combobox_3.get() == "Kosmos3_Drifter":
        messagebox.showinfo("Information", "The device is currently in use. Please select another device")
        device_combobox_3.current(0)  # Reset the combobox selection to its initial state

    # Reset the combobox selection to its initial state
# Set up the main application window
root = tk.Tk()
root.title("Scroll Bar")
# root.attributes("-topmost", True)
root.configure(bg="white")  # Set background color
root.geometry("1350x900")

# Add left side padding
left_padding_label = tk.Label(root, text="", bg="white")
left_padding_label.grid(row=0, column=0)

# Create a heading label and center it
heading_label = tk.Label(root, text="Test Category", font=("Helvetica", 16), padx=20, pady=10, bg="white")
heading_label.grid(row=0, column=1, columnspan=2, sticky="w")

# Create a Combobox (dropdown menu) after the label
dropdown_values = ["Mouse", "Keyboard"]
combobox = ttk.Combobox(root, values=dropdown_values, state="readonly")
combobox.grid(row=1, column=1, padx=20, pady=(0, 10), sticky="w")
combobox.current(0)  # Set the default selection
# heading_label = tk.Label(root, text="Test Features", font=("Helvetica", 16), padx=20, pady=10, bg="white")
# heading_label.grid(row=2, column=1, columnspan=2, sticky="w")
# Bind the combobox selection event to update the test list
combobox.bind("<<ComboboxSelected>>", update_tests)

# Create a frame for the listboxes with styling
listboxes_frame = tk.Frame(root, bg="white", bd=2, relief=tk.SOLID)
listboxes_frame.grid(row=3, column=1, padx=20, pady=(10, 20), sticky="sw")  # Anchor the frame to the left side

# Create a listbox to display the test names with styling
listbox = tk.Listbox(listboxes_frame, width=60, height=40, bg="white", highlightthickness=0, borderwidth=1)
listbox.pack(side=tk.LEFT, expand=False)

# Bind the event to display the selected test
listbox.bind("<<ListboxSelect>>", display_selected_test)

# Create a scrollbar for the listbox
# Create a scrollbar for the listbox
scrollbar = tk.Scrollbar(listboxes_frame, orient=tk.VERTICAL)
scrollbar.pack(side=tk.LEFT, fill=tk.Y)
scrollbar.config(command=listbox.yview)
listbox.config(yscrollcommand=scrollbar.set)

# Add padding after the first scrollbar
padding_label = tk.Label(listboxes_frame, text="", bg="white")
padding_label.pack(side=tk.LEFT)

# Create a placeholder column between the listboxes
tk.Label(root, text="", bg="white").grid(row=3, column=2)

# Create a frame to contain both selected tests and the additional box
combined_frame = tk.Frame(root, bg="white")
combined_frame.grid(row=3, column=6, rowspan=20, padx=10, pady=(0, 20),
                    sticky="ws")  # Anchor the frame to the left side

# Create a frame for the selected test listbox with initial padding
selected_test_frame = tk.Frame(combined_frame, bg="white", bd=2, relief=tk.SOLID)
selected_test_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=10)  # Add padding here

# Create a label for the selected test
selected_test_label = tk.Label(selected_test_frame, text="Selected Tests:", font=("Helvetica", 14), bg="white")
selected_test_label.pack(anchor="w")

# Create a listbox to display the selected tests
selected_test_listbox = tk.Listbox(selected_test_frame, width=40, height=17, highlightthickness=0, bg="white")
selected_test_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)

# Create a scrollbar for the selected test listbox
selected_test_scrollbar = tk.Scrollbar(selected_test_frame, orient=tk.VERTICAL, command=selected_test_listbox.yview)
selected_test_scrollbar.pack(side=tk.LEFT, fill=tk.Y)

# Configure the listbox to use the scrollbar
selected_test_listbox.config(yscrollcommand=selected_test_scrollbar.set)

# Create a frame for the additional box below the selected tests
additional_frame = tk.Frame(combined_frame, bg="white", bd=2, relief=tk.SOLID)
additional_frame.pack(fill=tk.BOTH, expand=True, pady=(100, 80), padx=170)  # Adjusted padding here

# Create a label for the additional box
device_name_label_1 = tk.Label(additional_frame, text="Device Name:", font=("Helvetica", 14), bg="white")
device_name_label_1.grid(row=0, column=0, sticky="s", padx=20,pady=10)

# Create a Combobox for device name 1 inside the additional  box
device_name_values = ["Sanak", "Keyboard", "Drifter"]
device_combobox_1 = ttk.Combobox(additional_frame, values=device_name_values, state="readonly")
device_combobox_1.grid(row=0, column=1, padx=(10, 0), pady=(8, 5), sticky="w")  # Added padding pady=(8, 5)
device_combobox_1.current(0)  # Set the default selection

# Create another label for the additional box
device_name_label_2 = tk.Label(additional_frame, text="Patch_No:-", font=("Helvetica", 14), bg="white")
device_name_label_2.grid(row=0, column=2,padx=(30, 10), pady=(8, 5), sticky="w")

# Create an Entry box for device name 2 inside the additional box
device_entry_2 = tk.Entry(additional_frame, font=("Helvetica", 14), bd=2, relief=tk.SOLID)
device_entry_2.grid(row=0, column=3, padx=(0, 10), pady=(8, 5), sticky="w")  # Added padding pady=(8, 5)

# Create another label for the additional box
device_name_label_3 = tk.Label(additional_frame, text="Test Bed:-", font=("Helvetica", 14), bg="white")
device_name_label_3.grid(row=1, column=2, padx=(10, 60), pady=(35, 30), sticky="w")

# Create a Combobox for device name 3 inside the additional box
device_name_values2 = ["Kosmos1_Sanak","Kosmos1_slimPlus", "Kosmos2_Cortado", "Kosmos3_Drifter", "Kosmos4_Lexend"]
device_combobox_3 = ttk.Combobox(additional_frame, values=device_name_values2, state="readonly")
device_combobox_3.grid(row=1, column=3, padx=(5, 10), pady=(10, 0), sticky="w")
#device_combobox_3.current(0)  # Set the default selection

# Bind event to display a popup message when Kosmos2 is selected
device_combobox_3.bind("<<ComboboxSelected>>", display_popup)

#username_label = tk.Label(additional_frame, text="GitHub Username:", bg="white", font=("Helvetica", 14))
#username_label.grid(row=2, column=0, pady=(20, 5), padx=20, sticky='w')

#username_entry = tk.Entry(additional_frame, width=25, font=("Helvetica", 14), bd=2, relief=tk.SOLID)
#username_entry.grid(row=2, column=1, pady=(20, 5), padx=20, sticky='w')

#password_label = tk.Label(additional_frame, text="GitHub Password:", bg="white", font=("Helvetica", 14))
#password_label.grid(row=2, column=2, pady=(10, 5), padx=20, sticky='e')

#password_entry = tk.Entry(additional_frame, width=25, font=("Helvetica", 14), bd=2, relief=tk.SOLID, show='*')
#password_entry.grid(row=2, column=3, pady=(10, 5), padx=20, sticky='ws')
# Create a label below the additional box
# Create a frame for the additional label
additional_label_frame = tk.Frame(root, bg="white")
additional_label_frame.grid(row=3, column=6, columnspan=2, pady=(100, 0))

# Create the label "ththt"
additional_label = tk.Label(additional_label_frame, text="Branch Creation", font=("Helvetica", 20), bg="white")
additional_label.pack()


button = tk.Button(root, text="Sign in & Start Test", command=start_test, activebackground="green", activeforeground="white",
                   anchor="center", bd=3, bg="white", cursor="hand2", disabledforeground="green", fg="green",
                   font=("Arial", 8), height=1, highlightbackground="black", highlightcolor="green",
                   highlightthickness=2, justify="center", overrelief="raised", padx=10, pady=5, width=15,
                   wraplength=100)
# Adjust the row and column placement of widgets to maintain consistent alignment
button.grid(row=3, column=5, pady=5, sticky="s", columnspan=2)
# Add horizontal lines
# horizontal_line1 = ttk.Separator(root, orient='horizontal')
# horizontal_line1.grid(row=1, column=1, columnspan=10, sticky='ew', pady=(60, 30), padx=90)

# Bind double-click event to delete selected test
selected_test_listbox.bind("<Double-Button-1>", delete_selected_test)

root.mainloop()
