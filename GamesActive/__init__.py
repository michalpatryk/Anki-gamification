import os
from importlib import import_module


def loadFiles():
    modules = []
    moduleName = 'GamesActive'
    path = os.path.split(__file__)[0]
    for folder in os.listdir(os.path.abspath(path)):
        if os.path.isdir(os.path.join(path, folder)):
            for file in os.listdir(os.path.abspath(os.path.join(path, folder))):
                if file == '__init__.py':
                    module = import_module(
                        moduleName + '.' + folder + '.' + file[:-3])
                    modules.append(module.load())
    return modules
