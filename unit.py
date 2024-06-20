import unittest


def test_1x009(self):
    print("positive")
    result = addition(5, 6)
    self.assertEqual(result, 11)


def addition(a, b):
    return a + b
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)


class TestAddition(unittest.TestCase):
    def test_1x009(self):
        print("positive")
        result = addition(5, 6)
        self.assertEqual(result, 1111111)

    def test_4x008(self):
        result = addition(-5, -6)
        self.assertEqual(result, -1111)

    def test_8x007(self):
        result = addition(5, -6)
        self.assertEqual(result, -1)

    def test_9x009(self):
        result = addition(0, 0)
        self.assertEqual(result, 0)

    def test_2x007(self):
        result = addition(1000000000, 2000000000)
        self.assertEqual(result, 3000000000)

    def test_decimal_numbers(self):
        result = addition(3.5, 2.5)
        self.assertEqual(result, 6)

    def test_string_concatenation(self):
        result = addition("Hello", "World")
        self.assertEqual(result, "HelloWorld")

    def test_list_concatenation(self):
        result = addition([1, 2, 3], [4, 5, 6])
        self.assertEqual(result, [1, 2, 3, 4, 5, 6])

    def test_tuple_concatenation(self):
        result = addition((1, 2), (3, 4))
        self.assertEqual(result, (1, 2, 3, 4))

    def test_invalid_input(self):
        with self.assertRaises(TypeError):
            addition("Hello", 5)

    def test_fibonacci_5(self):
        result = fibonacci(5)
        self.assertEqual(result, 5)