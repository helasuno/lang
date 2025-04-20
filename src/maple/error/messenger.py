#!/usr/bin/env python3

# Standard library imports
import sys
import textwrap

# Custom imports
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
A simple module to handle error and warning messages.
'''

ERROR_MESSAGE_WRAP = 50


def simple_warning(message, error_code=0):
    """Report back a simple warning message.

    Args:
        message [str]: the message to be printed
        error_code [int]: the error code, 0 signifying that no error code was
            passed

    Returns:
        N/A

    Raises:
        None
    """

    # Create a wrapped version of the warning message that is no more than
    # ERROR_MESSAGE_WRAP characters wide.
    message = textwrap.fill(message, ERROR_MESSAGE_WRAP)

    if error_code == 0:
        # Print out the error message in red
        print(
            colourise.yellow('\n[Warning]\n') + message + '\n'
        )
    else:
        # Print out the error message in red with the error code
        print(
            colourise.yellow('\n[Warning]\n') +
            message + '\n' +
            colourise.magenta(f'[Code: {error_code}]\n')
        )


def line_warning(message, line_no, error_code=0):
    """Report back a simple warning message.

    Args:
        message [str]: the message to be printed
        line_no [str]: the line number triggering the warning
        error_code [int]: the error code, 0 signifying that no error code was
            passed

    Returns:
        N/A

    Raises:
        None
    """

    # Create a wrapped version of the warning message that is no more than
    # ERROR_MESSAGE_WRAP characters wide.
    message = textwrap.fill(message, ERROR_MESSAGE_WRAP)

    if error_code == 0:
        # Print out the error message in red
        print(
            colourise.yellow(f'\n[Warning on Line {line_no}]\n') +
            message + '\n'
        )
    else:
        # Print out the error message in red with the error code
        print(
            colourise.yellow(f'\n[Warning on Line {line_no}]\n') +
            message + '\n' +
            colourise.magenta(f'[Code: {error_code}]\n')
        )


def simple_error(message, error_code=0, exit=True):
    """Report back a simple error message and offer the ability to exit from
        execution.

    Args:
        message [str]: the message to be printed
        error_code [int]: the error code, 0 signifying that no error code was
            passed
        exit [bool]: whether to exit execution, defaults to True

    Returns:
        N/A

    Raises:
        None
    """

    # Create a wrapped version of the warning message that is no more than
    # ERROR_MESSAGE_WRAP characters wide.
    message = textwrap.fill(message, ERROR_MESSAGE_WRAP)

    if error_code == 0:
        # Print out the error message in red
        print(
            colourise.red('\n[Error]\n') + message + '\n'
        )
    else:
        # Print out the error message in red with the error code
        print(
            colourise.red('\n[Error]\n') +
            message + '\n' +
            colourise.magenta(f'[Code: {error_code}]\n')
        )

    # If exit remains True, exit the script
    if exit:
        sys.exit(0)


def line_error(message, line_no, error_code=0, exit=True):
    """Report back a simple error message and offer the ability to exit from
        execution.

    Args:
        message [str]: the message to be printed
        line_no [str]: the line number triggering the warning
        error_code [int]: the error code, 0 signifying that no error code was
            passed
        exit [bool]: whether to exit execution, defaults to True

    Returns:
        N/A

    Raises:
        None
    """

    # Create a wrapped version of the warning message that is no more than
    # ERROR_MESSAGE_WRAP characters wide.
    message = textwrap.fill(message, ERROR_MESSAGE_WRAP)

    if error_code == 0:
        # Print out the error message in red
        print(
            colourise.red(f'\n[Error on Line {line_no}]\n') + message + '\n'
        )
    else:
        # Print out the error message in red with the error code
        print(
            colourise.red(f'\n[Error on Line {line_no}]\n') +
            message + '\n' +
            colourise.magenta(f'[Code: {error_code}]\n')
        )

    # If exit remains True, exit the script
    if exit:
        sys.exit(0)
