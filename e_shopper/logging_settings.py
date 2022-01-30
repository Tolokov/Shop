from datetime import datetime
from pythonjsonlogger.jsonlogger import JsonFormatter


class CustomJsonFormatter(JsonFormatter):
    """Модуль сохраняющий данные в json"""
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['time'] = datetime.utcnow().strftime('%Y-%m-%dT %H:%M')
        log_record['level'] = record.levelname
        log_record['name'] = record.name
        log_record['funcName'] = record.funcName


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '{asctime} - {filename} - {funcName} ',
            'style': '{',
        },
        'detail': {
            'format': '{asctime} - {levelname} - {filename} - {message}',
            'style': '{',
        },
        'json_formatter': {
            '()': CustomJsonFormatter
        }

    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'console_detail': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'detail',
        },
        'file_detail': {
            'class': 'logging.FileHandler',
            'formatter': 'json_formatter',
            'filename': 'log/shop_information.log'
        },
    },
    'loggers': {
        'Blog': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'Interactive': {
            'handlers': ['console_detail'],
            'level': 'DEBUG',
        },
        'Shop': {
            'handlers': ['console_detail', 'file_detail'],
            'level': 'INFO',
        },
    },
}
