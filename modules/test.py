# invalid module
from bases import BaseTelegramModule


class TelegramModule(BaseTelegramModule):
    def __init__(self, api):
        super(TelegramModule, self).__init__(api)
        self._telegram_api.register_command(['ping'], self.help)

    def help(self, message, args):
        self._telegram_api.send_text_message(message.chat_id, 'Test Fail!')
