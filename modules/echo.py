from bases import BaseTelegramModule


class TelegramModule(BaseTelegramModule):
    disabled = True

    def __init__(self, *args):
        super(TelegramModule, self).__init__(*args)
        self._telegram_api.register_text_handler(self.echo)

    def help(self, message, args, lang):
        self._telegram_api.send_text_message(message.chat_id,
                                             self._tr(lang, 'help'),
                                             reply_to=message.message_id)

    def echo(self, message):
        self._telegram_api.send_text_message(message.chat_id, message.text)
