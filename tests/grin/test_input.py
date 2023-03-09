import unittest
from unittest.mock import patch

import grin.parsing
from grin.input import Input
from io import StringIO
class TestInput(unittest.TestCase):

    @patch('builtins.input', side_effect = ['LET MESSAGE "BOO"', 'PRINT MESSAGE', '.'])
    def test_input_is_read(self, mock_input):
        self.assertEqual(Input().read_input(), ['LET MESSAGE "BOO"', 'PRINT MESSAGE', '.'])


    @patch('builtins.input', side_effect = ['LET MESSAGE "BOO"', '', '.', 'randomstuff'])
    def test_input_after_end_ignored(self, mock_input):
        self.assertEqual(Input().read_input(), ['LET MESSAGE "BOO"', '', '.'])

    @patch('builtins.input', side_effect = ['LET DSF sad sadf asd das', '.'])
    def test_error_message_sys_exit(self, mock_input):
        output = StringIO()
        with patch('sys.stdout', new=output):
            with self.assertRaises(SystemExit):
                self.assertRaises(grin.parsing.GrinParseError, Input().parse_input())

if __name__ == '__main__':
    unittest.main()