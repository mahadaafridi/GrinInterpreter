class Operation:
    def __init__(self, value1 : int|float|str, value2: int|float|str):
        self._value1 = value1
        self._value2 = value2

    def value_1(self) -> int|float|str:
        """Returns the first value."""
        return self._value1

    def value_2(self) -> int|float|str:
        """Returns the second value"""
        return self._value2


class Add(Operation):
    def execute(self) -> int|float|str:
        """Executes the statement"""
        result = self.value_1() + self.value_2()
        return result

class Subtract(Operation):
    def execute(self) -> int|float|str:
        """Executes the statement"""
        result = self.value_1() - self.value_2()
        return result

class Divide(Operation):
    def execute_int_div(self) -> int|float|str:
        """Executes the int division"""
        result = self.value_1() // self.value_2()
        return result
    def execute_norm_div(self) -> int|float|str:
        """Executes the normal division"""
        result = self.value_1() / self.value_2()
        return result

class Multiply(Operation):
    def execute(self) -> int|float|str:
        """Executes the statement"""
        result = self.value_1() * self.value_2()
        return result

