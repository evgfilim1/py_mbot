from bases import BaseTelegramModule


class TelegramModule(BaseTelegramModule):
    def __init__(self, *args):
        super(TelegramModule, self).__init__(*args)
        self._telegram_api.register_command(['me'], self.me)

    def help(self, message, args, lang):
        self._telegram_api.send_text_message(message.chat_id, self._tr(lang, 'help'),
                                             reply_to=message.message_id)

    def me(self, message, args, lang):
        self._telegram_api.send_text_message(message.chat_id,
                                             '{0} {1}'.format(message.from_user.name,
                                                              ' '.join(args)))
