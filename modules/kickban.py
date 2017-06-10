from bases import BaseTelegramModule

# TODO: refactor


class TelegramModule(BaseTelegramModule):
    def __init__(self, *args):
        super(TelegramModule, self).__init__(*args)
        self._telegram_api.register_command(['kick'], self.kick)
        self._telegram_api.register_command(['ban'], self.ban)
        self._telegram_api.register_command(['unban'], self.unban)
        self.friendly_name = 'AdminModule'

    def help(self, message, args, lang):
        self._telegram_api.send_text_message(message.chat_id,
                                             self._tr(lang, 'help'),
                                             reply_to=message.message_id)

    def is_admin(self, chat_id, user_id):
        return not self._telegram_api.is_private_chat(chat_id) and \
               user_id in self._telegram_api.get_admins(chat_id, use_ids=True)

    def main(self, message, lang, fn):
        if not self.is_admin(message.chat_id, message.from_user.id):
            self._telegram_api.send_text_message(message.chat_id, self._tr(lang, 'not_admin'),
                                                 reply_to=message.message_id)
            return

        user_id = message.reply_to_message.from_user.id
        return fn(message.chat_id, user_id)

    def kick(self, message, args, lang):
        if self.main(message, lang, self._telegram_api.kick_member):
            self._telegram_api.send_text_message(message.chat_id,
                                                 self._tr(lang, 'kicked').format(
                                                     message.from_user.name,
                                                     message.reply_to_message.from_user.name
                                                 ), reply_to=message.message_id)

    def ban(self, message, args, lang):
        if self.main(message, lang, self._telegram_api.ban_member):
            self._telegram_api.send_text_message(message.chat_id,
                                                 self._tr(lang, 'banned').format(
                                                     message.from_user.name,
                                                     message.reply_to_message.from_user.name
                                                 ), reply_to=message.message_id)

    def unban(self, message, args, lang):
        if self.main(message, lang, self._telegram_api.unban_member):
            self._telegram_api.send_text_message(message.chat_id,
                                                 self._tr(lang, 'unbanned').format(
                                                     message.from_user.name,
                                                     message.reply_to_message.from_user.name
                                                 ), reply_to=message.message_id)
