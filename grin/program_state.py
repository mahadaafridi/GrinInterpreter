import grin.input
import grin.parsing
import grin.token
import grin.statement
class ProgramState:
    def __init__(self, grin_tokens):
        self._grin_tokens = grin_tokens
        self._labels = {}
        self._remove_labels()
        self._current_line = 0
        self._variables = {}
        self._return = []
        self._conditional = True

    def current_line(self) -> int:
        """returns the current line that the program is on."""
        return self._current_line

    def total_lines(self) -> int:
        """returns the total number of lines in the program (including the ending ".")"""
        return len(self._grin_tokens)

    def process_line(self) -> dict:
        """Processes the line and changes the variables based on what action is taken. It may also change
        the line number or end the programming and etc based on the action."""
        grin_line = self._grin_tokens[self.current_line()]
        #this is for the let statement
        if grin_line[0].kind().index() == 17:
            self._variables = grin.statement.Statement(grin_line, self._variables).let_statement()
        #this is for the print statement
        if grin_line[0].kind().index() == 23:
            grin.statement.Statement(grin_line, self._variables).print_statement()
        #this is for the innum statement
        if grin_line[0].kind().index() == 13:
            self._variables = grin.statement.Statement(grin_line, self._variables).innum_statement()
        #this is for the instr statement
        if grin_line[0].kind().index() == 14:
            self._variables = grin.statement.Statement(grin_line, self._variables).instr_statement()
        #this is for the end statement
        if grin_line[0].kind().index() == 5:
            exit()
        #add statement
        if grin_line[0].kind().index() == 1:
            self._variables = grin.statement.Statement(grin_line, self._variables).operation_statement("ADD")
        #subtract
        if grin_line[0].kind().index() == 25:
            self._variables = grin.statement.Statement(grin_line, self._variables).operation_statement("SUB")
        # mult
        if grin_line[0].kind().index() == 21:
            self._variables = grin.statement.Statement(grin_line, self._variables).operation_statement("MULT")
        # div
        if grin_line[0].kind().index() == 3:
            self._variables = grin.statement.Statement(grin_line, self._variables).operation_statement("DIV")
        #chekcs if there is a conditional in the line
        try:
            if grin_line[2].kind().index() == 12:
                self._conditional = grin.statement.Statement(grin_line, self._variables).conditional()
        except:
            pass
        #If the statement is gosub or goto
        if (grin_line[0].kind().index() == 8 or grin_line[0].kind().index() == 7) and (self._conditional == True):
            #if the statement is gosub it will save the line number
            if grin_line[0].kind().index() == 7:
                self._return.append(self.current_line())
            line, string_value = grin.statement.Statement(grin_line, self._variables).goto_statement(self._labels)
            #checks if the gosub/goto should go to a label or a line number
            if string_value:
                self._current_line = line
            else:
                self._current_line += line
            #ends the program if it goes to a 0 line or negative line
            if self.current_line() < 0:
                print('ERROR: Line at 0 or Below')
                exit()
            #ends the program if it tries to go to a line that is out of the range
            if self.current_line() > self.total_lines():
                print('ERROR: Line Out of Range')
                exit()
        #return statement
        elif grin_line[0].kind().index() == 24:
            try:
                self._current_line = self._return[-1] + 1
                self._return = self._return[:-1]
            except:
                print('ERROR: Nothing to Return To')
                exit()
        #goes to the next line
        else:
            self._current_line += 1
        return self._variables

    def _remove_labels(self) -> dict:
        """Removes the labels and puts them into a dictionary with their identifier and line number
        in a dictionary."""
        for line_num, line in enumerate(self._grin_tokens):
            try:
                if line[1].kind().index() == 2:
                    self._labels[line[0].value()] = line_num
                    self._grin_tokens[line_num] = self._grin_tokens[line_num][2:]
            except:
                pass
        return self._labels
__all__ = [
    ProgramState.__name__
]