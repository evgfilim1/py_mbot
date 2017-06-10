from bases import BaseTelegramModule


class TelegramModule(BaseTelegramModule):
    def __init__(self, *args):
        super(TelegramModule, self).__init__(*args)
        self._telegram_api.register_command(['delete'], self.delete)
        self.friendly_name = 'DeleteMessageModule'

    def help(self, message, args, lang):
        self._telegram_api.send_text_message(message.chat_id, self._tr(lang, 'help'),
                                             reply_to=message.message_id)

    def delete(self, message, args, lang):
        if message.reply_to_message.from_user.id == self._telegram_api.bot_id:
            self._telegram_api.delete_message(message=message.reply_to_message)
