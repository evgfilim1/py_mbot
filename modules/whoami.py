from bases import BaseTelegramModule


class TelegramModule(BaseTelegramModule):
    # TODO: Docs
    def __init__(self, telegram_api):
        super(TelegramModule, self).__init__(telegram_api)
        self.commands = ((['whoami', 'whois', 'who'], self.who), )
        self._register_module()

    def help(self, message, args):
        self._telegram_api.send_text_message(message.chat_id,
                                             "This module replies to /whoami with user info\n\n"
                                             "Aliases: /who, /whois")

    def who(self, message, args):
        self._telegram_api.send_text_message(message.chat_id,
                                             "You are {0}\nYour ID: {1}\n".format(
                                                 message.from_user.name, message.from_user.id
                                             ))
