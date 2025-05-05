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
A module that holds globally accessible values for the language.
'''

# How many executions of functions to run with performance check enabled
PERF_CHECK_EXECUTIONS = 100000

# Language name
LANG_NAME = 'Helasuno'
# Language name acronym
LANG_NAME_ACRONYM = 'hs'
# Language name in lowercase
LANG_NAME_LOWER = LANG_NAME.lower()
# Language version
LANG_VERSION = 0.1
# Whether this is a development version or not.
# FOR EACH RELEASE, MAKE SURE THIS IS SET TO FALSE
LANG_DEV_VERSION = True

# Get the platform architecture
PLAT_ARCH = platform.machine()
# Get the platform system
PLAT_SYSTEM = platform.system()

# Python version
PYTHON_VERSION = platform.python_version_tuple()
# Minimum Python version
PYTHON_VERSION_MINIMUM = '3.12'
# Minimum Python version (minor)
PYTHON_VERSION_MINIMUM_MINOR = 12
