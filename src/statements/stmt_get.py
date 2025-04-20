#!/usr/bin/env python3

# Standard library imports

# Language imports
from maple import (helpers, values)
from statements import stmt_set

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
This module handles the get statement.
'''


def stmt_get(tokens: list):
    """Get user input and set a variable accordingly

    Args:
        tokens [list]: the list of tokens on the line with the get statement
            call

    Returns:
        N/A

    Raises:
        None
    """

    # Get the line number
    line_number = tokens[0]['script_line_number']
    # Get the variable name that will house the input from the prompt
    variable_name = tokens[2]['token_value']
    # Get the prefix of the variable to make sure that they aren't using one
    # of the builtin variables.
    variable_prefix = variable_name[0:len(values.VARIABLE_PROHIBITED_PREFIX)]
    # Get the assignment operator so that we can check that the assignment
    # operator is used.
    assignment_operator = tokens[3]['token_value']
    # Get the variable value by an input call
    variable_value = input(tokens[4]['token_value'].strip('"'))

    # Check the statement to make sure that it is syntactically correct
    stmt_set.stmt_check(
        variable_prefix, assignment_operator, line_number, variable_name
    )

    # Substitute any variable values
    variable_value = helpers.substitute_values(variable_value, line_number)

    # Check to see if the variable_value is an expression that can be and
    # needs to be calculated
    variable_value = helpers.calculate_value(variable_value)

    # Store the variable
    values.VARIABLES[variable_name] = variable_value
