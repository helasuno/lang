#!/usr/bin/env python3

# Standard library imports
import collections

# Language imports
from maple import (tree, values)

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
The arborist checks to make sure that the script and tree are valid (for
instance, the lines are sequentially numbered). It also does some work to
prune (ie. clean up) lines that won't require parsing such as comments.
Consider this the "maintainer" of the (future) set of tokens that also cleans
up the script.
'''


def check_unique_line_numbers(lines_of_code: list) -> bool:
    """Checks lines in a script to make sure that the lines have unique line
    numbers. This helps to ensure that statements like GOTO work as intended.

    Args:
        lines_of_code [list]: the lines of code to check

    Returns:
        unique_lines [bool]: whether the lines of code have unique line numbers
        non_unique_line_number [str]: a string that contains the non-unique
            line number, defaults to None if every line number is unique

    Raises:
        None
    """

    # Hold the line numbers
    line_numbers = []

    # Loop over the lines of code
    for line in lines_of_code:
        # Try to get the line
        try:
            # Get the first part of the line which is assumed to be the line
            # number
            line_numbers.append(line.split()[0])
        except IndexError:
            # Pass if there is an IndexError
            pass

    # Create a counter of the line numbers. Thanks to https://www.
    # pythonhelp.org/python-lists/how-to-check-for-duplicates-in-a-list-
    # python/ for this one.
    line_numbers = collections.Counter(line_numbers)
    # For each line number and it's associated count...
    for line, count in line_numbers.items():
        # If the number of times a line number appears is greater than 1...
        if count > 1:
            # Return False as we don't have unique line numbers
            # Return, as well, the line number that is not unique
            return False, str(line)

    # If we didn't catch any duplicate line numbers above, return True
    return True, None


def check_valid_line_numbers(lines_of_code: list) -> bool:
    """Checks lines to make sure that they all start with a valid line number.
    This will throw an error if, for instance, a line number is missing.

    Args:
        lines_of_code [list]: the lines of the script to validate

    Returns:
        valid_lines [bool]: whether the lines of code have unique line numbers
        invalid_line_number [str]: the line with an invalid line number, None
            if the line number is valid
        line_number_in_doc [str]: the line number of the line with the invalid
            line number

    Raises:
        None
    """

    # Set up a placeholder for line numbers that will be used to make sure
    # that they are all valid.
    line_numbers = []
    # For each line in the script
    for line in lines_of_code:
        # Try to get the line numbers and add them to line_numbers
        try:
            line_numbers.append(line.split()[0])
        except IndexError:
            pass

    # For each line
    for line in line_numbers:
        # If the line has an actual value that isn't None...
        # This helps to catch things like blank lines
        if line is not None:
            # And if the line isn't a number...
            if not line.isnumeric():
                # Return False
                return False, line, line_numbers.index(line)+1

    # If we didn't catch any invalid line numbers above, return True
    return True, None, None


def check_sequential_line_numbers(lines_of_code: list) -> bool:
    """Checks lines to make sure that the line numbers are sequential.

    Args:
        lines_of_code [list]: the lines of the script to validate

    Returns:
        sequential_line_numbers [bool]: whether the lines of code are
            sequentially ordered
        line_numbers [list]: a list of the line numbers that are scripted,
            None if the lines are in order
        sorted_line_numbers [list]: a list of the line numbers in sorted
            order, None if the lines are in order

    Raises:
        None
    """

    # Hold the line numbers
    line_numbers = []

    # Loop over the lines of code
    for line in lines_of_code:
        # Try to get the line
        try:
            # Get the first part of the line which is assumed to be the line
            # number
            line_numbers.append(line.split()[0])
        except IndexError:
            # Pass if there is an IndexError
            pass

    # Hold the sorted line numbers
    sorted_line_numbers = sorted(line_numbers)

    # If the line_numbers list is not in the same order as a sorted list
    if line_numbers != sorted_line_numbers:
        # Return False and the line_numbers
        return False, line_numbers, sorted_line_numbers

    # If we got here, we can assume that the lines are in sequential order
    return True, None, None


def check_for_multiples(lines_of_code: list) -> bool:
    """Check to see if the line numbers are multiples of each other. This
        should only be reported as a warning to the end user.

    Args:
        lines_of_code [list]: the lines of the script to validate

    Returns:
        multiples [bool]: whether the numbers are multiples of each other
        first_line_number [int]: the first line number which every subsequent
            line number should be a multiple of

    Raises:
        None
    """
    # Create a list to hold line numbers
    line_numbers = []
    # Hold the first number that will be returned if the lines are not
    # multiples of this number
    first_number = -1
    # For each line in the lines_of_code
    for line in lines_of_code:
        # Hold the line number
        line_no = int(line.split()[0])
        # Append the line number
        line_numbers.append(line_no)
        # Check if the first number needs to be set
        if first_number == -1:
            # If the first_number is still -1, set it to the line_number
            first_number = line_no

    # For each number in line_number
    for number in line_numbers:
        # We need to catch the possibility that the first number is zero
        try:
            # If the number modulo first number is not zero (ie. the division
            # yields a non-zero remainder)
            if number % first_number != 0:
                # Return false and the first_number so that a user can be
                # notified.
                return False, first_number
            # If the first line number is 0, warn the user.

        except ZeroDivisionError:
            # Ignore the fact that the first line is zero
            pass
    # If we got here, everything is golden so report back that all line numbers
    # are multiples of the first line
    return True, None


def check_for_nonzero_start(lines_of_code: list) -> bool:
    """Check to make sure that the last line of the script is an end statement

    Args:
        lines_of_code [list]: the lines of the script to validate

    Returns:
        nonzero_start [bool]: True if the first line is not zero

    Raises:
        None
    """

    # Remove any blank lines from the lines of code in case there are empty
    # lines after the end statement (or the last statement used)
    try:
        lines_of_code.remove('')
    # A ValueError will be thrown if there are no empty lines at the end of
    # the file.
    except ValueError:
        pass
    # Get the last line of code
    split_last_line = lines_of_code[0]
    # Get the line number
    statement_line_number = int(split_last_line.split()[0])

    # If the statement_line_number is 0
    if statement_line_number == 0:
        # The first number is not zero so return False
        return False

    # If we got here, we can assume that the first number is 0 so return True
    # and None to signify that there is no error
    return True


def check_for_end_statement(lines_of_code: list) -> bool:
    """Check to make sure that the last line of the script is an end statement

    Args:
        lines_of_code [list]: the lines of the script to validate

    Returns:
        end_statement [bool]: whether the final statement is an end statement
        line_number: the line number where the (in)valid statement is
        statement_name: the invalid statement name

    Raises:
        None
    """

    # Remove any blank lines from the lines of code in case there are empty
    # lines after the end statement (or the last statement used)
    try:
        lines_of_code.remove('')
    # A ValueError will be thrown if there are no empty lines at the end of
    # the file.
    except ValueError:
        pass
    # Get the last line of code
    split_last_line = lines_of_code[-1]
    # Get the line number
    statement_line_number = split_last_line.split()[0]
    # Get the statement name to check that it is an end statement
    statement_name = split_last_line.split()[1]
    # If the statement name isn't end
    if statement_name != 'end':
        # Return False and provide the line number and statement name for
        # error reportion
        return False, statement_line_number, statement_name
    # If we got here, the last statement is an end statement
    return True, None, None


def prune_comments(lines_of_code: list) -> list:
    """Remove comments from the list of lines of code as these don't need to
    be parsed and, ultimately, the token tree

    Args:
        lines_of_code [list]: the lines of the script to validate

    Returns:
        pruned_comments [list]: a list of lines of code with the comments
            pruned (ie. removed)

    Raises:
        None
    """

    # This is the list of lines of code that will have comments removed
    pruned_lines_of_code = []

    for line in lines_of_code:
        # Get the first non-numeric element as comments are line numbered so
        # we need to get the next element after the line number
        first_element = line.split()[1]

        # If the first element is not a comment...
        if first_element is not values.VALID_STATEMENTS['comment']:
            # Append the line as we can assume that it is not a comment
            # and therefore in need of parsing
            pruned_lines_of_code.append(line)

    # Return the script without commented lines
    return pruned_lines_of_code


def clean_token_list() -> bool:
    """Remove unnecessary tokens from the TOKEN_LIST after
    planter.build_tokens() has run

    Args:
        None

    Returns:
        bool: whether the cleaning of unnecessary tokens was successful

    Raises:
        None
    """

    if tree.TOKEN_LIST == {}:
        return False
    else:
        # Get rid of the encoding
        tree.TOKEN_LIST.pop(0)
        # Get rid of a trailing newline
        tree.TOKEN_LIST.pop(-1)
