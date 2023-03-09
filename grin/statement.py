import grin.parsing
import grin.operations
class Statement:
    def __init__(self, grin_line : list, variables : dict):
        self._grin_line = grin_line
        self._variables = variables

    def let_statement(self) -> dict:
        """This assigns the variable to the value in a dictionary. The dictionary is then returned."""
        key = self._grin_line[1].value()

        token_value = self._grin_line[2]

        self._variables[key] = self._value_finder(token_value)

        return self._variables

    def conditional(self) -> bool:
        """This enacts the conditional statement. IF the value is not allowed, not comparable, or not valid it will end the program after
        printing a error message. Otherwise, it returns a bool value if the condition is true."""
        value_1 = self._value_finder(self._grin_line[3])
        value_2 = self._value_finder(self._grin_line[5])
        operator = self._grin_line[4].text()
        if (type(value_1) == str and type(value_2) != str) or (type(value_2) == str and type(value_1) != str):
            print('ERROR: Values not comparable')
            exit()
        if operator == '>':
            result = value_1 > value_2
        if operator == '>=':
            result = value_1 >= value_2
        if operator == '<':
            result = value_1 < value_2
        if operator == '<=':
            result = value_1 <= value_2
        if operator == '=':
            result = value_1 == value_2
        if operator == '<>':
            result = value_1 != value_2
        return result
    def operation_statement(self, operation) -> dict:
        """This enacts the operation. It will find the value of the statements that are being operated on.
        Once the values are found the operation is done which will then be put into a dictionary."""
        value_1 = self._value_finder(self._grin_line[1])
        value_2 = self._value_finder(self._grin_line[2])
        key = self._grin_line[1].value()
        try:
            if operation == "ADD":
                result = grin.operations.Add(value_1, value_2).execute()
            elif operation == "SUB":
                result = grin.operations.Subtract(value_1, value_2).execute()
            elif operation == "MULT":
                result = grin.operations.Multiply(value_1, value_2).execute()
            elif operation == "DIV":
                if type(value_1) == int and type(value_2) == int:
                    result = grin.operations.Divide(value_1, value_2).execute_int_div()
                else:
                    result = grin.operations.Divide(value_1, value_2).execute_norm_div()
        except TypeError:
            print('ERROR: Type Error')
            exit()
        except ZeroDivisionError:
            print('ERROR: Zero Division Error')
            exit()
        self._variables[key] = result
        return self._variables

    def print_statement(self) -> None:
        """Prints the statement"""
        token_value = self._grin_line[1]
        print(self._value_finder(token_value))

    def innum_statement(self) -> dict:
        """IF the statement is INNUM it will first find  the value the user inputted
        if a valid integer or float. After that it will look through the variables and check if the variable already has a value
        or not and will replace that value."""

        key = self._grin_line[1].value()

        value = input("").replace(" ", "")
        other_value = value.lstrip('-').split('.')
        if other_value[0] == '':
            print('ERROR: Invalid Value')
            exit()
        if value.lstrip('-').replace('.', '', 1).isdigit():
            if '.' in value or (value.startswith('-') and '.' in value[1:]):
                value = float(value)
            else:
                value = int(value)
        else:
            print('ERROR: Invalid Value')
            exit()

        self._variables[key] = value

        return self._variables


    def instr_statement(self) -> dict:
        """Does the INSTR statement. It puts it into a dictionary with the value associated with it."""
        key = self._grin_line[1].value()
        value = input()
        self._variables[key] = value
        return self._variables

    def goto_statement(self, labels: dict) -> tuple[int,bool]:
        """The goto statement that will go to a label or a integer value. If it goes to a label
        it will return the string_value as True. It also returns the current line the program is on."""
        current_line = None
        string_value = False
        #if it is a literal string
        if self._grin_line[1].kind().index() == 20:
            try:
                current_line = labels[self._grin_line[1].value()]
                string_value = True
            except KeyError:
                print('ERROR: Non Existing Label')
                exit()
        else:
            value = self._value_finder(self._grin_line[1])
            if type(value) == str:
                try:
                    current_line = labels[value]
                    string_value = True
                except KeyError:
                    print('ERROR: Non Existing Label')
                    exit()
            else:
                current_line = value

        return current_line, string_value
    def _value_finder(self, value: 'GrinToken') -> int|str|float:
        """This function determines if the grin token given is an identifier or a literal value.
        If the grin token is a variable that has not been defined, it will make the value 0."""
        if value.kind().index() == 11:
            if value.value() in self._variables:
                value = self._variables[value.value()]
            else:
                value = 0
        else:
            value = value.value()
        return value

__all__ = [
    Statement.__name__
]