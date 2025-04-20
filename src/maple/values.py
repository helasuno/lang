#!/usr/bin/env python3

# Standard library imports
import time

# Language imports
from etc import global_values

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
This houses variables that serve as a central location for values that need to
be drawn on from other parts of the parser.
'''

STATEMENT_NAMES = [
    'end',
    'get',
    'jump',
    'pause',
    'set',
    'write',
    'writeln'
]

# List of valid operators
VALID_OPERATORS = {
    'assignment': '=',
    'statmod': '->',
    'statmod_splitter': '|'
}

# List of valid and implemented statements
VALID_STATEMENTS = {
    'comment': '-',
    'end': 'end'
}

# List of valid statmods for the write(ln) statement
VALID_STATMODS_WRITE = [
    'blue',
    'green',
    'lower',
    'magenta',
    'red',
    'upper',
    'yellow'
]

# This sets the prohibited variable prefix. Scripts cannot start with this
# prefix as reserved variables are only allowed to use it
VARIABLE_PROHIBITED_PREFIX = 'hs_'

# Hold the variables
VARIABLES = {
    f'{VARIABLE_PROHIBITED_PREFIX}current_date':
        f'{time.localtime().tm_mday}/' +
        f'{time.localtime().tm_mon}/' +
        f'{time.localtime().tm_year}',
    f'{VARIABLE_PROHIBITED_PREFIX}ac_current_time':
        f'{time.localtime().tm_hour}:' +
        f'{time.localtime().tm_min}:' +
        f'{time.localtime().tm_sec}',
    f'{VARIABLE_PROHIBITED_PREFIX}lang_name': global_values.LANG_NAME,
    f'{VARIABLE_PROHIBITED_PREFIX}lang_version': global_values.LANG_VERSION
}

VARIABLE_SYMBOL = '#'
