#!/usr/bin/env python3

# Standard library imports
# import pprint
# import sys

# Language imports
from maple import (tree, values)
from maple.error import messenger
from statements import (
    stmt_end,
    stmt_get,
    stmt_jump,
    stmt_pause,
    stmt_set,
    stmt_write
)

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
This Maple module serves to start calling modules from statements based on the
strcture of the TOKEN_TREE. This works like a tree's xylem by moving tokens
(ie. nutrients) around the statements/ folder, calling functions to start doing
things.
'''


def set_execution_location(start_location=-1):
    """Check to make sure that we are in the right place in the token tree.
    This is the first method to be called in the xylem module to make sure
    that we are executing the statements as need be.

    Args:
        start_location: the line number to start executing from which is
            helpful in case something like a jump statement is called. This
            defaults to -1 which indicates that we are to start from the
            beginning of the tree.

    Returns:
        N/A

    Raises:
        None
    """

    # Get the tree
    stmts = tree.get_tree()

    # For each key (line number)/value (line tokens) pair in the tree
    for line_no, line_tokens in stmts.items():
        # Get an integer value of the line number so we can do comparisons as
        # the line numbers in the trees are held as strings
        line_no = int(line_no)
        # If the start_location is not -1, we start somewhere specific in the
        # tree.
        if start_location != -1:
            # If the start location is less than the line number, we have a
            # statement that should be executed (ie. if the start location
            # is 20 and the line number is 30, we should execute line 30).
            if start_location <= line_no:
                # execute_statements(line_tokens)
                call_statements(line_tokens)
        # Otherwise, we are starting at the beginning of the tree
        else:
            # execute_statements(line_tokens)
            call_statements(line_tokens)


def call_statements(tokens: list):
    """Start calling statement modules to enable the execution of the script.
    It's been a journey to get here but we're finally ready to start executing
    things.

    Args:
        tokens [list]: a list of tokens for the individual line of the script.
            This is broken down into its necessry values and then passed to
            stmt_* modules to execute statement calls in the script.

    Returns:
        N/A

    Raises:
        None
    """
    # Get the line number in case an unknown statement is provided
    line_number = tokens[0]['script_line_number']

    # Get the name of the statement call. This is necessarily the second token
    statement_name = tokens[1]['token_value']

    # Check that the statements in the script are indeed valid statement names
    if statement_name not in values.STATEMENT_NAMES:
        messenger.line_error(
            f'The statement name "{statement_name}" is not a valid ' +
            'statement name.',
            line_no=line_number,
            error_code=12
        )

    try:
        # Match the statement name from the line and pass the tokens to the
        # statement module.
        match statement_name:
            case 'end':
                stmt_end.stmt_end(tokens)
            case 'get':
                stmt_get.stmt_get(tokens)
            case 'jump':
                stmt_jump.stmt_jump(tokens)
            case 'pause':
                stmt_pause.stmt_pause(tokens)
            case 'set':
                stmt_set.stmt_set(tokens)
            case 'write':
                stmt_write.stmt_write(tokens, False)
            case 'writeln':
                stmt_write.stmt_write(tokens)
            case _:
                # This is here just in case something unanticipated happens
                pass
    except RecursionError:
        messenger.simple_error(
            'The script is caught in a loop and to keep you safe, the app ' +
            'needs to exit.',
            error_code=22
        )
