import json


class BaseTelegramModule(object):
    """Base class which represents module

    Attributes:
        _telegram_api(:class:`api.TelegramAPI`): Telegram API object which is used in module
        friendly_name(str): friendly name that will be shown in list
        disabled(bool): when this evaluates to ``True``, module is considered disabled
        commands(list|tuple): list of lists of commands and associated callback
        text_handler(function): callback to handle text messages

    Args:
        telegram_api(:class:`api.TelegramAPI`): Telegram API object to use in module

    """

    def __init__(self, telegram_api):
        self._telegram_api = telegram_api
        self.friendly_name = None
        self.disabled = False
        self.commands = None
        self.text_handler = None

    def help(self, message, args):
        """Answers to `/help` message

        Args:
            message(:class:`telegram.Message`): received message
            args(list): message arguments

        """
        raise NotImplementedError('This method must be implemented')

    def _register_module(self):
        """Initializes and registers module handlers

        Raises:
            ValueError: if one of commands was already registered

        """
        if not self.disabled:
            if self.commands is not None:
                for commands in self.commands:
                    self._telegram_api.register_command(commands[0], commands[1])
            if self.text_handler is not None:
                self._telegram_api.register_text_handler(self.text_handler)


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
    def __init__(self, directory, name):
        with open('./{0}/{1}.json'.format(directory, name), 'r') as f:
            self._raw_data = json.load(f)

    def __getitem__(self, item):
        return self._raw_data.get(item.lower(), None)

    @property
    def raw_data(self):
        return self._raw_data
