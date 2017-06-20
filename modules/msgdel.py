from bases import BaseTelegramModule


class TelegramModule(BaseTelegramModule):
    def __init__(self, *args):
        super(TelegramModule, self).__init__(*args)
        self._telegram_api.register_command(['delete'], self.delete)
        self.friendly_name = 'DeleteMessageModule'

    def delete(self, message, args, lang):
        if message.reply_to_message.from_user.id == self._telegram_api.bot_id:
            self._telegram_api.delete_message(message=message.reply_to_message)
