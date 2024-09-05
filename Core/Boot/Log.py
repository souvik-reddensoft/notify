import os
import logging
import json
import datetime
from logging.config import dictConfig
from google.cloud.logging import Client
from google.oauth2.service_account import Credentials
from Core.Boot.Bus import MessageBus
class KafkaLoggerHandler(logging.Handler):
    def __init__(self, topic_name):
        logging.Handler.__init__(self)
        self.topic_name = topic_name
        
    def emit(self, record):
        if record.module == 'Error':
            MessageBus.produce('APP', self.topic_name, self.format(record))
class JSONFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()

    def format(self, record):
        if hasattr(record, 'json_fields'):
            record.msg = json.dumps(
                {
                    **{
                        'message': record.getMessage(),
                    },
                    **record.json_fields,
                }, indent=4
            )
        return super().format(record)
class ErrorFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()

    def format(self, record):
        document = {
            'created_at': datetime.datetime.now(),
            'level': record.levelname,
            'thread': record.thread,
            'thread_name': record.threadName,
            # 'message': record.getMessage(),
            'logger_name': record.name,
            'fileName': record.pathname,
            'module': record.module,
            'method': record.funcName,
            'line_number': record.lineno,
            'app_slug' : "accounts",
        }
        if hasattr(record, 'json_fields'):
            document = {**document,**record.json_fields}
        return document


formatters = {
    'json_formatter': {
        '()': JSONFormatter
    },
    'error_formatter' : {
        '()': ErrorFormatter
    }
}
handlers = {
    'gcp': {
        'level': 'INFO',
        'class': 'google.cloud.logging.handlers.CloudLoggingHandler',
        'stream': 'ext://sys.stdout',
        'client': Client(
            credentials=Credentials.from_service_account_info({
                'project_id': os.environ.get('GCP_PROJECT_ID'),
                'private_key': os.environ.get('GCP_PRIVATE_KEY'),
                'client_email': os.environ.get('GCP_CLIENT_EMAIL'),
                'token_uri': os.environ.get('GCP_TOKEN_URI')
            })
        ),
    } if all(k in os.environ for k in (
        'GCP_PROJECT_ID',
        'GCP_PRIVATE_KEY',
        'GCP_CLIENT_EMAIL',
        'GCP_TOKEN_URI'
    )
    ) else {'class': 'logging.NullHandler'},
    'console': {
        'level': 'INFO',
        'formatter': 'json_formatter',
        'class': 'logging.StreamHandler',
        'stream': 'ext://sys.stdout',
    },
    'file': {
        'level': 'INFO',
        'formatter': 'json_formatter',
        'class': 'logging.handlers.TimedRotatingFileHandler',
        'filename': 'Logs/pypa.log',
        'when': 'midnight',
    },
    'db': {
        "()" : KafkaLoggerHandler,
        'topic_name' : 'error_logs_manage',
        'formatter': 'error_formatter',
    }
}
log_options = os.environ.get("LOG_OPTIONS").split("|") if os.environ.get(
    'LOG_OPTIONS') is not None else ['console']
dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': formatters,
    'handlers': {option: handlers[option] for option in log_options},
    'root': {
        'handlers': log_options,
        'level': 'INFO'
    }
})
