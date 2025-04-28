#!/usr/bin/env python3

# Standard library imports
import compileall
import math
import os
import shutil
import stat
import sys
import time
import zipapp

# Custom imports
from src.etc import (colourise, global_values)

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
This packages the interpreter as a zipapp executable bundle.
'''

NAME = global_values.LANG_NAME_ACRONYM
VERSION = global_values.LANG_VERSION

PY_MINOR_VERSION = int(global_values.PYTHON_VERSION[1])
PY_MINOR_VERSION_MINIMUM = global_values.PYTHON_VERSION_MINIMUM_MINOR
PY_VERSION = f'{global_values.PYTHON_VERSION[0]}.' + \
    f'{global_values.PYTHON_VERSION[1]}'

DIST = 'dist/'
INTERPRETER = '/usr/bin/env python3'

START = time.time()


def print_status(message, bright=False):
    """Print status messages with various options for brightness

    Args:
        message: the message to print
        bright [bool]: if True, print the message in yellow and if False, print
            the message in a subtle blue

    Returns:
        N/A

    Raises:
        None
    """
    if bright:
        # Simple function to facilitate progress reporting
        output = f'    {colourise.red(":: ")} {colourise.yellow(message)}'
    else:
        # Simple function to facilitate progress reporting
        output = f'    {colourise.blue("\u2713 ")} {colourise.cyan(message)}'
    print(output)


# Check that the version of Python installed is sufficient. Here, we are
# checking to see that the minor version is not lower than the minimum.
if PY_MINOR_VERSION < PY_MINOR_VERSION_MINIMUM:
    # Print an error message
    print_status(
        f'The version of Python you are running ({PY_VERSION}) ' +
        'is too low. Please upgrade to at least ' +
        f'{global_values.PYTHON_VERSION_MINIMUM}.',
        bright=True
    )
    # Exit the script
    sys.exit(0)

# Print out a blank space at the beginning
print('')
print(colourise.magenta(f'{global_values.LANG_NAME} Packager'))
print_status(f'Python version installed ({PY_VERSION}) is new enough...')
# Set up the DIST directory
print_status(f'Checking for {DIST} directory and creating if need be...')
# If the build directory does not exist...
if os.path.exists(DIST) is False:
    # Create the dist directory
    os.mkdir(DIST)

# Clean up the pycaches that might have been produced through local executions
print_status('Cleaning up source folders to remove any pycaches...')

# Remove the __pycache__ folders
try:
    # Remove the caches
    shutil.rmtree('src/__pycache__/')
    shutil.rmtree('src/etc/__pycache__/')
    shutil.rmtree('src/maple/__pycache__/')
    shutil.rmtree('src/maple/error/__pycache__/')
    shutil.rmtree('src/statements/__pycache__/')
    shutil.rmtree('src/tools/__pycache__/')
    shutil.rmtree('tests/__pycache__/')
# If a folder is not found, move on
except FileNotFoundError:
    pass

print_status('Compiling .py files to bytecode...')
# Compile py modules to pyc files
#   Force recompiles pyc modules even if they aren't old
#   Optimise of 2 is the most "aggressive", removing even the
#   docstrings.
compileall.compile_dir(
    'src/',
    force=True,
    optimize=2,
    quiet=2
)

# Set the zipapp location
zipapp_loc = f'{DIST}{NAME.lower()}'
print_status(f'Creating {NAME} package, version {VERSION}...')
# Create the zipapp
zipapp.create_archive(
    source='src/',
    target=zipapp_loc,
    interpreter=INTERPRETER,
    compressed=True
)

print_status('Setting permissions of the interpreter to be correct...')

# Set the permissions of the interpreter to executable for everyone
# os.chmod(zipapp_loc, 0o755)
os.chmod(zipapp_loc, stat.S_IRWXU)

# Report the output of the packaging, including the timing
print_status(f'zipapp created in {DIST}!')

# Get the time now
END = time.time()
# Get the difference between the end and start time, rouding the difference
# to two decimal places
diff = round(END-START, 2)
# Get the minutes by dividing the diff by 60 and getting the floor
# Here, as an example, if the diff is 183, we really only need 183/3 to yield
# 3, not 3.05
minutes = math.floor(diff/60)
# Get the modulo to get the remainder, that is, the "0.05" from above
seconds = round(diff % 60)

# Print out the results
print(
    colourise.green(f'\n    ::  Time: {minutes} min, {seconds} sec')
)

# Get the size of the zipapp
package_size = os.stat(zipapp_loc)
# Convert the bytes to kilobytes
package_size = round(package_size.st_size / 1024, 2)
# Print out the package size
print(
    colourise.green(f'    ::  Package Size: {package_size} KB')
)

# Print out an extra line to space things out
print()
