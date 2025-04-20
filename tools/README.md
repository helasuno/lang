# Helasuno Tools

## Description
This directory houses a set of simple tools to help you write compliant Helasuno code. These scripts can be run as regular Python scripts.

### reliner
This simple script will allow you to reline a script so that it is compliant with line numbering conventions (ie. lines as multiples of the first line).

This tool is also accessible via the `-r` flag in the interpreter which defaults to overwriting the script with line numbers that are multiples of 10.

#### Options
| Flag | Description |
|----|----|
| -w | The name of the newly relined file. If this is not provided, the original script is overwritten. |
| -m | This serves as the value of the first line and what each subsequent line will be a multiple of. If this is not provided, the default of 10 is used. |
