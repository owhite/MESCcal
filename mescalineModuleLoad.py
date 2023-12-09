import ast, os, re
import importlib.util
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5.QtCore import Qt, QTimer

### The code responsible for finding modules, testing them, runs them and creating new
###    PYQT windows that are selected by the user
### 
# Tried to follow this nomenclature:
#  modules: files that contain a python module
#  classes: are the attributes in a module (e.g. "__init__" and "def function(self)"
#  windows: are the things that get launched when exec_module is called on a module
#     and a PYQT5 window comes up
#  apps: in many parts of the code windows are also called apps

class loadModules(QtWidgets.QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.classNames = [] # contains all known classes
        self.windowPointers = {} # contains only the windows that are loaded
        self.windowNames = [] # contains names of the windows that are loaded
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.checkWindowStatus)
        self.timer.start(500)

    # pass this a list of files, it inspects them and then does the same
    #   thing as python's "import module", except it's performed on a 
    #   the files found in the app director
    def load(self, classes):
        if len(classes) > 0:
            directory = os.path.dirname(classes[0])
        else:
            print("no classes sent")
        
        classes = [os.path.basename(item) for item in classes]
        classes = [item for item in classes if item.endswith('.py')]

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
                    self.window_instance = module_class()
                    self.window_instance.show()
                    if full_module_name not in self.windowNames:
                        self.windowNames.append(full_module_name)
                        self.windowPointers[full_module_name] = self.window_instance
                else:
                    print("Module does not have a class named {0}".format(full_module_name))

        except Exception as e:
            print(f"Error loading or running module: {e}")

    # tests if the app no longer exists. for example if the user closed the
    #   by click on the apps close button
    def checkWindowStatus(self):
        for name in self.classNames:
            window  = self.windowPointers.get(name)
            if window != None:
                if window.isHidden():
                    # print(f"Child window has been closed: {window}")
                    self.killWindow(name)

    # this takes the name of a window, and closes the object with that name.
    def killWindow(self, name):
        # make sure it has a function called 'close()'
        if hasattr(self.windowPointers[name], 'close') and \
        callable(getattr(self.windowPointers[name], 'close')):
            # does it really unload an object if youre just closing the window? 
            self.windowPointers[name].close()
            self.windowPointers[name]= None
            if name in self.windowPointers:
                del self.windowPointers[name]
            if name in self.windowNames:
                self.windowNames.remove(name)
        else:
            print("The object is does not have the function 'close()'")

    # parses files in directory to make a list of them
    #   does not actually load the files into memory
    def testWithAST(self, directory):
        python_files = [f for f in os.listdir(directory) if f.endswith('.py')]

        returnDict = {}
        for name in python_files:
            file_path = directory + '/' + name
            name = name.replace('.py', '')
            self.classNames.append(name)
            with open(file_path, 'r') as file:
                tree = ast.parse(file.read(), filename=file_path)

            class_names = []
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_names.append(node.name)

            # this wins the "painful lack of testing" award
            if "MescalineSafe" in class_names and name in class_names:
                returnDict[name] = file_path

        return(returnDict)


