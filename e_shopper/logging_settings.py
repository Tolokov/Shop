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
            'handlers': ['console_detail'],
            'level': 'INFO',
        },
    },
}
