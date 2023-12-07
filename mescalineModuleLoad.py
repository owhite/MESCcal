#!/usr/bin/env python3

import ast, os, re
import importlib.util

class loadModules:

    def __init__(self):
        pass

    def load(self, directory, classes):
        python_files = [f for f in os.listdir(directory) if f.endswith('.py')]
        classes = [item for item in classes if item.endswith('.py')]
        classes = [re.sub(r'.*\/', '', item) for item in classes]

        try:
            l = []
            for py_file in classes:
                module_name = os.path.splitext(py_file)[0]
                full_module_name = f'{module_name}'  # Adjust the package name
                print (full_module_name)
                print (directory + '/' + py_file)
                spec = importlib.util.spec_from_file_location("loaded_module", directory + '/' + py_file)
                loaded_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(loaded_module)

                print("Module loaded successfully.")
                # Check if the module has the desired class
                if hasattr(loaded_module, full_module_name):
                    # Instantiate the secondWindow class and show it
                    module_class = getattr(loaded_module, full_module_name)
                    self.window_instance = module_class()
                    self.window_instance.show()
                    l.append(self.window_instance)
                    print("Window shown.")
                else:
                    print("Module does not have a class named 'secondWindow.'")

        except Exception as e:
            print(f"Error loading or running module: {e}")

        return(l)

    # this parses the files but does not load the modules. 
    def testWithAST(self, directory):
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

    def inspect_module(self, name, module):
        module_attributes = dir(module)
        functions_and_methods = [attr for attr in module_attributes if callable(getattr(module, attr))]
        classes = [attr for attr in module_attributes if isinstance(getattr(module, attr), type)]
        r = False

        print(module_attributes)
        print(functions_and_methods)
        print(classes)

        if name in classes and 'MescalineSafe' in classes:
            r = True
        return(r)

