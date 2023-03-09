# Reads the input from the shell and converts it into tokens
import grin.parsing
import grin.lexing
class Input:
    def __init__(self):
        self._list = []
        self._line = None

    def read_input(self) -> list[str]:
        """This reads the input and puts it into a list of strings."""
        while self._line != '.':
            self._line = input().strip()
            self._list.append(self._line)
        return self._list

    def parse_input(self) -> 'list[list[GrinToken]]':
        """This parses through the input and loops though all the tokens to ensure that none
        of them have errors. If there are errors it will print an error message."""
        try:
            grin_tokens = list(grin.parsing.parse(self.read_input()))
            for line in grin_tokens:
                line
        except (grin.parsing.GrinParseError, grin.lexing.GrinLexError) as e:
            print(e)
            exit()


        return grin_tokens


__all__ = [
    Input.__name__
]



