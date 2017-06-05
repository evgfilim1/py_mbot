from bases import BaseTelegramModule


class TelegramModule(BaseTelegramModule):
    """Example class which represents module

    Args:
        telegram_api(:class:`api.TelegramAPI`): Telegram api object to use in module

    """
    def __init__(self, telegram_api):
        super(TelegramModule, self).__init__(telegram_api)
        self.commands = ((['ping'], self.ping), )
        self.friendly_name = 'PingModule'
        self._register_module()

    def help(self, message, args):
        """Answers to `/help` message

        Args:
            message(:class:`telegram.Message`): received message
            args(list): message arguments

        """
        self._telegram_api.send_text_message(message.chat_id,
                                             'This module just replies "Pong!" to /ping command',
                                             reply_to=message.message_id)

    def ping(self, message, args):
        """Answers to `/ping` message

        Args:
            message(:class:`telegram.Message`): received message
            args(list): message arguments

        """
        self._telegram_api.send_text_message(message.chat_id, 'Pong!', reply_to=message.message_id)
