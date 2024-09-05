from flask import request
from Core.Boot.Plugin import *

__plugin__ = "BeforeHook"
__version__ = "1.0.0"

class BeforeHook(AppPlugin):

    def setup(self):
        def doEvent(data): # pylint: disable=no-member
            print('Do Before Hook Event')
        def doEvent2(data):
            print('Do Before Hook Filter Request')
            request.args.update(plugin_param = 'Test')

        AppPlugin.registerEvent('before_demo_list', doEvent, 2)
        AppPlugin.registerEvent('before_demo_list', doEvent2, 1)