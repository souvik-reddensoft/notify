import os
import importlib
from dotenv import load_dotenv
load_dotenv()

class CacheFactory:
    instance: object = None
    def __init__(self):
        self.instance = None
        self.cache_type = os.getenv("DEFAULT_CACHE", default = None)
        if self.cache_type:
            self.cache_type = self.cache_type.capitalize()
            self.module = f'Config.Cache.{self.cache_type}'
            self.path = os.path.abspath(os.curdir) + f'/Config/Cache/{self.cache_type}.py'
            if not os.path.isfile(self.path):
                raise ImportError(self.path + " not found!")
            instance = getattr(importlib.import_module(self.module), self.cache_type)
            CacheFactory.instance = instance()