from bases import BaseTelegramModule


class TelegramModule(BaseTelegramModule):
    """Example class which represents module"""
    def __init__(self, *args):
        super(TelegramModule, self).__init__(*args)
        self._telegram_api.register_command(['ping'], self.ping)
        self.friendly_name = 'PingModule'

    def ping(self, message, args, lang):
        """Answers to `/ping` message

        Args:
            message(:class:`telegram.Message`): received message
            args(list): message arguments
            lang(str|NoneType): user language

        """
        self._telegram_api.send_text_message(message.chat_id, self._tr(lang, 'pong'),
                                             reply_to=message.message_id)
