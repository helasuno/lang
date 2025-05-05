#!/usr/bin/env python3

# Standard library imports
import sys

# Custom imports
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
A module that holds functions to support flags in the interpreter.
'''


def reline(script_name: str):
    # Try to open the script
    try:
        # Open the script
        with open(script_name, 'r') as script:
            # Create a variable that will house the relined script
            relined_script = ''
            # Set the first line number to the line_number_multiple. This
            # number will be incremented down below.
            line_number = 1
            # Read in the lines
            lines = script.readlines()
            # Loop over the lines
            for line in lines:
                # Split the lines so that we can cut out the old line number
                line = line.split()
                # Delete the line number from the line
                del line[0]
                # Join the remaining parts of the line back together
                line = ' '.join(line)
                # Set the new line to the line_number + the remaining part of
                # the line. Here, we have the newly numbered line
                line = str(line_number) + ' ' + line
                # Increment the line number
                line_number += 1
                # Add the newly numbered line to the relined_script and add a
                # new line.
                relined_script += line + '\n'
    # If the file isn't found, notify the user and abandon ship
    except FileNotFoundError:
        if script_name == '':
            messenger.simple_error(
                'No script name was passed to the interpreter.',
                error_code=10
            )
        else:
            messenger.simple_error(
                f'{script_name} is not a valid script',
                error_code=9
            )
        sys.exit(0)

    # Open up the new file
    with open(script_name, 'wb') as new_file_output:
        # Write the newly relined script to disk
        new_file_output.write(relined_script.encode())
