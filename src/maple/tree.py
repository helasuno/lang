#!/usr/bin/env python3

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
This Maple module houses the TOKEN_TREE, plain and simple.
'''

# This just houses the list of tokens that aren't yet put in the tree
TOKEN_LIST = []

# This is the token "tree" for the Maple parser
TOKEN_TREE = {}

# Line numbers
LINE_NUMBERS = []


def get_line_numbers():
    """Get the line numbers

    Args:
        N/A

    Returns:
        list: the line numbers in the script

    Raises:
        None
    """
    return LINE_NUMBERS


def verify_line_number(line_no) -> bool:
    """Verify that a line number is in the list of LINE_NUMBERS

    Args:
        line_no [str]: the line number to check

    Returns:
        bool: True if the line number is in the list, False if it's not

    Raises:
        None
    """
    try:
        # Get the index of the line number
        index = LINE_NUMBERS.index(line_no)
        # If it's equal to or greater than zero, that is, it is in the list...
        if index >= 0:
            # Return True
            return True
    # If a ValueError is thrown
    except ValueError:
        # Return False
        return False


def get_tokens():
    """Get the token list

    Args:
        N/A

    Returns:
        list: the token list

    Raises:
        None
    """
    return TOKEN_LIST


def get_tree():
    """Get the token tree

    Args:
        N/A

    Returns:
        dict: the token tree

    Raises:
        None
    """
    return TOKEN_TREE


def get_tree_item(line_no):
    """Get a specific line of tokens from token tree

    Args:
        N/A

    Returns:
        dict: the token tree

    Raises:
        None
    """
    return TOKEN_TREE[line_no]


def set_tokens(tokens):
    """Set the token list

    Args:
        tokens [list]: the token list

    Returns:
        N/A

    Raises:
        None
    """
    global TOKEN_LIST
    TOKEN_LIST = tokens


def set_tree(tree):
    """Set the token tree

    Args:
        tree [dict]: the token tree

    Returns:
        N/A

    Raises:
        None
    """
    global TOKEN_TREE
    TOKEN_TREE = tree
