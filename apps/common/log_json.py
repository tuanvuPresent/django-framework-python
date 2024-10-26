import logging.config
import logging

from pythonjsonlogger import jsonlogger


logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'fmt': '%(asctime)s %(name)s %(levelname)s %(message)s %(filename)s %(lineno)s %(process)d %(thread)d',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'json',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
})
access_logger = logging.getLogger('access_log')


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        log_record['level'] = record.levelname
        log_record['name'] = record.name
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)


def get_logger(name, level=logging.DEBUG):
    log_handler = logging.StreamHandler()
    log_handler.setFormatter(CustomJsonFormatter())

    _logger = logging.getLogger(name)
    _logger.setLevel(level)
    _logger.addHandler(log_handler)
    return _logger


debug_logger = get_logger('debug')
debug_logger.info("info", extra={"special": "value", "run": 12})
