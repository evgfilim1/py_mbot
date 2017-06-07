from bases import BaseTelegramModule


class TelegramModule(BaseTelegramModule):
    def __init__(self, telegram_api):
        super(TelegramModule, self).__init__(telegram_api)
        self.text_handler = (self.echo, )
        self.disabled = True
        self._register_module()

    def help(self, message, args):
        self._telegram_api.send_text_message(message.chat_id,
                                             'This module simply echoes every text message',
                                             reply_to=message.message_id)

    def echo(self, message):
        self._telegram_api.send_text_message(message.chat_id, message.text)
