# My Ghidra scripts

A collection of some useful Ghidra scripts I come up with.
This is a personal repository. So while you can open issues,
I won't guarantee any bug fixes, improvements, etc.

Scripts only tested with CentOS 7.

## Documentation

Each script has a `.md` file with its documentation.

## Dependencies

- YaraSearch.py: `yara` must be in `$PATH`
- GoogleSearch.py: Needs `firefox` in `$PATH`

For details please see each script's `.md` file.

## Install

Copy the script(s) (you like to use) to your `ghidra_scripts` folder (usually located
at `~/ghidra_scripts`) or any other directory Ghidra is configured to search for
scripts.


## TODO

- Make `SearchStackStrings.py` call `StackStrings.py` internally.
- Improve `StackStrings.py` to handle different and more complex strack strings.


