#!/usr/bin/env python3

# Standard library imports

# Language imports
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
This module serves to do checks on parts of a script that might be common
across modules (for instance, checking for a valid statmod operator).
'''


def check_statmod_operator(operator, line_number):
    """Check the token value to see if it is a valid statmod operator

    Args:
        statmod_token [str]: the value of the statmod operator
        line_number [str]: the line number of the code for reporting the error

    Returns:
        N/A

    Raises:
        None
    """

    # If the operator is not valid
    if operator != values.VALID_OPERATORS['statmod']:
        # Report that back
        messenger.line_error(
            'The operator provided to modify the statement ' +
            f'({operator}) is not valid.',
            line_no=line_number,
            error_code=18
        )
