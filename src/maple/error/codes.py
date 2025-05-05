#!/usr/bin/env python3

# Standard library imports
import sys

# Custom imports
from maple import values
from maple.error import messenger
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
A simple module to handle reporting more elaborate details about errors with
information about error codes.
'''

elaborated_errors = {
    1:  [
            'This error is thrown when you try to interrupt something by ' +
            'pushing Ctrl-C in your terminal. It\'s likely the case that ' +
            'you knew this error was coming. Regardless, you will want to ' +
            'consider some of the consequences of this as the script was ' +
            'abruptly ended. For instance, something being worked on would ' +
            'not have finished.',
            'N/A'
        ],
    2:  [
            'This error is thrown when you don\'t have unique line numbers. ' +
            'A key requirement of a script is that each line has a unique ' +
            'line number. Look for the multiple line numbers that are the '
            'same as reported by the error. For instance, the following ' +
            'script will trigger the error.',
            '10 - This is a comment\n' +
            f'{colourise.red("20")} writeln "Hello World"\n' +
            f'{colourise.red("20")} end'
        ],
    3:  [
            'This error is thrown when the lines of code are not ' +
            'sequential. Each line needs to have a line number greater than ' +
            'the past. Look for any out of order line numbers and fix ' +
            'accordingly.',
            '10 - This is a comment\n' +
            f'{colourise.red("30")} writeln "Hello World"\n' +
            '20 end'
        ],
    4:  [
            'This error notes that a line does not start with a valid line ' +
            'numbers, that is, an integer greater than zero.',
            f'{colourise.red("a")} - This is a comment\n' +
            '20 writeln "Hello World"\n' +
            '30 end'
        ],
    5:  [
            'This error is thrown when there is not a valid end statement ' +
            'as the last statement in the script. All scripts need to have ' +
            'an end statement on the final line to flag, for the ' +
            'interpreter that the script is done executing. Think of this ' +
            'as similar to telling the interpreter that you want to quit.',
            '10 - This is a comment\n20 writeln "Hello World"\n' +
            f'{colourise.red("_______________")}'
        ],
    6:  [
            'This warning is thrown when there are line numbers that are ' +
            'not multiples of the first line. This has no consequences for ' +
            'the execution of the script and this warning will only alert ' +
            'you to a convention in the language. While execution won\'t ' +
            'be affected, yoru script will benefit from having conformant ' +
            'line numbering. This warning can be addressed by running the ' +
            f'interpreter with the {colourise.yellow("-r")} flag.',
            '10 - This is a comment\n' +
            f'{colourise.red("14")} writeln "Hello World"\n' +
            '30 end'
        ],
    7:  [
            'This error is thrown when there is a zero as a first line ' +
            'number. You need to use a non-zero positive integer as the ' +
            'first line.',
            f'{colourise.red("0")} - This is a comment\n' +
            '10 writeln "Hello World"\n' +
            '20 end'
        ],
    8:  [
            'This error occurs when Maple, the language parser, errors out ' +
            'because there is a part of the script that can\'t be ' +
            'accounted for. An error message will be provided to guide ' +
            'this rather general error which is commonly caused by a string ' +
            'that is missing a quotation mark.',
            '10 - This is a comment\n' +
            f'20 writeln "Hello World{colourise.red("___")}' +
            '\n30 end'
        ],
    9:  [
            'This error is thrown if the script passed to the interpreter ' +
            'can\'t be found. It\'s possible that either a typo was made ' +
            'or the file isn\'t accessible (in spite of it existing).' +
            'A common reason here might be failing to provide a path to ' +
            'the file if it\'s not in the current path.'
            'N/A'
        ],
    10:  [
            'Thrown when the interpreter is called without a script. You ' +
            'will need to pass, at a minimum, a flag. Run' +
            f'{colourise.yellow("helasuno -h")} to get a list of valid flags.',
            'N/A'
        ],
    11:  [
            'This error happens when a variable value is requested but it ' +
            'isn\'t set. Make sure that the variable is set before ' +
            'continuing along. In the example below, the ' +
            f'{colourise.yellow("name")} variable is not set.',
            '10 - This is a comment\n20 writeln "Hello ' +
            f'{colourise.red("#name")}"\n30 end'
        ],
    12:  [
            'The statement you\'ve provided isn\'t valid. Perhaps a valid ' +
            'one was provided but spelled wrong or a statement was called ' +
            'that doesn\'t exist.',
            '10 - This is a comment\n' +
            f'20 {colourise.red("wrte")} "Hello World"\n' +
            '30 end'
        ],
    13:  [
            f'The {colourise.yellow("end")} statement that you\'ve ' +
            'provided involves too many options and values. The only thing ' +
            'that should be on that line is a line number and the ' +
            f'{colourise.yellow("end")} statement itself.',
            '10 - This is a comment\n' +
            '20 write "Hello World"\n' +
            f'30 end{colourise.red("_now")}'
        ],
    14:  [
            f'The {colourise.yellow("pause")} statement includes a ' +
            'parameter that isn\'t a valid number. As a result, the ' +
            'statement is trying to pause on the basis of an invalid ' +
            f'timeframe. Provide the {colourise.yellow("pause")} statement ' +
            'a simple integer.',
            '10 - This is a comment\n'
            f'20 pause {colourise.red("\"Hello World\"")}\n'
            '30 end'
        ],
    15:  [
            f'The {colourise.yellow("set")} statement tries to create a ' +
            'variable using the PROHIBITED_PREFIX (hs_). You need to start ' +
            'your variable with a different prefix as variables that start ' +
            'with hs_ are reserved by the interpreter.',
            '10 - This is a comment\n' +
            f'20 set {colourise.red("hs_name")} = "Helasuno"\n' +
            '30 end'
        ],
    16:  [
            'The error here is calling attention to the lack of an ' +
            'appropriate operator used to assign a variable. A ' +
            f'{colourise.yellow("set")} statement should be followed by the ' +
            'variable name, an equal sign, and the value of the variable. ' +
            'The language has two assignment operators (= and ->) but they ' +
            'are not interchangeable.',
            '10 - This is a comment\n' +
            f'20 set name {colourise.red("->")} "Helasuno"\n'
            '30 end'
        ],
    17:  [
            'This error is thrown when the user tries to name a variable ' +
            'after a statement (eg. naming the variable "write"). You ' +
            'can\'t name a variable after the following: ' +
            f'{colourise.yellow(", ".join(values.STATEMENT_NAMES))}.',
            '10 - This is a comment\n' +
            f'20 set {colourise.red("write")} -> "Helasuno"\n'
            '30 end'
        ],
    18:  [
            'The wrong operator is used to modify a statement. You need ' +
            f'to use {colourise.yellow(values.VALID_OPERATORS["statmod"])}.',
            '10 - This is a comment\n' +
            f'20 writeln "Hello World" {colourise.red("-")} green\n' +
            '30 end'
        ],
    19:  [
            'An invalid statement modifier was provided to a ' +
            f'{colourise.yellow("write")} or {colourise.yellow("writeln")} ' +
            'statement. A list of valid statement modifiers will be ' +
            'provided in the error message. Perhaps this was just a typo?',
            '10 - This is a comment\n' +
            f'20 writeln "Hello World" -> {colourise.red("fun")}\n' +
            '30 end'
        ],
    20:  [
            'A statement modifier (statmod) is placed in the wrong order. ' +
            'While this may seem irrelevant, some statmods need to be ' +
            'ordered in a particular way. See the documentation for the ' +
            'statement being modified for more details.',
            '10 - This is a comment\n' +
            '20 writeln "Hello World" -> ' +
            f'{colourise.red("\"green|upper\"")}\n' +
            '30 end'
        ],
    21:  [
            f'You passed something to a {colourise.yellow("jump")} ' +
            'statement that isn\'t a valid number.',
            '10 - This is a comment\n' +
            f'20 jump {colourise.red("\"Hello World\"")}\n'
            '30 end'
        ],
    22:  [
            'This error is thrown if the script is stuck in a loop and if ' +
            'there\'s no certain break from the loop. Check for any ' +
            f'{colourise.yellow("jump")} statements that might create an ' +
            'unending loop.',
            '10 - This is a comment\n' +
            '20 writeln "Hello World"\n' +
            f'{colourise.red("30 jump 20")}\n' +
            '40 end'
        ],
    23:  [
            'An invalid line number is passed to a ' +
            f'{colourise.yellow("jump")} statement. Unlike error 21, where ' +
            'the error is thrown if something like "ab" is passed (ie. not ' +
            'a number), this error is thrown if a valid line number is ' +
            'provided but if the number doesn\'t exist.',
            '10 - This is a comment\n' +
            f'20 jump {colourise.red("40")}\n'
            '30 end\n' +
            f'{colourise.red("_______________")}'
        ],
    24:  [
            'Variable substitution failed because the variable ' +
            'substitution character (' +
            f'{colourise.yellow(values.VARIABLE_SYMBOL)}) was left on its ' +
            'own. You need to escape it by providing the symbol twice: ' +
            f'{colourise.yellow(values.VARIABLE_SYMBOL*2)}.',
            '10 - This is a comment\n' +
            '20 set name = "Helasuno"\n' +
            f'30 writeln "Hello {colourise.red("#")} #name"\n' +
            '40 end'
        ],
    25:  [
            f'The {colourise.yellow("write")} statement has too many ' +
            'statement modifiers. Currently, you can only have ' +
            f'{values.WRITE_STATMOD_COUNT} statmods for the ' +
            f'{colourise.yellow("write")} statement. Cut down the number of ' +
            'statmods that you have. Currently, valid statmods include ' +
            f'{colourise.yellow(", ".join(values.VALID_STATMODS_WRITE))}.',
            '10 - This is a comment\n' +
            '20 writeln "Hello World" -> ' +
            f'{colourise.red("\"lower|green|blue\"")}\n' +
            '30 end\n'
    ]
}


def error_elaborator(error_code: int):
    """Report back elaborated error messages to help a user diagnose issues
    with their script.

    Args:
        error_code [int]: the error code to elaborate on

    Returns:
        N/A

    Raises:
        None
    """
    try:
        # Convert the error code into an integer in case it wasn't passed
        # as one.
        error_code = int(error_code)
        # Get the corresponding error message
        elaboration_message = elaborated_errors[error_code]
        # Error message header to add to the elaborated message
        elaboration_header = colourise.blue(
            f'[Error Code {str(error_code)}]'
        )
    except (KeyError, ValueError):
        # Report back an error message when the error code provided is invalid
        messenger.simple_error(
            f'The error code {colourise.yellow(str(error_code))} is ' +
            'not a valid error code. You need to pass an error code ' +
            f'between 1-{list(elaborated_errors)[-1]}.'
        )

    # Print the header
    print(elaboration_header)
    # Construct the message with a description and sample erroneous code
    message = elaboration_message[0] + '\n\n' + \
        colourise.cyan('[Sample Erroneous Code]\n') + \
        elaboration_message[1] + '\n'
    # Print the message
    print(message)
    # Exit the script
    sys.exit(0)
