#!/usr/bin/env python3

# Language imports
from maple import arborist
from maple.error import (codes, messenger)
from etc import (colourise, interpreter_flags, global_values)

# Standard library imports
import signal
import sys
import textwrap
# import platform

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
A module that does simple checks for the interpreter.
'''


# Thanks to https://stackoverflow.com/a/6990487 for this one
def catch_interrupt():
    '''A simple handler for KeyboardInterrupts. This will effectively take
    control from Python and catch all of them.

    Args:
        None

    Returns:
        None

    Raises:
        None
    '''

    def interrupt_handler(signal, frame):
        '''A nested method that handles the actual interruption based on the
        signal

        Args:
            signal: This is the signal number
            frame: This is the stack frame. It's unclear what this is but it
              seems to be required and it is largely ignored at this point.

        Returns:
            None

        Raises:
            None
        '''

        messenger.simple_error(
            'Interrupt caught, exiting...',
            error_code=1
        )
    signal.signal(signal.SIGINT, interrupt_handler)


def check_flags(opts, script_name):
    '''A simple check of the options for the interpreter

    Args:
        opts [list]: a list of options passed as flags to the interpreter

    Returns:
        modes [dict]: a dictionary with mode settings (eg. dev mode)

    Raises:
        None
    '''

    modes = {
        'dev_mode': False,
        'performance_check': False
    }

    # Loop over the options
    for opt in opts:
        # Store the flag
        opt_flag = opt[0]
        # Store the value of the flag (where necessary)
        opt_value = opt[1]
        # Match the flags
        match opt_flag:
            case '-d':
                modes['dev_mode'] = True
            case '-e':
                codes.error_elaborator(opt_value)
            case '-h':
                print(colourise.yellow('\n:: HELP ::'))
                print(
                    f'{global_values.LANG_NAME} {global_values.LANG_VERSION}'
                )
                print(colourise.green('\n\nDEVELOPER FLAGS'))
                print(
                    'These are flags that are helpful for people working on ' +
                    'the language itself.\n'
                )
                print(textwrap.fill(
                    f'{colourise.cyan("-d")}  ' +
                    'Run in developer mode. This outputs information about ' +
                    'tokenisation and other "inner workings."',
                    subsequent_indent='\t'
                ))
                print(textwrap.fill(
                    f'{colourise.cyan("-p")}  ' +
                    'Run a performance check. This outputs information ' +
                    'about how well Maple and other parts of the ' +
                    'interpreter are working.',
                    subsequent_indent='\t'
                ))
                print(colourise.green('\n\nUSER FLAGS'))
                print(
                    'These are flags that are helpful for people writing ' +
                    'scripts and/or general users.\n'
                )
                print(textwrap.fill(
                    f'{colourise.cyan("-e [error code]")}  ' +
                    'Get elaborations on errors. If you find yourself ' +
                    'confused by an error message, you can run this and ' +
                    'pass an error code to get more information and sample' +
                    'code (where relevant).',
                    subsequent_indent='\t'
                ))
                print(textwrap.fill(
                    f'{colourise.cyan("-r")}  ' +
                    'Reline script. This relines the script before ' +
                    'execution, ensuring that the script follows convention.',
                    subsequent_indent='\t'
                ))
                print(textwrap.fill(
                    f'{colourise.cyan("-v")}  ' +
                    'Version information. This outputs information about ' +
                    'the language.',
                    subsequent_indent='\t'
                ))
                print('')
                sys.exit(0)
            case '-p':
                modes['performance_check'] = True
            case '-r':
                interpreter_flags.reline(script_name)
            case '-v':
                print(
                    f'{global_values.LANG_NAME} ' +
                    f'{global_values.LANG_VERSION} ' +
                    f'({global_values.PLAT_SYSTEM}, {global_values.PLAT_ARCH})'
                )
                print(
                    f'Python {".".join(global_values.PYTHON_VERSION)}'
                )
                if global_values.LANG_DEV_VERSION is True:
                    print(
                        colourise.red(
                            'NOTE: THIS IS A DEVELOPMENT VERSION OF THE ' +
                            'LANGUAGE. EXPECT THAT THINGS WILL BREAK.'
                        )
                    )
                sys.exit(0)

    return modes


def check_python_version():
    '''A function to check that we are running with an appropriate version of
    Python under the hood.

    Args:
        None

    Returns:
        None

    Raises:
        None
    '''

    # If the version of Python installed is less than the minimum...
    if global_values.PYTHON_VERSION[0] == '3' and \
            int(global_values.PYTHON_VERSION[1]) < \
            global_values.PYTHON_VERSION_MINIMUM_MINOR:
        # Report an error
        messenger.simple_error(
            'Your version of Python (' +
            f'{".".join(global_values.PYTHON_VERSION)}) ' +
            'is too old. You need to be running a version of Python >= ' +
            f'{global_values.PYTHON_VERSION_MINIMUM}.'
        )
        # Abandon ship
        sys.exit(0)


def run_arborist_checks(lines_of_script):
    '''A function to run a series of arborist checks on the script

    Args:
        lines_of_script [list]: the lines of the script that need to be
            checked by the arborist

    Returns:
        None

    Raises:
        None
    '''

    # First up, let's check to make sure that each line has a unique line
    # number
    unique, non_unique_line = arborist.check_unique_line_numbers(
        lines_of_script)
    # If the lines are not unique, throw an error
    if not unique:
        messenger.simple_error(
            'There are duplicate line numbers in the script: ' +
            non_unique_line,
            error_code=2
        )

    # Next up, check to see if the line numbers are sequential
    seq_lines, lines, sort_lines = arborist.check_sequential_line_numbers(
        lines_of_script)
    if not seq_lines:
        # If the lines are not sequential, throw an error
        messenger.simple_error(
            'The lines are not sequentially ordered in the script. ' +
            f'You\'ve scripted {", ".join(lines)} and the correct ' +
            f'ordering should be {", ".join(sort_lines)}.',
            error_code=3
        )

    # Next, check to see if the line numbers are valid numbers
    valid_line, line, line_no = arborist.check_valid_line_numbers(
        lines_of_script)
    if not valid_line:
        # If the lines are not valid, throw an error
        messenger.simple_error(
            f'A line of code has an invalid line number: {line}.',
            error_code=4
        )

    valid_end_line, line_no, stmt = arborist.check_for_end_statement(
        lines_of_script)
    if not valid_end_line:
        # If the last line is not an end statement, throw an error
        messenger.line_error(
            f'{stmt} is not an end statement. The last line of your ' +
            'code needs to be an end statement.',
            line_no=line_no,
            error_code=5
        )

    valid_line_multiples, first_number = arborist.check_for_multiples(
        lines_of_script)
    if not valid_line_multiples:
        messenger.simple_warning(
            'The line numbers are not multiples of each other. ' +
            f'Each line is not a multiple of {first_number}.',
            error_code=6
        )

    valid_nonzero_start = arborist.check_for_nonzero_start(
        lines_of_script)
    if not valid_nonzero_start:
        messenger.simple_error(
            'The first line starts with 0. You need to start the first' +
            'line with an integer greater than 0.',
            error_code=7
        )
