## Helasuno Scripting Language
Helasuno (hee-la-sue-no), coming from the (butchered) blending of the Esperanto words "bright" (hela) and "sun" (suno), is a simple non-structured scripting language started in 2024. Inspired loosely by BASIC and a desire to learn more about parsing text, the language will likely serve no practical purpose other than learning.

The entire language is written in pure Python (>= 3.12) with no third party dependencies. If it can't be done with the standard library, it won't be done.

[See the homepage for more information](https://bryanabsmith.com/helasuno). See also the [TESTING](TESTING.md) document for more about the status of language features.

### Layout

| Path | Description |
|---|---|
| src/ | Source code for the interpreter. |
| tests/ | Unit tests. |
| tools/ | Tools for use in the language. |


### Quick Start
First and foremost, you need a working Python installation. The language is written in pure Python so a working version of Python installed that is >= version 3.12 will do.

If you just want to get going, you can run the following on a *nix (macOS, Linux, BSD) system:

    git clone https://github.com/helasuno/lang.git
    cd lang/
    python3 package.py

The above will create an executable Python zipapp in `dist/` that will work well across *nix platforms. If `vsce` is installed, a Visual Studio Code extension will also be available in `dist/`.

On a more conventional *nix system (macOS/Linux/BSD), you can use the included Makefile.

    make

This will clean the `src/` directory, (re)compile the bytecode, and create the interpreter along with source distributions in `src/` directory. This is the same as:

    make clean bytecode package source

If you want to make the interpreter package and install it (in /usr/local/bin/), you can run the conventional pattern:

    make && sudo make install

**NOTE: If you're using FreeBSD, you will need to install Python 3.12 from Ports (lang/python312). As of now (06/05/2025), FreeBSD's bianry packages of Python 3 are only 3.11.**

#### Making a Release Build
There are a few steps to making a release ready version of the interpreter:
1. Run `make clean` to clean out the caches (pycaches and ruff caches).
2. Set `etc/global_values.py` -> `LANG_DEV_VERSION` to `False`.
3. Run `make` or `python3 package.py` to build the package.


### Using the Interpreter
Using Helasuno is similar to any other interpreter:

    helasuno [name of script]


## Licence
The code and materials are provided under the MIT licence.

### MIT Licence
Copyright 2024-2025 Bryan Smith.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.