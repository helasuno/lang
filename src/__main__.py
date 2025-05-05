#!/usr/bin/env python3

# Standard library imports
import getopt
import sys
import time

# Language imports
from etc import (colourise)
from interpreter import checks
from maple import (arborist, data, planter, xylem)
from maple.error import (messenger)

'''Copyright 2024-2025 Bryan Smith.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

-- Description --
The main entry point for the language. This is the "manager" that calls
external functions to start executing the script and checking for language
compliance.
'''

# A global catch all handler for interrupts. This prevents, for instance, a
# KeyboardInterrupt from being called by Python and thus outputting Python
# errors. Set this up from the outset so that all interrupts are handled right
# from the moment the interpreter is invoked.
checks.catch_interrupt()

# Check the minimum version of Python from the interpreter checks
checks.check_python_version()

# This is a workaround for the limits of recursion built into Python.
# The solution here is bad so it's commented out.
# sys.setrecursionlimit(10000)

# Try to open up the script
# Get the system arguments
sys_args = sys.argv[1:]
# Set the options here:
#   -d (dev mode)
#   -e [error_code] (error code elaboration for [error_code])
#   -h (help)
#   -p (performance check)
#   -r (reliner)
#   -v (version)
short_opts = 'de:hprv'

# Try to get the options and arguments
try:
    # Get the options and arguments
    opts, args = getopt.getopt(sys_args, short_opts)
# If the flag is invalid, error out
except getopt.GetoptError:
    messenger.simple_error(
        'Option passed to the interpreter is not valid. Pass ' +
        f'{colourise.yellow("-h")} to the interpreter to get a list of ' +
        'valid flags.'
    )
    sys.exit(0)

# Try to get the script name and leave blank if need be (ie. a user doesn't)
# input a script name.
try:
    # Get the script name from the args
    script_name = args[0]
except IndexError:
    # Pass an empty script name if there isn't one passed
    script_name = ''

# Check the options to see if any need to be addressed in the execution of
# the interpreter.
modes = checks.check_flags(opts, script_name)

# Whether we are running in dev mode
dev_mode = modes['dev_mode']

# Whether we are running a performance check
performance_check = modes['performance_check']


def main():
    """Start the ball rolling by opening the script, doing some quick checks
    and passing off to xylem to start parsing.

    Args:
        tokens [list]: the list of tokens on the line with the end statement
            call

    Returns:
        N/A

    Raises:
        None
    """
    try:
        # With an open script handler
        with open(script_name, 'r') as script:
            # Read the script
            contents = script.read()
            # Split the script into lines which will themselves serves as
            # branches in Maple.
            lines_of_script = contents.split('\n')

            # Time to hand over to the arborist to check in on the script
            # before the token tree is planted (ie. built). Do this by passing
            # the lines to the checks module that runs through the functions
            # in the arborist.
            checks.run_arborist_checks(lines_of_script)

            # Prune the comments from the script so that they don't get parsed
            # by the planter. This is helpful, as well, in minimising the
            # number of possible errors as any uncaught parsing errors that
            # might be triggered by a comment are removed
            lines_for_parsing = arborist.prune_comments(lines_of_script)

            # Now, we turn over to the planter to start building, bit by bit,
            # the tokens first and then the TOKEN_TREE which serves as the
            # basis for executing commands. If performance check is enabled,
            # calculate the timing of the tokenisation instead.
            if performance_check:
                start_time = time.time()
                # Run a tokenisation performance check
                tokenisation_data = data.perf_tokenisation(lines_for_parsing)
                # Print a new line
                print('\r')
                # Run a tree planting performance check
                tree_data = data.perf_tree_planting()
                # Print a new line
                print('\n')
                # Print out the data
                data.print_dev_data(
                    script_name,
                    tokenisation_data['average'],
                    tokenisation_data['median'],
                    tokenisation_data['stdev'],
                    tree_data['average'],
                    tree_data['median'],
                    tree_data['stdev']
                )
                end_time = time.time()
                perf_total_time = end_time - start_time
                print(
                    colourise.cyan(
                        f':: Total Run Time: {perf_total_time} seconds'
                    )
                )
                # Exit as we aren't executing the script
                sys.exit(0)
            # Otherwise, tokenise and build the TOKEN_TREE without calculating
            # how long it takes.
            else:
                # Build the tokens
                token_planter = planter.build_tokens(lines_for_parsing)
                # If index 0 is True, it means that the tokeniser has errored
                # out so report the error.
                if token_planter[0] is True:
                    # Index 3 is the line number, index 1 is the error message
                    messenger.line_error(
                        token_planter[1],
                        line_no=token_planter[3],
                        error_code=8
                    )
                # Plant the tree
                planter.build_tree()

            # If developer mode is enabled...
            if dev_mode:
                data.get_token_data(script_name)
                # Exit as we aren't executing the script
                sys.exit(0)

            # Start executing statements by checking where we need to start
            # Since we are starting here at the start, we don't pass a value to
            # set_execution_location() since we aren't starting at a specific
            # spot.
            xylem.set_execution_location()

    except FileNotFoundError:
        # This will catch any call where there is no script passed and/or one
        # not found.
        if script_name == "":
            error_message = 'No script passed to the interpreter.'
        else:
            error_message = 'The script could not be found. Double check ' + \
                'that the file exists.'
        messenger.simple_error(error_message, error_code=9)
    except NameError:
        messenger.simple_error(
            'It looks like you have not passed a script to the interpreter.',
            error_code=10
        )


main()
