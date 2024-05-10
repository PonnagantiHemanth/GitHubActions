import unittest
import unit
import ast

def run_tests_from_filter():
    # Read test names from the text file
    test_names = []
    with open("testfilter.txt", "r") as file:
        test_names_str = file.read().strip()  # Read the whole content as a string
        test_names = ast.literal_eval(test_names_str)  # Convert the string to a list using ast.literal_eval

    # Check available test methods in TestAddition
    available_tests = dir(unit.TestAddition)

    # Load the test suite from the unit module
    suite = unittest.TestSuite()

    # Load specific tests from the unittest file based on the test names from the text file
    for test_name in test_names:
        if hasattr(unit.TestAddition, test_name):
            suite.addTest(unit.TestAddition(test_name))
        else:
            print("Test method not found:", test_name)

    # Run the tests
    runner = unittest.TextTestRunner()
    result = runner.run(suite)

if __name__ == "__main__":
    run_tests_from_filter()
