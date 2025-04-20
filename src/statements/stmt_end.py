#!/usr/bin/env python3

# Standard library imports
import sys

# Language imports
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
This module handles the end statement.
'''


def stmt_end(tokens: list):
    """End the execution of the script via an end statement call

    Args:
        tokens [list]: the list of tokens on the line with the end statement
            call

    Returns:
        N/A

    Raises:
        None
    """

    # Get the line number for error reporting
    line_number = tokens[0]['script_line_number']
    # Get the full line of code for error reporting
    full_loc = tokens[0]['full_line_of_code'].strip('\n')
    # Get the final token to check if it's a NEWLINE token
    final_token_type = tokens[-1]['token_type'][1]

    # If the final token is a NEWLINE token...
    if final_token_type == 'NEWLINE':
        # Remove it. This last token is unnecessary and potentially complicates
        # parsing.
        tokens.pop(-1)

    # If there are still more than two tokens after removing the NEWLINE, we
    # can assume that there is an issue with the line of code
    if len(tokens) > 2:
        messenger.line_error(
            'The end statement contains more than just a line number and ' +
            f'the end statement: {full_loc}',
            line_no=line_number,
            error_code=13
        )
    # At this point, we can assume that things are fine and do the work of the
    # end statement, that is, end the execution.
    sys.exit(0)
