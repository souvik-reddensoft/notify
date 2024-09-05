from Core.Boot.Plugin import *

__plugin__ = "AfterHook"
__version__ = "1.0.0"

class AfterHook(AppPlugin):

    def setup(self):
        def doEvent(data):
            print('Do After Hook Event')
            return data
        def doEvent2(data):
            print('Do After Hook Response Tampering')
            data['fields'].update(tampered_field = 'This is my Tampered Response')
            return data

        AppPlugin.registerEvent('after_demo_list', doEvent, 2)
        AppPlugin.registerEvent('after_demo_list', doEvent2, 1)