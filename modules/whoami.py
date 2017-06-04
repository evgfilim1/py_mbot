from bases import BaseTelegramModule


class TelegramModule(BaseTelegramModule):
    # TODO: Docs
    def __init__(self, telegram_api):
        super(TelegramModule, self).__init__(telegram_api)
        self._telegram_api.register_command(['whoami', 'whois', 'who'], self.who)

    def help(self, message, args):
        self._telegram_api.send_text_message(message.chat_id,
                                             "This module replies to /whoami with user info\n\n"
                                             "Aliases: /who, /whois")

    def who(self, message, args):
        self._telegram_api.send_text_message(message.chat_id, f"You are {message.from_user.name}\n"
                                                              f"Your ID: {message.from_user.id}\n")
