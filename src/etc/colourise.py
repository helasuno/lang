#!/usr/bin/env python3

# Standard library imports
import platform

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
A simple module to colourise the output of text for various components of the
language including coder choices (eg. coloured write statements) and internal
needs (eg. error messages).
'''

# Get the platform of the underlying operation system
PLAT_SYSTEM = platform.system()

# If the system is not Windows, we're operating on the assumption that we are
# using *nix
if PLAT_SYSTEM != 'Windows':
    # Colours for *nix operating systems
    COLOURS = {
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'reset': '\033[00m'
    }
else:
    # Colours for Windows operating systems
    # Courtesy of https://www.youtube.com/watch?v=yQ9Ns6Z4Q-s
    COLOURS = {
        'red': '\u001b[31m',
        'green': '\u001b[32m',
        'yellow': '\u001b[33m',
        'blue': '\u001b[34m',
        'magenta': '\u001b[35m',
        'cyan': '\u001b[36m',
        'reset': '\u001b[0m'
    }


def blue(text: str):
    """Returns blue text. This function returns a blue version of the text
    parameter.

    Args:
        text: the text to "colourise"
    """

    # Return blue text
    return COLOURS['blue'] + text + COLOURS['reset']


def cyan(text: str):
    """Returns cyan text. This function returns a cyan version of the text
    parameter.

    Args:
        text: the text to "colourise"
    """

    # Return cyan text
    return COLOURS['cyan'] + text + COLOURS['reset']


def green(text: str):
    """Returns green text. This function returns a green version of the text
    parameter.

    Args:
        text: the text to "colourise"
    """

    # Return green text
    return COLOURS['green'] + text + COLOURS['reset']


# A simple alias for the green colouring for moments where successes are
# needed.
success = green


def magenta(text: str):
    """Returns magenta text. This function returns a magenta version of the
    text parameter.

    Args:
        text: the text to "colourise"
    """

    # Return magenta text
    return COLOURS['magenta'] + text + COLOURS['reset']


def red(text: str):
    """Returns red text. This function returns a red version of the text
    parameter.

    Args:
        text: the text to "colourise"
    """

    # Return red text
    return COLOURS['red'] + text + COLOURS['reset']


# A simple alias for the red colouring for moments where errors are needed.
error = red


def yellow(text: str):
    """Returns yellow text. This function returns a yellow version of the text
    parameter.

    Args:
        text: the text to "colourise"
    """

    # Return yellow text
    return COLOURS['yellow'] + text + COLOURS['reset']
