import unittest
import grin.program_state
import grin.parsing
from io import StringIO
from unittest.mock import patch
class TestProgramState(unittest.TestCase):
    def setUp(self):
        self.grin_lines1 = list(grin.parsing.parse(['LET MESSAGE 3', 'holder : PRINT MESSAGE', '.']))
        self.grin_lines2 = list(
            grin.parsing.parse(['LET MESSAGE CW', '.']))
        self.grin_lines3 = list(
            grin.parsing.parse(['PRINT 3', '.']))
        self.grin_lines4 = list(
            grin.parsing.parse(['LET MESSAGE "BOO"', '.']))
    def test_let_statement_integer(self):
        result = grin.program_state.ProgramState(self.grin_lines1).process_line()
        self.assertEqual(result, {'MESSAGE': 3})

    def test_let_statement_str(self):
        result = grin.program_state.ProgramState(self.grin_lines4).process_line()
        self.assertEqual(result, {'MESSAGE': "BOO"})

    def test_goto_statement(self):
        grin_line = list(grin.parsing.parse(['GOTO 2', 'PRINT MESSAGE','.']))
        state = grin.program_state.ProgramState(grin_line)
        state.process_line()
        result = state.current_line()
        self.assertEqual(result, 2)

    def test_gosub_statement(self):
        grin_line = list(grin.parsing.parse(['GOSUB 2', 'PRINT MESSAGE','.']))
        state = grin.program_state.ProgramState(grin_line)
        state.process_line()
        result = state.current_line()
        self.assertEqual(result, 2)


    def test_print_statement_int(self):
        output = StringIO()
        with patch('sys.stdout', new = output):
            grin.program_state.ProgramState(self.grin_lines3).process_line()
        self.assertEqual(output.getvalue().strip(), "3")

    def test_print_statement_var(self):
        grin_line = list(
            grin.parsing.parse(['PRINT C', '.']))
        output = StringIO()
        with patch('sys.stdout', new = output):
            grin.program_state.ProgramState(grin_line).process_line()
        self.assertEqual(output.getvalue().strip(), '0')

    def test_add_statement(self):
        grin_line = list(grin.parsing.parse(['ADD X 3','.']))
        result = grin.program_state.ProgramState(grin_line).process_line()
        self.assertEqual(result, {'X' : 3})

    def test_sub_statement(self):
        grin_line = list(grin.parsing.parse(['SUB X 3','.']))
        result = grin.program_state.ProgramState(grin_line).process_line()
        self.assertEqual(result, {'X' : -3})

    def test_mult_statement(self):
        grin_line = list(grin.parsing.parse(['MULT X 3','.']))
        result = grin.program_state.ProgramState(grin_line).process_line()
        self.assertEqual(result, {'X' : 0})

    def test_goto_out_range_statement(self):
        grin_line = list(grin.parsing.parse(['GOTO 4', '.']))
        output = StringIO()
        with patch('sys.stdout', new = output):
            with self.assertRaises(SystemExit):
                grin.program_state.ProgramState(grin_line).process_line()

    def test_goto_out_range_negative_statement(self):
        grin_line = list(grin.parsing.parse(['GOTO -4', '.']))
        output = StringIO()
        with patch('sys.stdout', new = output):
            with self.assertRaises(SystemExit):
                grin.program_state.ProgramState(grin_line).process_line()

    @patch('builtins.input', side_effect = ['3  '])
    def test_innum_statement_normal_int(self, mock_input):
        grin_line = list(
            grin.parsing.parse(['INNUM C', '.']))
        result = grin.program_state.ProgramState(grin_line).process_line()

        self.assertEqual(result, {'C' : 3})

    @patch('builtins.input', side_effect = ['-3  '])
    def test_innum_statement_negative_int(self, mock_input):
        grin_line = list(
            grin.parsing.parse(['INNUM C', '.']))
        result = grin.program_state.ProgramState(grin_line).process_line()

        self.assertEqual(result, {'C': -3})

    @patch('builtins.input', side_effect = ['-3 . 0  '])
    def test_innum_statement_float(self, mock_input):
        grin_line = list(
            grin.parsing.parse(['INNUM C', '.']))
        result = grin.program_state.ProgramState(grin_line).process_line()

        self.assertEqual(result, {'C': -3.0})

    @patch('builtins.input', side_effect = ['3 . 0  '])
    def test_innum_statement_float_positive(self, mock_input):
        grin_line = list(
            grin.parsing.parse(['INNUM C', '.']))
        result = grin.program_state.ProgramState(grin_line).process_line()

        self.assertEqual(result, {'C': 3.0})

    @patch('builtins.input', side_effect = ['random'])
    def test_instr_statement_with_words(self, mock_input):
        grin_line = list(
            grin.parsing.parse(['INSTR C', '.']))
        result = grin.program_state.ProgramState(grin_line).process_line()

        self.assertEqual(result, {'C': 'random'})

    @patch('builtins.input', side_effect = ['3'])
    def test_instr_statement_with_integers(self, mock_input):
        grin_line = list(
            grin.parsing.parse(['INSTR C', '.']))
        result = grin.program_state.ProgramState(grin_line).process_line()

        self.assertEqual(result, {'C': '3'})
if __name__ == '__main__':
    unittest.main()