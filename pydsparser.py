import ast
import sys
import os



def parse_python_file_to_markdown(py_file_path):
    """
    This function parses a Python file and converts it into a Markdown file.

    Args:
        file_path (str): The path to the Python file to be parsed.

    Returns:
        str: The content of the Python file converted into Markdown format.
    """

    print("Starting the process of parsing the Python file to Markdown...")

    # Print the name of the Python file being read
    print(f"Reading Python file: {py_file_path}")
    # Open the Python file in read mode
    with open(py_file_path, 'r') as file:
        # Read the content of the Python file
        py_content = file.read()

    # Print a message to indicate the start of the parsing process
    print("Parsing the Python file...")
    # Parse the content of the Python file into an Abstract Syntax Tree (AST)
    tree = ast.parse(py_content)

    # Print a message to indicate the initialization of the documentation sections
    print("Initializing the Table of Contents, Classes Documentation, and Functions Documentation...")
    # Initialize the Table of Contents section
    toc = ["# Table of Contents\n"]
    # Initialize the Classes Documentation section
    class_docs = ["# Classes Documentation\n"]
    # Initialize the Functions Documentation section
    func_docs = ["# Functions Documentation\n"]

    # Parse the content of the Python file into an Abstract Syntax Tree (AST)
    tree = ast.parse(py_content)

    # Add parent references to each node in the AST
    # This enhances the AST with parent references, which are not provided by Python's `ast` module by default
    add_parent_references(tree)

    print("Walking through the AST nodes...")
    # Initialize an empty list to store the documentation for each module in the Python file
    module_docs = []
    # Iterate over all nodes in the Abstract Syntax Tree (AST)
    for node in ast.walk(tree):
        # Check if the node is an assignment, its target is a name, the name is 'module_docstring', the value of the assignment is a constant, and the value of the constant is a string
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id == 'module_docstring' and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            # Print a message indicating that a module-level docstring was found
            print(f"Found a module-level docstring")
            # Append the module-level docstring to the module documentation
            module_docs.append(f"# Module Documentation\n\n{node.value.value}\n")            
            # Append a link to the module documentation in the Table of Contents
            toc.append(f"- [Module Documentation](#module-documentation)\n")
            # Append a horizontal rule to the module documentation
            module_docs.append("\n<hr>\n")

        # Check if the node is a class definition and it has a docstring
        if isinstance(node, ast.ClassDef) and ast.get_docstring(node):
            # Print a message indicating that a class with a docstring was found
            print(f"Found a class with a docstring: {node.name}")
            # Convert the class name to lowercase and replace spaces with hyphens for URL compatibility
            class_name_for_url = node.name.lower().replace(' ', '-')
            # Append a link to the class in the Table of Contents
            toc.append(f"- [Class: {node.name}](#{class_name_for_url})\n")

            # Append the class name to the Classes Documentation section
            class_docs.append(f"<br/>\n\n## <div id='{class_name_for_url}'>Class: {node.name}</div>\n")
            # Append a styled div for the class documentation
            class_docs.append(f"\n\n<div style='border:1px dotted darkgrey; padding:10px; margin:5px;'>\n")

            # Get the docstring of the class
            docstring = ast.get_docstring(node)
            # Split the docstring into lines and iterate over them
            for line in docstring.split('\n'):
                # If the line ends with a colon, format it as a subheading
                if line.endswith(':'):
                    class_docs.append(f"### {line}\n")
                else:
                    # Otherwise, append the line as is
                    class_docs.append(f"{line}\n")
            
            # Initialize an empty list to store the documentation for each method in the class
            methods = []

            # Iterate over all nodes in the class body
            for method in node.body:
                # Check if the node is a function definition and it has a docstring
                if isinstance(method, ast.FunctionDef) and ast.get_docstring(method):
                    # Print a message indicating that a method with a docstring was found
                    print(f"Found a method with a docstring in class {node.name}: {method.name}")
                    # Get the method name
                    method_name = method.name
                    # Convert the method name to lowercase and replace spaces with hyphens for URL compatibility
                    method_name_for_url = method_name.lower().replace(' ', '-')
                    # Append a link to the method in the Table of Contents
                    toc.append(f"  - [Method: {method_name}](#{method_name_for_url})\n")
                    # Print the method name
                    print(f"Method name: {method_name}")

                    # Initialize the method documentation with the method name
                    method_doc = [f"\n#### <span id='{method_name}' style='background-color: darkblue; color: white; padding: 2px 5px;'>{method_name}</span>\n<hr>\n"]

                    # Get the docstring of the method
                    docstring = ast.get_docstring(method)
                    # Split the docstring into lines and iterate over them
                    for line in docstring.split('\n'):
                        # If the line ends with a space followed by a colon, format it as a sub-subheading
                        if line.endswith(' :'):
                            print(f"Found a line that ends with a space followed by a colon: {line}")
                            method_doc.append(f"##### {line}\n")
                        else:
                            # Otherwise, append the line as is
                            method_doc.append(f"{line}\n")

                    # Append the method documentation to the list of method documentations
                    methods.append(''.join(method_doc))

            # If there are any methods in the class
            if methods:
                # Append a Methods subheading to the Classes Documentation section
                class_docs.append("\n\n### Methods:\n<div style='margin-left: 20px;'>\n\n")
                # Append the method documentations to the Classes Documentation section
                class_docs.extend(methods)
                # Append a closing div tag to the Classes Documentation section
                class_docs.append("</div>\n")

            # Append a closing div tag to the Classes Documentation section
            class_docs.append("</div>\n")

        # Check if the node is a function definition, it has a docstring, and its parent is a module
        # This is to ensure that we only document top-level functions, not methods within classes
        elif isinstance(node, ast.FunctionDef) and ast.get_docstring(node) and isinstance(node.parent, ast.Module):
            # Print a message indicating that a function with a docstring was found
            print(f"Found a function with a docstring: {node.name}")
            # Append a link to the function in the Table of Contents
            toc.append(f"- [Function: {node.name}](#{'function-' + node.name.lower()})\n")
            # Append the function name to the Functions Documentation section
            func_docs.append(f"\n\n## Function: {node.name}\n<div style='margin-left: 20px;'>\n\n")

            # Get the docstring of the function
            docstring = ast.get_docstring(node)
            # Split the docstring into lines and iterate over them
            for line in docstring.split('\n'):
                # If the line ends with a colon, format it as a subheading
                if line.endswith(':'):
                    func_docs.append(f"### {line}\n")
                else:
                    # Otherwise, append the line as is
                    func_docs.append(f"{line}\n")

            # Append a closing div tag to the Functions Documentation section
            func_docs.append("</div>\n")

    print("Finished walking through the AST nodes.")
    # Check if the Table of Contents contains more than one item
    # This would mean that classes and/or functions with docstrings were found
    if len(toc) > 1:
        # Print a message indicating that classes and/or functions with docstrings were found and a markdown file is being created
        print("Classes and/or functions with docstrings found. Creating markdown...")
        # Return the markdown content, which is a concatenation of the Table of Contents, module documentation, class documentation, and function documentation
        return ''.join(toc) + '\n' + ''.join(module_docs) + '\n' + ''.join(class_docs) + '\n' + ''.join(func_docs)
    else:
        # If the Table of Contents contains only one item, this means that no classes or functions with docstrings were found
        print("No class or function with a docstring found.")
        # Return a message indicating that no classes or functions with docstrings were found
        return "No class or function with a docstring found."
    
    
def add_parent_references(node):
    """
    This function adds a parent reference to each child node in an Abstract Syntax Tree (AST).

    Args:
        node (ast.AST): The root node of the AST.
    """    
    # Iterate over all direct child nodes of the current node
    for child in ast.iter_child_nodes(node):
        # Set the parent attribute of the child node to the current node
        child.parent = node
        # Recursively call the function for the child node
        add_parent_references(child)

def main():
    # Check for correct usage
    if len(sys.argv) != 3:
        print("Usage: python pydsparser.py input.py output.md")
        sys.exit(1)

    # Get the path of the input Python file from the command line arguments
    input_path = sys.argv[1]
    # Get the path of the output Markdown file from the command line arguments
    output_path = sys.argv[2]

    # Create the target directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Parse the Python file to markdown format
    markdown_content = parse_python_file_to_markdown(input_path)

    # Write the markdown content to the output file
    with open(output_path, 'w') as file:
        file.write(markdown_content)

    # Print console message indicating successful creation of the markdown file
    print(f"Markdown file created at {output_path}")

if __name__ == "__main__":
    main()
