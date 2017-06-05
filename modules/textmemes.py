from bases import BaseTelegramModule


class TelegramModule(BaseTelegramModule):
    def __init__(self, telegram_api):
        super(TelegramModule, self).__init__(telegram_api)
        self.commands = ((['lenny'], self.lenny), (['shrug'], self.shrug))
        self._register_module()

    def help(self, message, args):
        self._telegram_api.send_text_message(message.chat_id, "This module sends /shrug or /lenny")

    def lenny(self, message, args):
        self._telegram_api.send_text_message(message.chat_id, "( ͡° ͜ʖ ͡° )")

    def shrug(self, message, args):
        self._telegram_api.send_text_message(message.chat_id, "¯\_(ツ)_/¯")
