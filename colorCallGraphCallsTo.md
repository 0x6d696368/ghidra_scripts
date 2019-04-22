# colorCallGraphCallsTo.py

This Ghidra script can be used to color all calls that are involved (as incoming edges) in the call graph
to the current address.

The `calls` will be colored `java.awt.Color.RED`.

## Usage

Just run the script at the location to which you would like to have all calls in the call graph
colored.

### Example:

Let's say you want to analyze the path from `main()` to code in function `foo()`.
You click on the address in function `foo()` that you would like to investigate
the path to and run the script.
Now you can navigate to `main()` and all calls that have a path to `foo()` will
be colored in red. This allows you to immediately see what calls are potentially
relevant.

