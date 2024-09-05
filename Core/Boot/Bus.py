import logging
import os
import inspect
from functools import reduce
import sys
from threading import Thread
import traceback
from bson.json_util import loads, dumps
from kafka import KafkaConsumer, KafkaProducer, TopicPartition
import subscribers


class MessageBus:
    __producers = {}
    __arguments = {
        'security_protocol': '_EVENT_SECURE_PROTOCOL',
        'sasl_mechanism': '_EVENT_SECURE_PROTOCOL_MECHANISM',
        'sasl_plain_username': '_EVENT_SECURE_PROTOCOL_USERNAME',
        'sasl_plain_password': '_EVENT_SECURE_PROTOCOL_PASSWORD',
    }

    def __init__(self):
        raise Exception('Class not intended to be instantiated')
    
    @classmethod
    def isJson(cls, data):
        try:
            loads(data)
            return True
        except Exception as ex:
            return False

    @classmethod
    def load(cls, env_event_keys: list):
        for key in env_event_keys:
            if (os.environ.get("FLASK_ENV") != "development" or os.environ.get("WERKZEUG_RUN_MAIN") == "true") and f'{key}_EVENT_BROKER' in os.environ:
                configs = {index: os.environ.get(f'{key + value}')  for index,value in cls.__arguments.items() if f'{key + value}' in os.environ}
                cls.__producers[key] = KafkaProducer(
                    bootstrap_servers=os.environ.get(f'{key}_EVENT_BROKER'),
                    value_serializer=lambda m: dumps(m).encode('utf-8'),
                    **configs
                )
                for event_class in inspect.getmembers(subscribers, inspect.isclass):
                    if event_class[0].upper() == key + 'EVENT':
                        for func in inspect.getmembers(event_class[1], inspect.ismethod):
                            topic_generated = reduce(lambda x, y: x + ('_' if y.isupper() else '') + y, func[0]).lower()
                            topic = f'{topic_generated}_{os.getenv("RED_ENV")}'
                            Thread(
                                target=cls.consume,
                                kwargs={
                                    'topic': topic,
                                    'callback': func[1],
                                    'env_key': key,
                                    'configs': configs
                                },
                                daemon=True
                            ).start()

    @classmethod
    def consume(cls, env_key, configs, topic, callback):
        consumer = KafkaConsumer(
            bootstrap_servers=os.environ.get(f'{env_key}_EVENT_BROKER').split('|'),
            group_id=os.environ.get(f'{env_key}_EVENT_GROUP_ID'),
            value_deserializer=lambda m: loads(m.decode('utf-8')) if MessageBus.isJson(m) else str(m).encode('utf-8'),
            auto_offset_reset='earliest',
            **configs
        )
        consumer.assign(
            [TopicPartition(topic, int(os.environ.get(f'{env_key}_EVENT_PARTITION', 0)))]
        )

        for message in consumer:
            try:
                callback(message.value)
            except Exception as ex:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logging.error(
                    ex.__class__.__name__,
                    extra={
                        'json_fields': {
                            'error': ex.args[0],
                            'traceback': [
                                {
                                    'file': trace.filename,
                                    'line': trace.line,
                                    'line_no': trace.lineno,
                                    'func_name': trace.name
                                } for trace in traceback.extract_tb(exc_tb)
                            ]
                        }
                    }
                )

    @classmethod
    def produce(cls, env_key, topic, value):
        if env_key in  cls.__producers:
            topic = f'{topic}_{os.getenv("RED_ENV")}'
            cls.__producers[env_key].send(topic, value=value, partition=int(
                os.environ.get(f'{env_key}_EVENT_PARTITION', 0)))
