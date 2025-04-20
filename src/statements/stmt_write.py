#!/usr/bin/env python3

# Standard library imports
import sys

# Language imports
from maple import (helpers, values)
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
This modules handles the writing of content to the screen
'''


def stat_moderator(
                    operator: str,
                    statmod: str,
                    output: str,
                    line_number: str) -> str:
    """Return strings for printing that are modified as per the statmod
    included.

    Args:
        operator [str]: the operator for the statement modification
        statmod [str]: the statmod itself
        output [str]: the string that will be written that will be modified
        line_number [str]: the script line number, helpful for error reporting

    Returns:
        output [str]: the modified string that then gets printed

    Raises:
        None
    """

    # If the operator isn't valid...
    if operator != values.VALID_OPERATORS['statmod']:
        # Report that back
        messenger.line_error(
            f'The operator provided to modify the statement ({operator}) is ' +
            'not valid.',
            line_no=line_number,
            error_code=18
        )

    # Split the statmod by the statmod_splitter operator
    statmod = statmod.split(values.VALID_OPERATORS['statmod_splitter'])

    # Thanks to https://stackoverflow.com/a/522578.
    # We need to loop over the statmods and remove any lingering quotation
    # marks.
    for index, mod in enumerate(statmod):
        # Strip off any lingering quotation marks.
        statmod[index] = mod.strip('"')

    # Get index of lower as we need to check that it is at the front of the
    # list.
    try:
        lower_index = statmod.index('lower')
    except ValueError:
        # Set the lower index to None since it doesn't exist
        lower_index = None

    # Get index of upper as we need to check that it is at the front of the
    # list.
    try:
        upper_index = statmod.index('upper')
    except ValueError:
        # Set the lower index to None since it doesn't exist
        upper_index = None

    # If the lower index is None, we can assume that we don't have it so move
    # along
    if lower_index is None:
        pass
    # If the lower index is greater than zero, that is, it's not the first
    # element...
    elif lower_index > 0:
        # Throw a warning
        messenger.line_warning(
            'The lower statement modifier is located in position ' +
            f'{lower_index+1} and should be at the beginning. Expect some ' +
            'unexpected output.',
            line_no=line_number,
            error_code=20
        )

    # If the lower index is None, we can assume that we don't have it so move
    # along
    if upper_index is None:
        pass
    # If the upper index is greater than zero, that is, it's not the first
    # element...
    elif upper_index > 0:
        # Throw a warning
        messenger.line_warning(
            'The upper statement modifier is located in position ' +
            f'{upper_index+1} and should be at the beginning. Expect some ' +
            'unexpected output.',
            line_no=line_number,
            error_code=20
        )

    for mod in statmod:
        # Match the statmod
        match mod:
            # Statmod: blue
            case 'blue':
                # Return blue text
                output = colourise.blue(output)
            # Statmod: green
            case 'green':
                # Return green text
                output = colourise.green(output)
            # Statmod: lower
            case 'lower':
                # Return a lower case version
                output = output.lower()
            # Statmod: magenta
            case 'magenta':
                output = colourise.magenta(output)
            # Statmod: red
            case 'red':
                # Return red text
                output = colourise.red(output)
            # Statmod: upper
            case 'upper':
                # Return an upper case version
                output = output.upper()
            # Statmod: yellow
            case 'yellow':
                # Return yellow text
                output = colourise.yellow(output)
            case _:
                # Create a list of valid statmods for the write statement
                valid_statmods = ', '.join(values.VALID_STATMODS_WRITE)
                # Print out an error if we've got an invalid statmod
                messenger.line_error(
                    'The statement modifier provided is not valid. Valid ' +
                    'statement modifiers include ' +
                    f'{colourise.yellow(valid_statmods)}.',
                    line_no=line_number,
                    error_code=19
                )
    # Return the output
    return output


def stmt_write(tokens: list, newline=True):
    """Write a string to the screen/console

    Args:
        tokens [list]: the list of tokens on the line with the write statement
            call
        newline: if True [the default], move to the next line and if False,
            don't move to the next line. This allows the function to serve
            both the write and writeln statement.

    Returns:
        N/A

    Raises:
        None
    """

    # Get the string to be written to the screen
    output = tokens[2]['token_value']

    # Get the line number for error reporting
    line_number = tokens[2]['script_line_number']

    # Substitute any variables in the string
    output = helpers.substitute_values(output, line_number)

    # Calculate the possible output in case it was a math
    # expression
    output = helpers.calculate_value(output)

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
        # Pass off the stat_moderator for the write statement
        output = stat_moderator(
            stat_mod_op, stat_mod_value, output, line_number
        )

    if newline:
        print(output)
    else:
        print(output, end='')
    # Flush the output: https://stackoverflow.com/questions/21886233/time-
    # sleepx-not-working-as-it-should. Doing this allows the pause statement
    # to work as it should.
    sys.stdout.flush()
