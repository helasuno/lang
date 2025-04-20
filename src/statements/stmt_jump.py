#!/usr/bin/env python3

# Standard library imports
# import sys

# Language imports
from maple import (tree, xylem)
from maple.error import messenger
from etc import colourise

'''Copyright 2024-2025 Bryan Smith.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

-- Description --
This module handles the end statement.
'''


def stmt_jump(tokens: list):
    """End the execution of the script via an end statement call

    Args:
        tokens [list]: the list of tokens on the line with the end statement
            call

    Returns:
        N/A

    Raises:
        None
    """

    # Get the line number
    line_number = tokens[2]['script_line_number']
    # Get the location
    jump_location = tokens[2]['token_value'].strip('"')

    # Try to cast the jump_location to an integer as the xylem.set_execution_
    # location() function requires an integer. Additionally, this allows us
    # to check that it is a valid line number and not, say, a string of
    # letters.
    try:
        jump_location_integer = int(jump_location)
    # If it was not castable to an integer, throw an error
    except ValueError:
        # Report an error
        messenger.line_error(
            'The line number that you are planning to jump to is not a ' +
            f'number: {colourise.yellow(jump_location)}.',
            line_no=line_number,
            error_code=21
        )

    # Get the script line numbers
    script_line_numbers = tree.get_line_numbers()
    # Join the line numbers in the script for error reporting
    valid_line_numbers = ', '.join(script_line_numbers)

    # If the jump_location is not a verifiable line numbers...
    if not tree.verify_line_number(jump_location):
        # Report an error
        messenger.line_error(
            'The line that you have requested be jumped to - ' +
            f'{jump_location} - does not exist. Valid line numbers include ' +
            f'{valid_line_numbers}.',
            line_no=line_number,
            error_code=23
        )

    # If we've gotten here, set the execution location to the jump_location as
    # we can assume that everything is okay.
    xylem.set_execution_location(jump_location_integer)
