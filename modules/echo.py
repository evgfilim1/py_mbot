from bases import BaseTelegramModule


class TelegramModule(BaseTelegramModule):
    disabled = True

    def __init__(self, telegram_api):
        super(TelegramModule, self).__init__(telegram_api)
        self._telegram_api.register_text_handler(self.echo)

    def help(self, message, args):
        self._telegram_api.send_text_message(message.chat_id,
                                             'This module simply echoes every text message',
                                             reply_to=message.message_id)

    def echo(self, message):
        self._telegram_api.send_text_message(message.chat_id, message.text)
