# Python to Markdown Parser

This script, `pydsparser.py`, is designed to parse Python files and convert them into detailed Markdown documentation. It automatically generates a Table of Contents, classes, functions documentation, and more from the docstrings in the Python code.

## Features

- **Table of Contents Generation:** Automatically creates a clickable table of contents based on the documented elements.
- **Classes and Functions Documentation:** Parses and formats docstrings from classes and functions.
- **AST-Based Parsing:** Utilizes Python's Abstract Syntax Tree (AST) for accurate parsing.

## Installation

No external libraries are required for this script. It uses standard Python libraries `ast`, `sys`, and `os`. Ensure you have Python installed on your system.

## Usage

To use the script, simply pass the input Python file and the desired output Markdown file path as command-line arguments:

```bash
python pydsparser.py input.py output.md
```

### Example

If you have a Python file named `example.py`, you can generate its documentation as follows:

```bash
python pydsparser.py example.py example.md
```

The Markdown file `example.md` will be created with the parsed documentation.

## Contributing

Contributions to enhance the script's functionality or documentation are welcome. Please feel free to fork the repository, make your changes, and create a pull request.

## License

This script is provided under the MIT License. See the LICENSE file for more details.
