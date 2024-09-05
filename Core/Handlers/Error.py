import os
import sys
import logging
import json
import traceback
from flask import Response, request
from werkzeug.exceptions import HTTPException
class ErrorHandler:

    @staticmethod
    def handle(ex: Exception):
        exc_type, exc_obj, exc_tb = sys.exc_info()  # pylint: disable=unused-variable
        ex_trace = [
            {
                'file': trace.filename,
                'line': trace.line,
                'line_no': trace.lineno,
                'func_name': trace.name
            } for trace in traceback.extract_tb(exc_tb)
        ]
        if 'errors' in ex.__dict__:
            status_code = ex.code
            response = {
                'success': False,
                'message': ex.errors,
                'error': {
                    'module-code': os.environ.get('SERVICE_MODULE_CODE', '') + str(ex.code),
                    'name': ex.name
                }
            }
        elif isinstance(ex, HTTPException):
            status_code = ex.code
            response = {
                'success': False,
                'message': ex.description,
                'error': {
                    **{
                        'module-code': os.environ.get('SERVICE_MODULE_CODE', '') + str(ex.code),
                        'name': ex.name
                    },
                    **(
                        {
                            'traceback': ex_trace
                        } if (os.environ.get('FLASK_ENV') != 'production') else {}
                    )
                }
            }
        else:
            status_code = 500
            response = {**{
                'success': False,
                'message': request.t('error.' + str(status_code), default='Something went wrong'),
                'error': {
                    'module-code': os.environ.get('SERVICE_MODULE_CODE', '') + str(ex.code if hasattr(ex, 'code') else 500),
                    'name': ex.__class__.__name__,
                    'description': list(ex.args)
                }
            },
                **(
                {
                    'traceback': ex_trace
                } if (os.environ.get('FLASK_ENV') != 'production') else {}
            )
            }
            logging.error(
                ex.__class__.__name__,
                extra={
                    'json_fields': {
                        'error': response['error'],
                        # pylint: disable=duplicate-code
                        'http_request': {
                            'remote-address': request.remote_addr,
                            'method': request.method,
                            'url': request.url,
                            'http-version': request.environ.get('SERVER_PROTOCOL'),
                            'user-agent': request.user_agent.string,
                            'status-code': status_code
                        },
                        'traceback': ex_trace
                    }
                }
            )

        return Response(json.dumps(response), status=status_code, mimetype='application/json')
