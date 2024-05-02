import unit
import unittest
import tkinter as tk

class DynamicTestGeneration(unittest.TestCase):
    pass

def add_test_method(test_name):
    def test_method(self):
        getattr(unit.TestAddition, test_name)(self)
    return test_method

def run_selected_tests(selected_tests):
    suite = unittest.TestSuite()
    for test_name in selected_tests:
        test_method = add_test_method(test_name)
        setattr(DynamicTestGeneration, "test_" + test_name, test_method)
        suite.addTest(DynamicTestGeneration("test_" + test_name))
    unittest.TextTestRunner().run(suite)

def add_tests_to_filter(selected_tests):
    with open("testfilter.txt", "w") as file:
        file.write('\n'.join(selected_tests))

root = tk.Tk()
root.title("Select Tests to Run")
root.configure(bg="#f0f0ff")  # Set background color

checkbox_vars = []
tests_run = False

def run_tests():
    global tests_run
    selected_tests = []
    for var, test_name in checkbox_vars:
        if var.get():
            selected_tests.append(test_name)
    run_selected_tests(selected_tests)
    add_tests_to_filter(selected_tests)  # Update testfilter.txt with selected tests
    tests_run = True

def on_closing():
    global tests_run
    if not tests_run:
        run_tests()
    root.destroy()

def create_checkboxes():
    test_names = [name for name in dir(unit.TestAddition) if name.startswith('test_')]
    for test_name in test_names:
        var = tk.BooleanVar()
        checkbox = tk.Checkbutton(root, text=test_name, variable=var)
        checkbox.pack(anchor='w')
        checkbox_vars.append((var, test_name))

run_button = tk.Button(root, text="Run Selected Tests", command=run_tests)
run_button.pack(side="bottom", pady=10)  # Position button at the bottom
create_checkboxes()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
