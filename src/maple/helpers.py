#!/usr/bin/env python3

# Standard library imports
import sys
from string import Template

# Language imports
from etc import colourise
from maple import values
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
This module provides helper functions to assist with various parsing needs.
'''


class VarTemplater(Template):
    # https://stackoverflow.com/a/1336851
    # Replace the delimiter with the values.VARIABLE_SYMBOL
    """This is a simple tweak to the string Template enging that changes the
    replacement value to values.VARIABLE_SYMBOL
    """
    delimiter = values.VARIABLE_SYMBOL


def substitute_values(expression: str, line_number: str) -> str:
    """Replace any variables in an arbitrary expression

    Args:
        expression [str]: the expression that is having any values replaced

    Returns:
        str: the expression with any variable values substituted in

    Raises:
        None
    """
    # Set up a templater for the variable by stripping quotation marks
    variable_templater = VarTemplater(
        expression.strip("'").strip('"')
    )
    # variable_templater = VarTemplater(expression.strip('"'))
    try:
        # Substitute the values in the string with variables
        expression = variable_templater.substitute(values.VARIABLES)
        # Return the variable substitutions
        return expression
    # Catch a variable substitution that doesn't make sense (eg. a variable)
    # is called for that hasn't been set.
    except KeyError as err:
        # Strip off any single-quotation marls
        err = str(err).strip("'")
        # Report back an error
        messenger.line_error(
            f'The variable {colourise.yellow(err)} is not set.',
            line_no=line_number,
            error_code=11
        )
    # Caught in cases where, for instance, the variable symbol is used on its
    # own without being escaped.
    except ValueError:
        # Report back an error
        messenger.line_error(
            f'The variable symbol - {values.VARIABLE_SYMBOL} - is provided ' +
            'wihout a variable name.',
            line_no=line_number,
            error_code=24
        )
        print('VALUE!')
        sys.exit(0)


def calculate_value(expression: str) -> str:
    """Check to see if the variable assignment is an expression that can be
    mathematically calculated.

    Args:
        expression [str]: the expression that is being checked to see if it
            can be calculated

    Returns:
        str: the variable value, either the original value or the calculated
            expression

    Raises:
        None
    """

    try:
        # Strip any lingering single quotation marks
        expression = expression.strip("'").strip('"')
        # Attempt to evaluate the expression
        expression = eval(expression)
    # Catch a NameError which is thrown if the expression can't be calculated
    except (NameError, SyntaxError):
        # Ignore and avoid conversions
        pass
    # Return the expression
    return expression
