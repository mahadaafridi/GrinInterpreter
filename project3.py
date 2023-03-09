# project3.py
# ICS 33 Winter 2023
# Project 3: Why Not Smile?
#
# The main module that executes your Grin interpreter.
#
# WHAT YOU NEED TO DO: You'll need to implement the outermost shell of your
# program here, but consider how you can keep this part as simple as possible,
# offloading as much of the complexity as you can into additional modules in
# the 'grin' package, isolated in a way that allows you to unit test them.

import grin


def main() -> None:
    grin_tokens = grin.Input().parse_input()
    program_state = grin.ProgramState(grin_tokens)
    while program_state.total_lines() > program_state.current_line():
        program_state.process_line()


if __name__ == '__main__':
    main()
