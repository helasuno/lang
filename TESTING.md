## Testing Status
This document tracks the status of testing, both what is planned and what is coming.

### Operating System Testing
This section outlines testing across platforms. Given that the interpreter is written in pure Python, anywhere that Python is supported should work. In that sense, this is more about any notes to keep in mind when trying to run the interpreter on a particular platform.

**Legend**
- &#10003; = tested
- &#10008; = not tested / something broken (see notes)

| Operating System / Distribution | Status | Notes |
|----|----|----|
| BSD - FreeBSD 14.2 | &#10003;* | The version of Python available as a binary package is too old (3.11 as of 06/05/2025). You will need to build the `lang/python312` port if you're relying on binary pkgs. |
| BSD - NetBSD 10.1 | &#10003; | None but Python is not installed by default. |
| BSD - OpenBSD 7.6 | &#10008; | OpenBSD gets tested very infrequently. Should be fine though as it seems like Python 3.12.x is the default Python version (as of 06/05/2025). |
| Linux - Fedora 42 | &#10003; | None |
| Linux - Ubuntu 25.04 | &#10003; | None |
| Linux - openSUSE Leap 15.6 | &#10003;* | Works but you need to install Python >= 3.12 (`zypper in python312`) as Leap comes witn Python 3.6.x. |
| macOS 15.4.x | &#10003; | Development is done on a Mac so it's likely to be both the most broken and most stable at the same time. |
| Windows 11 | &#10003; | None |

### Statements
This section outlines the status of testing with each statement.

**Legend**
- &#10003; = done (safe to assume it works)
- &#8277; = in testing (50/50 chance it works)
- &#10008; = not tested / something broken (see notes)

| Statement | Status | Notes |
|----|----|----|
| end | &#8277; |  |
| get | &#8277; |  |
| jump | &#8277; |  |
| pause | &#8277; |  |
| set | &#8277; |  |
| write(ln) | &#10003; | Assumed to work at this point |