import ast, os, re
import importlib.util
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog

class loadModules:

    def __init__(self):
        self.windowPointers = {}
        self.windowNames = []

    # pass this a list of files, it inspects them and then does the same
    #   thing as "import module", except it's done on a user-selected
    #   basis
    def load(self, classes):
        l = []

        print("THING: {0}".format(classes))
        if len(classes) > 0:
            directory = os.path.dirname(classes[0])
        else:
            print("no classes sent")
            return(l)
        
        classes = [os.path.basename(item) for item in classes]
        classes = [item for item in classes if item.endswith('.py')]

        # print("LOAD: {0} :: {1}".format(directory, classes))

        try:
            for py_file in classes:
                module_name = os.path.splitext(py_file)[0]
                full_module_name = f'{module_name}'  # Adjust the package name
                spec = importlib.util.spec_from_file_location("loaded_module", directory + '/' + py_file)
                loaded_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(loaded_module)

                # Check if the module has the desired class
                if hasattr(loaded_module, full_module_name):
                    # Instantiate the window class and show it
                    module_class = getattr(loaded_module, full_module_name)
                    print(module_class)
                    self.window_instance = module_class()
                    self.window_instance.show()
                    if full_module_name not in self.windowNames:
                        self.windowNames.append(full_module_name)
                        self.windowPointers[full_module_name] = self.window_instance
                else:
                    print("Module does not have a class named {0}".format(full_module_name))

        except Exception as e:
            print(f"Error loading or running module: {e}")

    # this takes the name of a window, and closes the object with that name.
    def killWindow(self, name):
        # make sure it has a function called 'close()'
        if hasattr(self.windowPointers[name], 'close') and callable(getattr(self.windowPointers[name], 'close')):
            # does it really unload an object if youre just closing the window? 
            self.windowPointers[name].close()
            self.windowPointers[name]= None
            if name in self.windowPointers:
                del self.windowPointers[name]
            if name in self.windowNames:
                self.windowNames.remove(name)
        else:
            print("The object is does not have the function 'close()'")

    # this parses the files but does not load the modules. 
    def testWithAST(self, directory):
        python_files = [f for f in os.listdir(directory) if f.endswith('.py')]

        returnDict = {}
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
                returnDict[name] = file_path

        return(returnDict)

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

