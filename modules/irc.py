from bases import BaseTelegramModule


class TelegramModule(BaseTelegramModule):
    def __init__(self, *args):
        super(TelegramModule, self).__init__(*args)
        self._telegram_api.register_command(['me'], self.me)

    def me(self, message, args, lang):
        self._telegram_api.send_text_message(message.chat_id,
                                             '{0} {1}'.format(message.from_user.name,
                                                              ' '.join(args)))
