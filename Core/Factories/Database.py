import os
import importlib
# Importing in factory class file for type-hinting
from pymongo.collection import Collection
class DbFactory:

    instance: object

    def __init__(self, module_name, connection_name):
        self.module = f'Core.Engines.Connections.{module_name}'
        self.path = os.path.abspath(os.curdir) + f'/Core/Engines/Connections/{module_name}.py'
        self.connection = connection_name
        if not os.path.isfile(self.path):
            raise ImportError(self.path + " not found!")

    def create(self):
        instance =  getattr(importlib.import_module(self.module), self.connection)
        instance.connect()
        # Adding type-hinting
        DbFactory.instance:dict[str, Collection] = instance()