#!/usr/bin/env python3

# Standard library imports
import collections
import io
import pprint
import sys
import tokenize

# Custom language imports
from maple import (arborist, tree)

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
This Maple module "plants" (builds) the token tree itself. This also checks
to make sure that it's valid (for instance, the lines are sequentially
numbered).
'''


def build_tokens(lines_of_code: list) -> list:
    """Builds the tokens that will be serve as the basis for the TOKEN_TREE.

    Args:
        contents [list]: the contents of the script as a list of lines

    Returns:
        list: the tree.TOKEN_LIST which is helpful for testing or a tuple that
            has an error message where item 0 is True to indicate that there
            is an error

    Raises:
        None
    """

    try:
        # This holds the last successfully tokenised line
        last_successfully_tokenised_line = []

        # Combine the lines of the script into a single string that will be
        # fed to the tokenizer
        script = '\n'.join(lines_of_code)

        # Pass the script to the tokeniser
        tokens = tokenize.tokenize(
            io.BytesIO(script.encode()).readline
        )

        # Do a quick check of the tokens to see if there are any errors that
        # prevent tokenisation. First, create a list of tokens that will house
        # them temporarily to first be checked and then to serve as a home for
        # them before they are prepped for the tree
        temp_tokens = []

        # Loop over the tokens
        for token in tokens:
            # Set the last_successfully_tokenised_line to two bits of info:
            # the line of the script itself and the script line number
            try:
                last_successfully_tokenised_line = [
                    token.line,
                    token.line.split()[0]
                ]
            # Capture any IndexErrors which are thrown at the end of the token
            # list for instance. These can be ignored
            except IndexError:
                pass
            # Append the token from the tokeniser to the temp_tokens list. This
            # will be drawn from the construct the tree
            temp_tokens.append(token)
    # Catch any tokeniser errors here
    except tokenize.TokenError:
        error_message = (True, 'There is an unterminated set of punctuation ' +
                         'marks. Did you forget some?',
                         last_successfully_tokenised_line[0],
                         last_successfully_tokenised_line[1])
        # Return the error message
        return error_message

    '''Add a finalised token dictionary to the TOKEN_TREE by extracting
    relevant information from a TokenInfo object. A sample of one looks
    like so:
        TokenInfo(
            type=1 (NAME),
            string='write',
            start=(4, 3),
            end=(4, 8),
            line='40 write "Hello world!"\n'
        )
    For ease of use, we are going to convert each of these into Maple friendly
    tokens that are simple Python dictionaries.
    '''
    # A simple counter for what token we are working with
    token_counter = 1
    for token in temp_tokens:
        # Try getting the script line. We assume by this point that the
        # arborist has dealt with any errant script line numbers so we are
        # running on the assumption that we are safe here.
        try:
            script_line = token.line.split()[0]
        # If the token line has no value
        except IndexError:
            # Set the script_line to None
            script_line = None

        # Append the token in dictionary format to the list of tokens held
        # by the tree module. This TOKEN_LIST will be used as the basis for
        # creating the tree itself.
        tree.TOKEN_LIST.append({
            'full_line_of_code': token.line,
            'script_line_number': script_line,
            'token_number': token_counter,
            'token_type': (token.type, tokenize.tok_name[token.type]),
            'token_start_location': token.start[1],
            'token_end_location': token.end[1],
            'token_value': token.string
        })

        # Increment the token counter
        token_counter += 1

    # Delete the temporary token list
    del temp_tokens

    # Clean up unnecessary tokens in the TOKEN_LIST
    arborist.clean_token_list()

    # Return the tree.TOKEN_LIST to signify that everything is okay
    return tree.TOKEN_LIST


def build_tree(show=False, show_line=None) -> dict:
    """Builds the token tree, the dictionary that is traversed as part of
    execution. This is the final step, so to speak, before the code is
    evaluated.

    Args:
        show: print out the tree when it's constructed, defaults to False
        show_line: show a specific line if show is set to True which allows for
            debugging specific lines in the tree

    Returns:
        dict: the tree.TOKEN_TREE or None (useful for testing)

    Raises:
        None
    """

    # Create a temporary tree that will ultimately be copied to the official
    # global_values.TREE. This allows us to do things like clean it up and
    # organise it accordingly.
    temp_token_tree = {}

    # Get the script line numbers (ie. the first part of each line) so that we
    # can number each line. We do this because each element in the tree is a
    # key-value pair with the key being the line number and the value being the
    # set of tokens on that line
    script_lines = []

    # Loop over the tokens
    for token in tree.TOKEN_LIST:
        # Append to the script lines the line of the token. This will create
        # duplicates in the list when a line has more than one token which
        # will be true for any line that does anything of value.
        script_lines.append(token['script_line_number'])

    # Get the unique elements of the script_lines list, that is, just a list of
    # the script_lines. Replace script_lines with the counter for each line
    # as we don't need the original list of lines anymore.
    script_lines = collections.Counter(script_lines)

    # Loop over the script_lines
    for line in script_lines:
        # And create an empty list for each of the script_lines. That list will
        # be a list of tokens associated with the unique line numbers. So, now,
        # we might have something like:
        # {
        #     '10': [],
        #     '20': [],
        #     '30': []
        # }
        temp_token_tree[line] = []

    # Loop over the TOKEN_LIST and add in the corresponding tokens
    for token in tree.TOKEN_LIST:
        # Add the token to the correct script_line in the temp_token_tree
        temp_token_tree[token['script_line_number']].append(token)

    # Try to see if there are any None tokens
    try:
        # Delete any None types in the tree. This would include things like the
        # encoding.
        del temp_token_tree[None]
    # If there aren't any None tokens, a KeyError will be raised
    except KeyError:
        # Ignore and move along
        pass

    # Set the tree.TOKEN_TREE to our constructed temporary tree
    tree.TOKEN_TREE = temp_token_tree

    # Set the LINE_NUMBERS to the keys from the tree
    tree.LINE_NUMBERS = list(tree.TOKEN_TREE.keys())

    # Delete the temp_token_tree. This won't save much memory but every little
    # bit helps
    del temp_token_tree

    # If the tree needs to be shown for internal language debugging...
    if show:
        # If a specific line is specified...
        if show_line is not None:
            # Pretty print the specific line
            pprint.pprint(tree.TOKEN_TREE[show_line])
        # Otherwise
        else:
            # Pretty print the whole tree
            pprint.pprint(tree.TOKEN_TREE)
        # Exit the app as it's clear that we are debugging the language
        sys.exit(0)

        return {}

    # Return the tree.TOKEN_TREE which is helpful for testing
    return tree.TOKEN_TREE
