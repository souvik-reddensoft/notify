from flask import Flask, request

from flask_plugins import PluginManager, Plugin, connect_event, emit_event


def executePlugin(func):
    def doExecution(self, *args, **kwargs):
        AppPlugin.execEvent(
            f'before_{self.__class__.__name__.lower()}_{func.__name__}')
        data = func(self, *args, **kwargs)
        data = AppPlugin.execEvent(
            f'after_{self.__class__.__name__.lower()}_{func.__name__}', data)
        return data
    return doExecution

class AppPlugin(Plugin):
    event_dict = {}
    hook_dict = {}
    route_dict = {}

    @classmethod
    def handle(cls, app: Flask):
        PluginManager(app, plugin_folder='Plugins')
        cls.pushEvents(app)

    @classmethod
    def registerEvent(cls, event, callback, position) -> None:
        """Connect a callback to an event.  Per default the callback is
            appended to the end of the handlers but handlers can ask for a higher
            privilege by setting position.

            Example usage::

                def on_before_metadata_assembled(metadata):
                    metadata.append('<!-- IM IN UR METADATA -->')

                # And in your setup() method do this:
                    connect_event('before-metadata-assembled', on_before_metadata_assembled, 10)
        """
        plugin = callback.__module__.split('.')[-1]
        if position not in AppPlugin.event_dict:
            AppPlugin.event_dict = {
                **AppPlugin.event_dict,
                **{
                    position: {
                        f'{event}~{plugin}': callback
                    }
                }
            }
        elif f'{event}~{plugin}' not in AppPlugin.event_dict[position]:
            AppPlugin.event_dict[position] = {
                **AppPlugin.event_dict[position],
                **{
                    f'{event}~{plugin}': callback
                }
            }

    @classmethod
    def pushEvents(cls, app: Flask):
        with app.app_context():
            for priority in sorted(cls.event_dict.keys()):
                for event in cls.event_dict[priority]:
                    if callable(cls.event_dict[priority][event]):
                        event_name = event.split('~')[0]
                        if event_name not in cls.hook_dict:
                            cls.hook_dict[event_name] = []

                        if event not in cls.hook_dict[event_name]:
                            cls.hook_dict[event_name].append(event)

                        connect_event(
                            event, cls.event_dict[priority][event]
                        )

    @classmethod
    def execEvent(cls, event, data=None):

        if event in cls.hook_dict:
            # List of plugins are fetched from @app.before_request
            if not request.active_plugins is None:
                for hook in list(
                    filter(
                        lambda hook: hook.split(
                            '~')[-1] in request.active_plugins['plugins'],
                        cls.hook_dict[event]
                    )
                ):
                    plugin_data = emit_event(hook, data)
                    data = plugin_data[0] if len(plugin_data) != 0 else data
        return data
