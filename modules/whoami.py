from bases import BaseTelegramModule


class TelegramModule(BaseTelegramModule):
    # TODO: Docs
    def __init__(self, *args):
        super(TelegramModule, self).__init__(*args)
        self._telegram_api.register_command(['whoami', 'whois', 'who'], self.who)

    def who(self, message, args, lang):
        text = self._tr(lang, 'info_common').format(message.from_user.name, message.from_user.id)
        if message.reply_to_message:
            text += self._tr(lang, 'info_reply').format(
                message.reply_to_message.from_user.name,
                message.reply_to_message.from_user.id
            )
            if message.reply_to_message.forward_from:
                text += self._tr(lang, 'info_forward').format(
                    message.reply_to_message.forward_from.name,
                    message.reply_to_message.forward_from.id
                )
        self._telegram_api.send_text_message(message.chat_id, text, reply_to=message.message_id)
