#!/usr/bin/env python3

import ast, os
import inspect
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
    r = False
    if name in classes and 'MescalineSafe' in classes:
        r = True
    return(r)

def loadModules(directory):
    python_files = [f for f in os.listdir(directory) if f.endswith('.py')]
    print(python_files)

    l = []
    for py_file in python_files:
        module_name = os.path.splitext(py_file)[0]
        print(module_name)
        full_module_name = f'{module_name}'  # Adjust the package name

        try:
            module_path = os.path.join(directory, py_file)
            spec = importlib.util.spec_from_file_location(full_module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            try:
                if inspect_module(full_module_name, module):
                    print("SAFE: {0}".format(full_module_name))
                else: 
                    print("NOT SAFE: {0}".format(full_module_name))
            except Exception as e:
                print(f"ERROR not seeing the right functions in module: {e}")
                pass

        except Exception as e:
            print(f"ERROR loading or running module: {e}")

    return(l)

# Specify the directory containing the modules
module_directory = './APPS'

classes_found = testWithAST(module_directory)

print(f'Classes found in {module_directory}: {classes_found}')

l = loadModules(module_directory)




