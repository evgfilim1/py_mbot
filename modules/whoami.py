from bases import BaseTelegramModule


class TelegramModule(BaseTelegramModule):
    # TODO: Docs
    def __init__(self, telegram_api):
        super(TelegramModule, self).__init__(telegram_api)
        self.commands = ((['whoami', 'whois', 'who'], self.who), )
        self._register_module()

    def help(self, message, args):
        self._telegram_api.send_text_message(message.chat_id,
                                             'This module replies to /whoami with user info\n\n'
                                             'Aliases: /who, /whois', reply_to=message.message_id)

    def who(self, message, args):
        text = 'You are {0}\nYour ID: {1}\n'.format(message.from_user.name, message.from_user.id)
        if message.reply_to_message:
            text += 'Replied to {0}\nReplied to ID: {1}\n'.format(
                message.reply_to_message.from_user.name,
                message.reply_to_message.from_user.id
            )
            if message.reply_to_message.forward_from:
                text += 'Forwarded from {0}\nForwarded from ID: {1}'.format(
                    message.reply_to_message.forward_from.name,
                    message.reply_to_message.forward_from.id
                )
        self._telegram_api.send_text_message(message.chat_id, text, reply_to=message.message_id)
