#!/usr/bin/env python3

# Standard library imports

# Language imports
from maple import (helpers, values)
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
This module handles the set statement and various variable related functions
that are needed outside of the set statement (eg. variable value substitution
in a write statement).
'''


def stmt_check(
            prefix: str,
            operator: str,
            line_number: str,
            variable_name: str):
    """Check that we have a valid statement line

    Args:
        prefix [str]: the prefix on the variable name, used to make sure that
            the name of a reserved variable isn't used
        operator [str]: the operator used to assign the value

    Returns:
        N/A

    Raises:
        None
    """

    # If the variable prefix matches the prohibited prefix...
    if prefix == values.VARIABLE_PROHIBITED_PREFIX:
        # Report an error
        messenger.line_error(
            f'The variable ({variable_name}) is invalid because it starts ' +
            f'with {values.VARIABLE_PROHIBITED_PREFIX}.',
            line_no=line_number,
            error_code=15
        )

    # If the operator is not an assignment operator...
    if operator != values.VALID_OPERATORS['assignment']:
        # Report an error
        messenger.line_error(
            f'The variable ({variable_name}) is assigned with {operator} ' +
            f'and you need to use {values.VALID_OPERATORS["assignment"]}.',
            line_no=line_number,
            error_code=16
        )

    if variable_name in values.STATEMENT_NAMES:
        # Report an error
        messenger.line_error(
            f'The variable ({variable_name}) is invalid as the name is the ' +
            'same as a statement name.',
            line_no=line_number,
            error_code=17
        )


def stmt_set(tokens: list):
    """Set a variable via the set statement

    Args:
        tokens [list]: the list of tokens on the line with the end statement
            call

    Returns:
        N/A

    Raises:
        None
    """

    # Get the line number
    line_number = tokens[0]['script_line_number']
    # Get the full line of code
    # full_loc = tokens[0]['full_line_of_code'].strip('\n')
    # Get the variable name
    variable_name = tokens[2]['token_value']
    # Get the prefix of the variable to make sure that they aren't using one
    # of the builtin variables.
    variable_prefix = variable_name[0:len(values.VARIABLE_PROHIBITED_PREFIX)]
    # Get the assignment operator so that we can check that the assignment
    # operator is used.
    assignment_operator = tokens[3]['token_value']
    # Get the variable value
    variable_value = tokens[4]['token_value'].strip('"')

    # Check the statement to make sure that it is syntactically correct
    stmt_check(
        variable_prefix, assignment_operator, line_number, variable_name
    )

    # Substitute any variable values
    variable_value = helpers.substitute_values(variable_value, line_number)

    # Check to see if the variable_value is an expression that can be and
    # needs to be calculated
    variable_value = helpers.calculate_value(variable_value)

    # Store the variable
    values.VARIABLES[variable_name] = variable_value
