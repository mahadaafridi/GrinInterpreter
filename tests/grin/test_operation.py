import unittest
import grin.operations

class TestOperation(unittest.TestCase):
    def test_base_class_values(self):
        self.assertEqual(1, grin.operations.Operation(1,2).value_1())
        self.assertEqual(2, grin.operations.Operation(1,2).value_2())

    def test_addition(self):
        self.assertEqual(3, grin.operations.Add(1,2).execute())
        self.assertEqual("Hello", grin.operations.Add("He", "llo").execute())

    def test_subtraction(self):
        self.assertEqual(-1, grin.operations.Subtract(1,2).execute())

    def test_multiplication(self):
        self.assertEqual(2, grin.operations.Multiply(1,2).execute())
        self.assertEqual("AAA", grin.operations.Multiply("A",3).execute())

    def test_int_div(self):
        self.assertEqual(2, grin.operations.Divide(7,3).execute_int_div())

    def test_norm_div(self):
        self.assertEqual(1.25, grin.operations.Divide(5,4).execute_norm_div())
if __name__ == '__main__':
    unittest.main()
