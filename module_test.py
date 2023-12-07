#!/usr/bin/env python3

import ast, os, re
import importlib.util

# this parses the files but does not load the modules. 
def testWithAST(directory):
    python_files = [f for f in os.listdir(directory) if f.endswith('.py')]

    returnList = []
    for name in python_files:
        file_path = directory + '/' + name
        name = name.replace('.py', '')

        with open(file_path, 'r') as file:
            tree = ast.parse(file.read(), filename=file_path)

        class_names = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_names.append(node.name)

        if "MescalineSafe" in class_names and name in class_names:
            returnList.append(file_path)

    return(returnList)

def inspect_module(name, module):
    module_attributes = dir(module)
    functions_and_methods = [attr for attr in module_attributes if callable(getattr(module, attr))]
    classes = [attr for attr in module_attributes if isinstance(getattr(module, attr), type)]

    print("INSPECT")
    print(module_attributes)
    print(functions_and_methods)
    print(classes)

    r = False
    if name in classes and 'MescalineSafe' in classes:
        r = True
    return(r)

def loadModules(directory, classes):
    python_files = [f for f in os.listdir(directory) if f.endswith('.py')]
    classes = [item for item in classes if item.endswith('.py')]
    classes = [re.sub(r'.*\/', '', item) for item in classes]

    try:
        l = []
        for py_file in classes:
            module_name = os.path.splitext(py_file)[0]
            full_module_name = f'{module_name}'  # Adjust the package name
            print (full_module_name)
            spec = importlib.util.spec_from_file_location("loaded_module", py_file)
            loaded_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(loaded_module)

            print("Module loaded successfully.")
            # Check if the module has a class named 'secondWindow'
            if hasattr(loaded_module, 'secondWindow'):
                # Instantiate the secondWindow class and show it
                self.window_instance = loaded_module.secondWindow()
                self.window_instance.show()
                print("Window shown.")
            else:
                print("Module does not have a class named 'secondWindow.'")

    except Exception as e:
        print(f"Error loading or running module: {e}")

    return(l)

# Specify the directory containing the modules
module_directory = './APPS'

classes_found = testWithAST(module_directory)

print(f'Classes found in {module_directory}: {classes_found}')

l = loadModules(module_directory, ['./APPS/secondWindow.py'])

print(l)


