from Core.Boot.Plugin import *

__plugin__ = "CustomHook"
__version__ = "1.0.0"

class CustomHook(AppPlugin):

    def setup(self):
        def doEvent(data):
            print('I\'m a custom hook')

        AppPlugin.registerEvent('trigger_custom_hook', doEvent, 1)