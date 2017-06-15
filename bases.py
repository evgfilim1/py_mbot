import utils
import json
import logging

logger = logging.getLogger(__name__)


class BaseTelegramModule(object):
    """Base class which represents module

    Attributes:
        _telegram_api(:class:`api.TelegramAPI`): Telegram API object which is used in module
        _tr(:class:`api.LangAPI`): LangAPI object which is used in module
        friendly_name(str): friendly name that will be shown in list
        disabled(bool): when this evaluates to ``True``, module is considered disabled

    Args:
        telegram_api(:class:`api.TelegramAPI`): Telegram API object to use in module
        lang(:class:`api.LangAPI`): LangAPI object to use in module

    """
    disabled = False

    @utils.log(logger, print_ret=False)
    def __init__(self, telegram_api, lang):
        if self.disabled:
            raise InterruptedError('Module is disabled')
        self._telegram_api = telegram_api
        self._tr = lang
        self.friendly_name = None

    def help(self, message, args, lang):
        """Answers to `/help` message

        Args:
            message(:class:`telegram.Message`): received message
            args(list): message arguments
            lang(str|NoneType): user language (``None`` if cannot be determined)

        """
        raise NotImplementedError('This method must be implemented')


class JSONAPI(object):
    """This class represents base for APIs that work with JSON files

    Attributes:
        raw_data: read-only raw data from file

    Args:
        directory(str): directory to use for finding a file
        name(str): name of file without ``.json` extension

    Raises:
        FileNotFoundError: when specified file cannot be found

    """
    @utils.log(logger, print_ret=False)
    def __init__(self, directory, name):
        with open('./{0}/{1}.json'.format(directory, name), 'r') as f:
            self._raw_data = json.load(f)

    @utils.log(logger)
    def __getitem__(self, item):
        return self._raw_data.get(item.lower(), None)

    @utils.log(logger)
    def __getattr__(self, item):
        return self.__getitem__(item)

    @property
    def raw_data(self):
        return self._raw_data
