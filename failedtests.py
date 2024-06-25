from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys  # Import Keys for sending keys
import time
import re  # Import the re module

# Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run headless if needed
chrome_options.add_argument("--window-size=1920,1080")  # Window size for screenshots

# Initialize the Chrome driver
driver = webdriver.Chrome(options=chrome_options)

# Maximize the window (if not headless)
driver.maximize_window()

# Open the URL
url = "https://github.com/PonnagantiHemanth/GitHubActions/actions/runs/9564478650/job/26365292524"
driver.get(url)

# Wait for the page to load
time.sleep(6)

# Login process (assuming login is needed)
try:
    driver.execute_script("document.querySelector('a[href^=\"/login?\"]').click();")
    username_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "login_field"))
    )
    # Assume user manually logs in within 30 seconds
    time.sleep(15)
except Exception as e:
    print("Login step skipped or failed:", e)

# Click on the 'python main.py' element
try:
    element = WebDriverWait(driver, 17).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'flex-1') and text()='python main.py']"))
    )
    element.click()
except Exception as e:
    print(f"An error occurred while clicking 'python main.py': {e}")

# Extract failed test details
testfilter = []  # Initialize an empty list to store test names
try:
    log_element = WebDriverWait(driver, 17).until(
        EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'FAIL:')]"))
    )
    failed_tests = driver.find_elements(By.XPATH, "//span[contains(text(), 'FAIL:')]")
    for test in failed_tests:
        match = re.search(r'FAIL: (\S+)', test.text)
        if match:
            test_name = match.group(1)  # Extract the test name
            testfilter.append(test_name)  # Append the test name to the testfilter list
except Exception as e:
    print(f"An error occurred while extracting failed test details: {e}")

finally:
    time.sleep(10)
    try:
        # Write the testfilter array to the testfilter.txt file
        with open('testfilter.txt', 'w') as file:
            file.write(str(testfilter))  # Convert the list to a string and write it to the file

        # Open the specified URL
        url_to_open = "https://github.com/PonnagantiHemanth/GitHubActions/actions"
        driver.get(url_to_open)
        time.sleep(5)

        # Navigate to the workflow page
        run_tests_link = driver.find_element(By.XPATH, '//a[contains(@href, "/actions/workflows/actions.yml")]')
        run_tests_link.click()
        time.sleep(3)

        # Click on "Run workflow" button
        run_workflow_button = driver.find_element(By.XPATH, '//summary[contains(text(), "Run workflow")]')
        run_workflow_button.click()
        time.sleep(3)

        # Click on branch dropdown to select branch
        branch_dropdown = driver.find_element(By.CSS_SELECTOR,
                                              'summary[data-view-component="true"] span[data-menu-button]')
        branch_dropdown.click()
        time.sleep(3)

        # Enter temporary branch name into input field
        branch_input = driver.find_element(By.ID, 'context-commitish-filter-field')
        branch_input.send_keys("testbranch")
        time.sleep(2)

        # Press Enter to submit branch name
        branch_input.send_keys(Keys.ENTER)
        time.sleep(2)

        # Click on "Run workflow" button after entering branch name
        run_workflow_button = driver.find_element(By.XPATH, '//button[contains(text(), "Run workflow")]')
        run_workflow_button.click()
        time.sleep(50)  # Adjust sleep time as needed for workflow to start
    except Exception as e:
        print(f"An error occurred in the finally block: {e}")
    finally:
        driver.quit()
