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
This module runs tests to verify Maple's parsing.
'''

# Standard library imports
import sys
import unittest

# Insert the src/ directory to the path so that we can keep the tests out of
# src directory.
sys.path.insert(0, '../src/')

# Language imports
from maple import (arborist, helpers, planter, values)  # noqa: E402

unittest.TestLoader.sortTestMethodsUsing = None

SAMPLE_LINES = [
        '10 - This is a comment',
        '20 write "Hello World"',
        '30 end'
    ]


class TestMapleArborist(unittest.TestCase):
    """This class houses tests for the Maple parser's Arborist module
    """

    def test_0_unique_line_numbers(self):
        # Test for unique line numbers
        self.assertEqual(
            arborist.check_unique_line_numbers(SAMPLE_LINES),
            (True, None),
            'Line numbers are not unique.'
        )

    def test_1_valid_line_numbers(self):
        # Test for valid line numbers
        self.assertEqual(
            arborist.check_valid_line_numbers(SAMPLE_LINES),
            (True, None, None),
            'Lines are not valid'
        )

    def test_2_sequential_line_numbers(self):
        # Test for sequential line numbers
        self.assertEqual(
            arborist.check_sequential_line_numbers(SAMPLE_LINES),
            (True, None, None),
            'Lines are not sequential'
        )

    def test_3_check_line_multiples(self):
        # Test for line numbers where each line is a multiple of the first
        self.assertEqual(
            arborist.check_for_multiples(SAMPLE_LINES),
            (True, None),
            'Line numbers are not multiples'
        )

    def test_4_check_end_statement(self):
        # Check that the last line is an end statement
        self.assertEqual(
            arborist.check_for_end_statement(SAMPLE_LINES),
            (True, None, None),
            'The last statement is not an end statement'
        )

    def test_5_prune_comments(self):
        # Test to ensure that the arborist pruner is cutting out comments
        self.assertEqual(
            arborist.prune_comments(SAMPLE_LINES),
            [
                '20 write "Hello World"',
                '30 end'
            ],
            'Comments have not been pruned'
        )


class TestMapleHelpers(unittest.TestCase):
    """This class houses tests for the Maple parser's helpers module
    """

    def test_0_substitute_values(self):
        # A simple test to verify the value substitution of variables
        # Add a place variable
        values.VARIABLES['place'] = 'world'
        # Test string for replacement
        test_string = '"Hello \'#place\'!"'
        # A valid replacement version of the above
        valid_string = 'Hello \'world\'!'

        # A dummy line number is parsing as this isn't relevant
        line_for_parsing = helpers.substitute_values(test_string, '10')

        # Assert that we have an expression that matches what we need
        self.assertEqual(
            line_for_parsing, valid_string
        )

    def test_1_calculate_expression(self):
        # A simple test to verify that any math expressions are calculated
        # Create a test expression that should be calculated
        test_expression = '"2+3"'

        # The valid output
        valid_expression = 5

        # Test the calculation
        line_for_parsing = helpers.calculate_value(test_expression)

        # Assert that we have an expression that matches what we need
        self.assertEqual(
            line_for_parsing, valid_expression
        )


class TestMaplePlanter(unittest.TestCase):
    """This class houses tests for the Maple parser's Planter module
    """

    def test_0_build_tokens(self):
        # Test to ensure that the tokens are built into the appropriate format
        valid_tokens = [
            {
                'full_line_of_code': '20 write "Hello World"\n',
                'script_line_number': '20',
                'token_end_location': 2,
                'token_number': 2,
                'token_start_location': 0,
                'token_type': (2, 'NUMBER'),
                'token_value': '20'
            },
            {
                'full_line_of_code': '20 write "Hello World"\n',
                'script_line_number': '20',
                'token_end_location': 8,
                'token_number': 3,
                'token_start_location': 3,
                'token_type': (1, 'NAME'),
                'token_value': 'write'
            },
            {
                'full_line_of_code': '20 write "Hello World"\n',
                'script_line_number': '20',
                'token_end_location': 22,
                'token_number': 4,
                'token_start_location': 9,
                'token_type': (3, 'STRING'),
                'token_value': '"Hello World"'
            },
            {
                'full_line_of_code': '20 write "Hello World"\n',
                'script_line_number': '20',
                'token_end_location': 23,
                'token_number': 5,
                'token_start_location': 22,
                'token_type': (4, 'NEWLINE'),
                'token_value': '\n'
            },
            {
                'full_line_of_code': '30 end',
                'script_line_number': '30',
                'token_end_location': 2,
                'token_number': 6,
                'token_start_location': 0,
                'token_type': (2, 'NUMBER'),
                'token_value': '30'
            },
            {
                'full_line_of_code': '30 end',
                'script_line_number': '30',
                'token_end_location': 6,
                'token_number': 7,
                'token_start_location': 3,
                'token_type': (1, 'NAME'),
                'token_value': 'end'
            },
            {
                'full_line_of_code': '30 end',
                'script_line_number': '30',
                'token_end_location': 7,
                'token_number': 8,
                'token_start_location': 6,
                'token_type': (4, 'NEWLINE'),
                'token_value': ''
            }
        ]

        # Prune the comments before continuing as we want to make sure that
        # the test checks for the kinds of tokens that we want.
        lines_for_parsing = arborist.prune_comments(SAMPLE_LINES)

        # Assert that we have a list of tokens that match what we need
        self.assertEqual(
            planter.build_tokens(lines_for_parsing), valid_tokens
        )

    def test_1_build_token_tree(self):
        # Test to ensure that the tokens are configured properly in the tree
        valid_tree = {
            '20':
                [
                    {
                        'full_line_of_code': '20 write "Hello World"\n',
                        'script_line_number': '20',
                        'token_end_location': 2,
                        'token_number': 2,
                        'token_start_location': 0,
                        'token_type': (2, 'NUMBER'),
                        'token_value': '20'
                    },
                    {
                        'full_line_of_code': '20 write "Hello World"\n',
                        'script_line_number': '20',
                        'token_end_location': 8,
                        'token_number': 3,
                        'token_start_location': 3,
                        'token_type': (1, 'NAME'),
                        'token_value': 'write'
                    },
                    {
                        'full_line_of_code': '20 write "Hello World"\n',
                        'script_line_number': '20',
                        'token_end_location': 22,
                        'token_number': 4,
                        'token_start_location': 9,
                        'token_type': (3, 'STRING'),
                        'token_value': '"Hello World"'
                    },
                    {
                        'full_line_of_code': '20 write "Hello World"\n',
                        'script_line_number': '20',
                        'token_end_location': 23,
                        'token_number': 5,
                        'token_start_location': 22,
                        'token_type': (4, 'NEWLINE'),
                        'token_value': '\n'
                    }
                ],
            '30':
                [
                    {
                        'full_line_of_code': '30 end',
                        'script_line_number': '30',
                        'token_end_location': 2,
                        'token_number': 6,
                        'token_start_location': 0,
                        'token_type': (2, 'NUMBER'),
                        'token_value': '30'
                    },
                    {
                        'full_line_of_code': '30 end',
                        'script_line_number': '30',
                        'token_end_location': 6,
                        'token_number': 7,
                        'token_start_location': 3,
                        'token_type': (1, 'NAME'),
                        'token_value': 'end'
                    },
                    {
                        'full_line_of_code': '30 end',
                        'script_line_number': '30',
                        'token_end_location': 7,
                        'token_number': 8,
                        'token_start_location': 6,
                        'token_type': (4, 'NEWLINE'),
                        'token_value': ''
                    }
                ]
            }

        # Assert that we have a list of tokens that match what we need
        self.assertEqual(
            planter.build_tree(), valid_tree
        )


if __name__ == '__main__':
    unittest.main()
