import logging
from telegram.utils.helpers import escape_markdown, escape_html

_logger = logging.getLogger(__name__)


def log(logger, print_ret=True, print_args=False):
    import functools

    def wraps(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            if print_args:
                printed_args = ', passed {0} and {1}'.format(args, kwargs)
            else:
                printed_args = ''
            logger.debug('Entering {0}{1}'.format(f.__qualname__, printed_args))
            result = f(*args, **kwargs)
            if print_ret:
                ret = ', returned {0}'.format(result)
            else:
                ret = ''
            logger.debug('Exited {0}{1}'.format(f.__qualname__, ret))
            return result
        return wrapper
    return wraps


@log(_logger)
def get_lang(data, user):
    if data.languages:
        lang = data.languages.get(user.id, user.language_code)
    else:
        lang = user.language_code
    return lang

