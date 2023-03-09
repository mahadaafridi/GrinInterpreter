import unittest
import grin.statement
import grin.parsing
from io import StringIO
from unittest.mock import patch

class TestStatement(unittest.TestCase):
    def setUp(self):
        self._grin_line = list(grin.parsing.parse(['LET MESSAGE 3', 'LET MESSAGE CS', 'LET CS MESSAGE', 'PRINT MESSAGE', 'PRINT "HELLO"', 'INNUM X', 'INSTR X', 'GOTO 3', 'GOTO MESSAGE', 'GOTO "CS"', '.']))
    def test_let_statement_replace_old_var(self):
        result = grin.statement.Statement(self._grin_line[0], {'MESSAGE' : 4}).let_statement()
        self.assertEqual(result, {'MESSAGE':3})
    def test_let_statement_for_var_value_0(self):
        result = grin.statement.Statement(self._grin_line[1], {'MESSAGE': 4}).let_statement()
        self.assertEqual(result, {'MESSAGE': 0})

    def test_let_statement_for_var(self):
        result = grin.statement.Statement(self._grin_line[2], {'MESSAGE': 4}).let_statement()
        self.assertEqual(result, {'MESSAGE':4, 'CS' : 4 })
    def test_print_statement_for_var_when_var_not_defined(self):
        output = StringIO()
        with patch('sys.stdout', new=output):
            grin.statement.Statement(self._grin_line[3], {}).print_statement()
        self.assertEqual(output.getvalue().strip(), "0")

    def test_print_statement_for_var_when_var_is_defined(self):
        output = StringIO()
        with patch('sys.stdout', new=output):
            grin.statement.Statement(self._grin_line[3], {'MESSAGE' : "BOO"}).print_statement()
        self.assertEqual(output.getvalue().strip(), "BOO")

    def test_print_statement_for_str(self):
        output = StringIO()
        with patch('sys.stdout', new=output):
            grin.statement.Statement(self._grin_line[4], {'MESSAGE' : "BOO"}).print_statement()
        self.assertEqual(output.getvalue().strip(), "HELLO")

    @patch('builtins.input', side_effect = ['-3 .  0'])
    def test_innum_statement_with_float(self, mock_input):
        result = grin.statement.Statement(self._grin_line[5], {}).innum_statement()
        self.assertEqual(result, {'X' : -3.0})

    @patch('builtins.input', side_effect = ['-3 .  0'])
    def test_innum_statement_with_float_type(self, mock_input):
        result = grin.statement.Statement(self._grin_line[5], {}).innum_statement()
        self.assertEqual(type(result['X']), float)

    @patch('builtins.input', side_effect = ['   3    '])
    def test_innum_statement_with_int(self, mock_input):
        result = grin.statement.Statement(self._grin_line[5], {}).innum_statement()
        self.assertEqual(result, {'X': 3})

    @patch('builtins.input', side_effect = [' 3'])
    def test_innum_statement_with_int_type(self, mock_input):
        result = grin.statement.Statement(self._grin_line[5], {}).innum_statement()
        self.assertEqual(type(result['X']), int)


    @patch('builtins.input', side_effect = [' hello there '])
    def test_instr_statement(self, mock_input):
        result = grin.statement.Statement(self._grin_line[5], {}).instr_statement()
        self.assertEqual(result, {'X': ' hello there '})

    def test_goto_statement_integer(self):
        result = grin.statement.Statement(self._grin_line[7], {'MESSAGE': 4}).goto_statement({})
        self.assertEqual(result, (3, False))

    def test_goto_statement_variable_with_int(self):
        result = grin.statement.Statement(self._grin_line[8], {'MESSAGE': 4}).goto_statement({})
        self.assertEqual(result, (4, False))

    def test_goto_statement_variable_with_negative_int(self):
        result = grin.statement.Statement(self._grin_line[8], {'MESSAGE': -4}).goto_statement({})
        self.assertEqual(result, (-4, False))

    def test_goto_statement_variable_with_label(self):
        result = grin.statement.Statement(self._grin_line[9], {'MESSAGE': 4}).goto_statement({'CS':3})
        self.assertEqual(result, (3, True))

    def test_operation_statement_add_two_ints(self):
        grin_line = list(grin.parsing.parse(['ADD X 3']))
        result = grin.statement.Statement(grin_line[0], {}).operation_statement(
            "ADD")
        self.assertEqual(result, {'X' : 3})
        self.assertEqual(type(result['X']), int)
    def test_operation_statement_add_two_floats(self):
        grin_line = list(grin.parsing.parse(['ADD Y 3.5']))
        result = grin.statement.Statement(grin_line[0], {'Y' : 3.5}).operation_statement(
            "ADD")
        self.assertEqual(result, {'Y' : 7.0})
        self.assertEqual(type(result['Y']), float)

    def test_operation_statement_add_int_float(self):
        grin_line = list(grin.parsing.parse(['ADD X 3']))
        result = grin.statement.Statement(grin_line[0], {'X' : 3.5}).operation_statement(
            "ADD")
        self.assertEqual(result, {'X' : 6.5})
        self.assertEqual(type(result['X']), float)

    def test_operation_statement_str_str(self):
        grin_line = list(grin.parsing.parse(['ADD X "OO"']))
        result = grin.statement.Statement(grin_line[0], {'X' : "B"}).operation_statement(
            "ADD")
        self.assertEqual(result, {'X' : "BOO"})
        self.assertEqual(type(result['X']), str)

    def test_operation_statement_sub_two_int(self):
        grin_line = list(grin.parsing.parse(['SUB X 3']))
        result = grin.statement.Statement(grin_line[0], {}).operation_statement(
            "SUB")
        self.assertEqual(result, {'X' : -3})

    def test_operation_statement_sub_two_float(self):
        grin_line = list(grin.parsing.parse(['SUB X 3.5']))
        result = grin.statement.Statement(grin_line[0], {'X' : 3.2}).operation_statement(
            "SUB")
        self.assertAlmostEqual(result['X'], -0.3, 3)
        self.assertEqual(type(result['X']), float)

    def test_operation_statement_sub_one_int_one_float(self):
        grin_line = list(grin.parsing.parse(['SUB X 3.5']))
        result = grin.statement.Statement(grin_line[0], {}).operation_statement(
            "SUB")
        self.assertEqual(result, {'X' : -3.5})
        self.assertEqual(type(result['X']), float)

    def test_operation_statement_mult_two_int(self):
        grin_line = list(grin.parsing.parse(['MULT X 3']))
        result = grin.statement.Statement(grin_line[0], {'X' : 3}).operation_statement(
            "MULT")
        self.assertEqual(result, {'X' : 9})
        self.assertEqual(type(result['X']), int)

    def test_operation_statement_mult_one_int_one_float(self):
        grin_line = list(grin.parsing.parse(['MULT X 3.5']))
        result = grin.statement.Statement(grin_line[0], {'X' : 2}).operation_statement(
            "MULT")
        self.assertEqual(result, {'X' : 7.0})
        self.assertEqual(type(result['X']), float)

    def test_operation_statement_mult_str_int(self):
        grin_line = list(grin.parsing.parse(['MULT X 2']))
        result = grin.statement.Statement(grin_line[0], {'X' : "Boo"}).operation_statement(
            "MULT")
        self.assertEqual(result, {'X' : "BooBoo"})
        self.assertEqual(type(result['X']), str)

    def test_operation_statement_mult_int_str(self):
        grin_line = list(grin.parsing.parse(['MULT X "Boo"']))
        result = grin.statement.Statement(grin_line[0], {'X' : 2}).operation_statement(
            "MULT")
        self.assertEqual(result, {'X' : "BooBoo"})
        self.assertEqual(type(result['X']), str)

    def test_operation_statement_div_int_int(self):
        grin_line = list(grin.parsing.parse(['DIV X 2']))
        result = grin.statement.Statement(grin_line[0], {'X' : 7}).operation_statement(
            "DIV")
        self.assertEqual(result, {'X' : 3})
        self.assertEqual(type(result['X']), int)

    def test_operation_statement_div_float_int(self):
        grin_line = list(grin.parsing.parse(['DIV X 2']))
        result = grin.statement.Statement(grin_line[0], {'X' : 7.0}).operation_statement(
            "DIV")
        self.assertEqual(result, {'X' : 3.5})
        self.assertEqual(type(result['X']), float)

    def test_operation_statement_div_float_float(self):
        grin_line = list(grin.parsing.parse(['DIV X 3.0']))
        result = grin.statement.Statement(grin_line[0], {'X' : 7.5}).operation_statement(
            "DIV")
        self.assertEqual(result, {'X' : 2.5})
        self.assertEqual(type(result['X']), float)

    def test_operation_statement_div_int_float(self):
        grin_line = list(grin.parsing.parse(['DIV X 2.0']))
        result = grin.statement.Statement(grin_line[0], {'X' : 7}).operation_statement(
            "DIV")
        self.assertEqual(result, {'X' : 3.5})
        self.assertEqual(type(result['X']), float)

    def test_operation_string_subtract_int(self):
        grin_line = list(grin.parsing.parse(['SUB X 3']))
        output = StringIO()
        with patch('sys.stdout', new=output):
            with self.assertRaises(SystemExit):
                grin.statement.Statement(grin_line[0], {'X' : '3'}).operation_statement("SUB")
        self.assertEqual(output.getvalue().strip(), 'ERROR: Type Error')

    def test_operation_string_divide_by_int(self):
        grin_line = list(grin.parsing.parse(['DIV X 3']))
        output = StringIO()
        with patch('sys.stdout', new=output):
            with self.assertRaises(SystemExit):
                grin.statement.Statement(grin_line[0], {'X' : '3'}).operation_statement("DIV")
        self.assertEqual(output.getvalue().strip(), 'ERROR: Type Error')

    def test_operation_zero_divide_error(self):
        grin_line = list(grin.parsing.parse(['DIV X 0']))
        output = StringIO()
        with patch('sys.stdout', new=output):
            with self.assertRaises(SystemExit):
                grin.statement.Statement(grin_line[0], {'X' : 6}).operation_statement("DIV")
        self.assertEqual(output.getvalue().strip(), 'ERROR: Zero Division Error')

    def test_comparison_statement_greater_than_int_int(self):
        grin_line = list(grin.parsing.parse(['GOTO 2 IF X > 2']))
        result = grin.statement.Statement(grin_line[0], {'X' : 1}).conditional()
        self.assertEqual(result, False)

    def test_comparison_statement_greater_than_equal_to_int_int(self):
        grin_line = list(grin.parsing.parse(['GOTO 2 IF X >= 2']))
        result = grin.statement.Statement(grin_line[0], {'X' : 2}).conditional()
        self.assertEqual(result, True)

    def test_comparison_statement_less_than_equal_to_int_int(self):
        grin_line = list(grin.parsing.parse(['GOTO 2 IF X <= 2']))
        result = grin.statement.Statement(grin_line[0], {'X' : 1}).conditional()
        self.assertEqual(result, True)

    def test_comparison_statement_less_than_to_int_int(self):
        grin_line = list(grin.parsing.parse(['GOTO 2 IF X < 2']))
        result = grin.statement.Statement(grin_line[0], {'X' : 2}).conditional()
        self.assertEqual(result, False)

    def test_comparison_statement_equal_to_int_int(self):
        grin_line = list(grin.parsing.parse(['GOTO 2 IF X = 2']))
        result = grin.statement.Statement(grin_line[0], {'X' : 2}).conditional()
        self.assertEqual(result, True)

    def test_comparison_statement_not_equal_to_int_int(self):
        grin_line = list(grin.parsing.parse(['GOTO 2 IF X <> 2']))
        result = grin.statement.Statement(grin_line[0], {'X' : 2}).conditional()
        self.assertEqual(result, False)

    def test_comparison_statement_not_equal_to_int_float(self):
        grin_line = list(grin.parsing.parse(['GOTO 2 IF X <> 2']))
        result = grin.statement.Statement(grin_line[0], {'X' : 2.1}).conditional()
        self.assertEqual(result, True)

    def test_comparison_statement_greater_than_to_int_float(self):
        grin_line = list(grin.parsing.parse(['GOTO 2 IF X > 2']))
        result = grin.statement.Statement(grin_line[0], {'X' : 2.1}).conditional()
        self.assertEqual(result, True)

    def test_comparison_statement_greater_than_to_float_float(self):
        grin_line = list(grin.parsing.parse(['GOTO 2 IF X > 2.3']))
        result = grin.statement.Statement(grin_line[0], {'X' : 2.1}).conditional()
        self.assertEqual(result, False)

    def test_comparison_statement_greater_than_str_str(self):
        grin_line = list(grin.parsing.parse(['GOTO 2 IF X > "Boo"']))
        result = grin.statement.Statement(grin_line[0], {'X' : "AAA"}).conditional()
        self.assertEqual(result, False)

    def test_comparison_statement_equal_to_str_str(self):
        grin_line = list(grin.parsing.parse(['GOTO 2 IF X = "Boo"']))
        result = grin.statement.Statement(grin_line[0], {'X' : "Boo"}).conditional()
        self.assertEqual(result, True)

    def test_comparison_statement_not_equal_to_str_str(self):
        grin_line = list(grin.parsing.parse(['GOTO 2 IF X <> "Boo"']))
        result = grin.statement.Statement(grin_line[0], {'X' : "BOo"}).conditional()
        self.assertEqual(result, True)

    def test_comparison_statement_str_int(self):
        grin_line = list(grin.parsing.parse(['GOTO 2 IF X > "Boo"']))
        output = StringIO()
        with patch('sys.stdout', new=output):
            with self.assertRaises(SystemExit):
                grin.statement.Statement(grin_line[0], {'X' : 3}).conditional()
        self.assertEqual(output.getvalue().strip(), 'ERROR: Values not comparable')

    def test_comparison_statement_int_str(self):
        grin_line = list(grin.parsing.parse(['GOTO 2 IF X > 3']))
        output = StringIO()
        with patch('sys.stdout', new=output):
            with self.assertRaises(SystemExit):
                grin.statement.Statement(grin_line[0], {'X' : '3'}).conditional()
        self.assertEqual(output.getvalue().strip(), 'ERROR: Values not comparable')

if __name__ == '__main__':
    unittest.main()