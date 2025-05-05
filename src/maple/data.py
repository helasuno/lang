#!/usr/bin/env python3

# Standard library imports
import datetime
import locale
import pathlib
import pprint
import statistics
import time

# Language imports
from maple import (planter, tree)
from maple.error import messenger
from etc import (colourise, global_values)

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
This module produces data about Maple's functions
'''

# Set the locale to the local one so that thousands seperators are locale
# specific. Thanks to https://stackoverflow.com/a/10742904 for this tip.
locale.setlocale(locale.LC_ALL, '')


def get_token_data(script_name: str) -> dict:
    """Generates simple data about tokens and tokenisation

    Args:
        script_name [str]: the script that is being checked

    Returns:
        data [dict]: the data generated in the method

    Raises:
        None
    """

    # Get the tokens without them being "planted"
    raw_tokens = tree.get_tokens()
    # Get the token tree
    token_tree = tree.get_tree()

    # Print out a header for the token tree
    print(colourise.yellow(':: TOKENISATION :: '))
    # Print out a header for the token tree
    print(colourise.green('\nRaw Tokens'))
    # Print out the token tree
    pprint.pprint(raw_tokens)
    # Print out a header for the token tree
    print(colourise.green('\nToken Tree'))
    # Print out the token tree
    pprint.pprint(token_tree)

    # Print out a header for the statistics
    print(colourise.cyan(f'\nStatistics for {script_name}'))
    # Print the number of tokens in the token tree
    print(f'\tNumber of Tokens: {len(raw_tokens)}')
    print(f'\tToken Tree Length: {len(token_tree)}')
    print('')


def perf_tokenisation(lines_for_parsing) -> dict:
    """Runs a performance check on the tokenisation.

    Args:
        lines_for_parsing [str]: the lines to run the performance check on

    Returns:
        perf_values [dict]: the speed scores of the tokenisation

    Raises:
        None
    """

    perf_values = {}

    # Hold the tokenising time
    tokenise_total_time = []
    # Set a counter
    count = 1
    for iteration in range(global_values.PERF_CHECK_EXECUTIONS):
        # Set the token list to nothing, otherwise the TOKEN_LIST just
        # grows in size
        tree.set_tokens([])
        # Print out the iteration
        print(
            f'{colourise.magenta("[TOKENISING]")} Iteration # ' +
            f'{count:n} of ' +
            f'{global_values.PERF_CHECK_EXECUTIONS:n}',
            end='\r'
        )
        # Get the start time
        start_token_planter = time.perf_counter()
        # Build the tokens (ie. tokenise)
        token_planter = planter.build_tokens(lines_for_parsing)
        # If index 0 is True, it means that the tokeniser has errored out so
        # report the error.
        if token_planter[0] is True:
            # Index 3 is the line number, index 1 is the error message
            messenger.line_error(
                token_planter[1],
                line_no=token_planter[3],
                error_code=8
            )
        # Get the end time
        end_token_planter = time.perf_counter()
        # Calclate the time that it took to tokenise
        tokenise_total_time.append(
            end_token_planter-start_token_planter
        )
        # Increment the counter
        count += 1
    # Get the average
    perf_values['average'] = statistics.fmean(tokenise_total_time)
    # Get the median
    perf_values['median'] = statistics.median(tokenise_total_time)
    # Get the standard deviation
    perf_values['stdev'] = statistics.stdev(tokenise_total_time)

    # Return the performance values
    return perf_values


def perf_tree_planting() -> dict:
    """Runs a performance check on the tokenisation.

    Args:
        None

    Returns:
        perf_values [dict]: the speed scores of the tokenisation

    Raises:
        None
    """

    perf_values = {}

    # Hold the timings
    tree_total_time = []
    # Set a counter
    count = 1
    for _ in range(global_values.PERF_CHECK_EXECUTIONS):
        # Set the token tree to nothing
        tree.set_tree({})
        # Print out the iteration
        print(
            f'{colourise.magenta("[TREE BUILD]")} Iteration # ' +
            f'{count:n} of ' +
            f'{global_values.PERF_CHECK_EXECUTIONS:n}',
            end='\r'
        )
        # Get the start time
        start_tree_building = time.perf_counter()
        # Build the tokens (ie. tokenise)
        planter.build_tree()
        # Get the end time
        end_tree_building = time.perf_counter()
        # Calclate the time that it took to tokenise
        tree_total_time.append(end_tree_building-start_tree_building)
        # Increment the counter
        count += 1
    # Get the average
    perf_values['average'] = statistics.fmean(tree_total_time)
    # Get the median
    perf_values['median'] = statistics.median(tree_total_time)
    # Get the standard deviation
    perf_values['stdev'] = statistics.stdev(tree_total_time)

    return perf_values


def print_dev_data(
                    script_name,
                    token_avg,
                    token_median,
                    token_stdev,
                    tree_avg,
                    tree_median,
                    tree_stdev):
    """Output data relevant to interpretation and save the results to disk

    Args:
        script_name: the name of the script
        token_avg: the time to tokenise as an average
        token_stdev: the standard deviation of tokenisation samples
        tree_ave: the average time to build the TOKEN_TREE
        tree_stdev: the standard deviation for tree building

    Returns:
        N/A

    Raises:
        None
    """

    # How much padding to indent text
    padding = 30

    # Get the tokens without them being "planted"
    raw_tokens = tree.get_tokens()
    # Get the token tree
    token_tree = tree.get_tree()

    # Number of raw tokens
    num_tokens = len(raw_tokens)
    # Number of branches in the token tree (ie. lines of code)
    num_lines = len(token_tree)

    print(colourise.yellow(f':: RESULTS FOR {script_name} ::'))
    executions = f'{global_values.PERF_CHECK_EXECUTIONS:,}'
    print(f'Executions: {str(executions)}')

    print(colourise.green('\nBASIC DATA'))
    # Get the number of tokens
    print(f'{"Tokens:".rjust(padding)} {num_tokens}')
    # Get the length of the tree
    print(f'{"Tree Length:".rjust(padding)} {num_lines}')
    # Average line length in tokens, rounded to two decimal places
    avg_tokens = round(num_tokens/num_lines, 2)
    print(
        f'{"Average Tokens per Line:".rjust(padding)} ' +
        f'{avg_tokens}'
    )

    print(colourise.green('\nTOKENISATION'))
    # Get the average tokenisation time
    print(f'{"Tokenisation Time [AVG]:".rjust(padding)} {token_avg}')
    # Get the median for tokenisation
    print(f'{"Tokenisation Time [MEDIAN]:".rjust(padding)} {token_median}')
    # Get the standard deviation for tokenisation
    print(f'{"Tokenisation Time [STDEV]:".rjust(padding)} {token_stdev}')

    print(colourise.green('\nTREE BUILDING'))
    # Get the average tree building time
    print(f'{"Tree Building Time [AVG]:".rjust(padding)} {tree_avg}')
    # Get the median for tree building
    print(f'{"Tree Building Time [MEDIAN]:".rjust(padding)} {tree_median}')
    # Get the standard deviation for tree building
    print(f'{"Tree Building Time [STDEV]:".rjust(padding)} {tree_stdev}')

    # Get the date and time for storing in the ~/.hs_profile.json file
    date_time = datetime.datetime.now()
    # Get a more friendly version of the date.
    # Thanks to https://www.geeksforgeeks.org/how-to-add-leading-zeros-to-a-
    # number-in-python/.
    perf_test_date = f'{date_time.year}/{date_time.month:02d}/' + \
        f'{date_time.day:02d}'
    perf_test_time = f'{date_time.hour:02d}:{date_time.minute:02d}:' + \
        f'{date_time.second:02d}'

    # Print out the success of the test
    print(colourise.magenta(f'\n:: Performance test complete at {date_time}'))

    # Get home directory to write out the results to a JSON file at
    # ~/.hs_profile.
    data_file = f'{str(pathlib.Path.home())}/.hs_profile.csv'
    # Collect the data in a dictionary
    data = {
        'date': perf_test_date,
        'time': perf_test_time,
        'executions': global_values.PERF_CHECK_EXECUTIONS,
        'num_tokens': num_tokens,
        'num_lines': num_lines,
        'avg_tokens': avg_tokens,
        'token_avg': token_avg,
        'token_median': token_median,
        'token_stdev': token_stdev,
        'tree_avg': tree_avg,
        'tree_median': tree_median,
        'tree_stdev': tree_stdev,
    }

    print(colourise.magenta(f':: Data added to {data_file}!\n'))

    # Set up the contents variable that will house the final CSV output
    contents = ''
    # Check to see if the ~/.hs_profile file exists
    if pathlib.Path(data_file).exists() is False:
        # If not, create our header row
        for key, _ in data.items():
            # Add the key (ie. the column header) to a running row
            contents += f'{key},'
        # Strip off the extra comma at the end
        contents = contents.strip(',')
        # Add a line after so that the data can be added to the file under
        # the header
        contents += '\n'

    # Loop over the values of the dictionary (ie. our data) and add it to the
    # contents variable
    for _, value in data.items():
        contents += f'{value},'

    # Strip off the lingering comma
    contents = contents.strip(',')

    # Open up the data file in append mode
    with open(data_file, 'a') as output:
        # Write the contents
        output.write(f'\n{contents}')
