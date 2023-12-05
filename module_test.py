#!/usr/bin/env python3

import os
import inspect
import importlib.util

def inspect_module(name, module):
    module_attributes = dir(module)
    functions_and_methods = [attr for attr in module_attributes if callable(getattr(module, attr))]
    classes = [attr for attr in module_attributes if isinstance(getattr(module, attr), type)]
    r = False
    if name in classes and 'MescalineSafe' in classes:
        r = True
    return(r)

def findModules(directory):
    python_files = [f for f in os.listdir(directory) if f.endswith('.py')]

    l = []
    for py_file in python_files:
        module_name = os.path.splitext(py_file)[0]
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


def load_and_run_module(directory, class_name):
    python_files = [f for f in os.listdir(directory) if f.endswith('.py')]

    for py_file in python_files:
        module_name = os.path.splitext(py_file)[0]
        full_module_name = f'{module_name}'  # Adjust the package name

        try:
            # Dynamically loads modules. Completely unsafe: in that it
            #   could load a malicious module from this directory
            module_path = os.path.join(directory, py_file)
            spec = importlib.util.spec_from_file_location(full_module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            safeToLoad = False
            names = []
            for name, obj in inspect.getmembers(module):
                names.append(name)
            if "MescalineSafe" in names and \
               full_module_name in names:
                    safeToLoad = True
                    
            if safeToLoad:
                for name, obj in inspect.getmembers(module):
                    if name == full_module_name:
                        print ("LAUNCH: {0}".format(name))
                    if name not in "__builtins__":
                        print("stuff: {0} :: {1}".format(name, obj))

                if hasattr(module, 'ExampleModule') and callable(getattr(module.ExampleModule, 'print_info', None)):
                    # Create an instance of the class and run the print_info method
                    instance = module.ExampleModule()
                    instance.print_info()
                else:
                    print(f'Module {full_module_name} does not have the ExampleModule class or the print_info method.')

        except Exception as e:
            print(f"Error loading or running module {full_module_name}: {e}")

# Specify the directory containing the modules
module_directory = './APPS'


l = findModules(module_directory)
# load_and_run_module(module_directory, "ExampleModule")



