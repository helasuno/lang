#!/usr/bin/env python3

# Standard library imports
import getopt
import sys

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
A simple script to reline a script in case things get unruly or the scripter
just wants to clean up their line numbering to be conformant with language
conventions.
'''
# Get the system arguments
sys_args = sys.argv[1:]
# Set the options here, -w and -m
short_opts = 'w:m:'

# Get the options and arguments
opts, args = getopt.getopt(sys_args, short_opts)

# Set a default line multiple
line_number_multiple = 10
# Set a default relined_file name which defaults to nothing signifying that
# the user
relined_file = ''

# If there is no argument (ie. no script to reline), error out
if args[0] == '':
    # If the script name isn't passed, fail gracefully
    print('Pass a script name to the reliner')
    # Exit the script
    sys.exit(0)
else:
    # Set the script name to the argument
    script_name = args[0]
    # Default to setting the relined_file to the script_name, ie. set it to
    # overwrite. This can be overriden if the -w flag is set (handled below).
    relined_file = args[0]

# Loop over the options
for option in opts:
    # Match case with the options. Here, we look at option[0] as the opts
    # are tuples of the form (option, value).
    match option[0]:
        # Match the -m flag
        case '-m':
            # Check to see if it's numeric
            if not option[1].isnumeric():
                # Print an error
                print('The line number multiple passed is not a valid ' +
                      'line number')
                # Abandon ship
                sys.exit(0)
            else:
                # Otherwise, set the line_number_multiple to the option passed
                line_number_multiple = int(option[1])
        # Match the -w flag
        case '-w':
            # Set the relined_file to the option passed
            relined_file = option[1]

# Leave these here just in case we need to debug
# print('Script to reline:', script_name)
# print('Line multiple:', line_number_multiple)
# print('Relined file:', relined_file)
# sys.exit(0)

# Inform the user that we are about to start relining
print(
    f'Relining {script_name} and numbering with multiples of ' +
    f'{line_number_multiple}'
)

# Try to open the script
try:
    # Open the script
    with open(script_name, 'r') as script:
        # Create a variable that will house the relined script
        relined_script = ''
        # Set the first line number to the line_number_multiple. This number
        # will be incremented down below
        line_number = int(line_number_multiple)
        # Read in the lines
        lines = script.readlines()
        # Notify the user that we are about to reline
        print(f'Relining {len(lines)} lines...')
        # Loop over the lines
        for line in lines:
            # Split the lines so that we can cut out the old line number
            line = line.split()
            # Delete the line number from the line
            del line[0]
            # Join the remaining parts of the line back together
            line = ' '.join(line)
            # Set the new line to the line_number + the remaining part of the
            # line. Here, we have the newly numbered line
            line = str(line_number) + ' ' + line
            # Increment the line number
            line_number += int(line_number_multiple)
            # Add the newly numbered line to the relined_script and add a new
            # line
            relined_script += line + '\n'
# If the file isn't found, notify the user and abandon ship
except FileNotFoundError:
    print(f'{script_name} is not a valid script')
    sys.exit(0)

# Open up the new file
with open(relined_file, 'wb') as new_file_output:
    # Write the newly relined script to disk
    new_file_output.write(relined_script.encode())
    # Notify the user
    print(f'Script written to {relined_file}')
