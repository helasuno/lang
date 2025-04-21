#!/usr/bin/env python3

# Standard library imports
import time

# Language imports
from maple import helpers
from maple.error import messenger

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
This modules handles pausing the execution of the script.
'''


def stmt_pause(tokens: list):
    """Pause the execution of a script for a period of time.

    Args:
        tokens [list]: the list of tokens on the line with the write statement
            call

    Returns:
        N/A

    Raises:
        None
    """

    # Get the requested pause length
    pause_length = tokens[2]['token_value']
    # Get the line number
    line_number = tokens[0]['script_line_number']

    # Substitute variables in the pause length
    pause_length = helpers.substitute_values(pause_length, line_number)
    # Calculate the expression if it needs to be calculated
    pause_length = helpers.calculate_value(pause_length)

    # If the pause is not numeric...
    if not str(pause_length).isnumeric():
        # Throw an error
        messenger.line_error(
            f'The length of the pause requested ({pause_length}) is not a ' +
            'valid number.',
            line_no=line_number,
            error_code=14
        )

    # Pause the execution of the script
    time.sleep(int(pause_length))
