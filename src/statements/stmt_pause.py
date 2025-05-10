#!/usr/bin/env python3

# Standard library imports
import time

# Language imports
from maple import (doctor, helpers, values)
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
This modules handles pausing the execution of the script.
'''


def stat_moderator(
                    operator: str,
                    statmod: str,
                    pause_length: str,
                    line_number: str):

    """Modify the pause statement where needed.

    Args:
        operator [str]: the operator for the statement modification
        statmod [str]: the statmod itself
        pause_length [int]: the length of the pause to be modified
        line_number [str]: the script line number, helpful for error reporting

    Returns:
        output [str]: the modified string that then gets printed

    Raises:
        None
    """

    # Check with the doctor to see if the statmod operator is valid
    doctor.check_statmod_operator(operator, line_number)

    # Strip of the quotation marks from the statmod
    statmod = statmod.strip('"')

    # Start modifying
    match statmod:
        # Countdown
        case 'countdown':
            # For each number in a reversed list of numbers starting with the
            # pause_length.
            for number in reversed(range(pause_length)):
                # Print the countdown
                print(
                    f'{str(number+1)}...',
                    end='\r'
                )
                # Pause for a second
                time.sleep(1)
        case _:
            # Create a list of valid statmods for the write statement
            valid_statmods = ', '.join(values.VALID_STATMODS_PAUSE)
            # Print out an error if we've got an invalid statmod
            messenger.line_error(
                'The statement modifier provided is not valid. Valid ' +
                'statement modifiers include ' +
                f'{colourise.yellow(valid_statmods)}.',
                line_no=line_number,
                error_code=19
            )


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

    # Convert the pause length to an integer
    pause_length = int(pause_length)

    # Try to get the statmod
    try:
        # Hold the stat mod operator
        stat_mod_op = tokens[3]['token_value']
        # Get the stat mod value
        stat_mod_value = tokens[4]['token_value']
    # Catch an index error
    except IndexError:
        # Ignore it by setting the statmod operator and value to None
        stat_mod_op = None
        stat_mod_value = None

    # If the operator is not None, that is, there is an operator...
    if stat_mod_op is not None:
        # Pass off the stat_moderator for the pause statement
        stat_moderator(stat_mod_op, stat_mod_value, pause_length, line_number)
    else:
        # Pause the execution of the script if there is no statmod
        time.sleep(pause_length)
