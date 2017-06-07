from bases import BaseTelegramModule


class TelegramModule(BaseTelegramModule):
    def __init__(self, telegram_api):
        super(TelegramModule, self).__init__(telegram_api)
        self.commands = ((['kick'], self.kick), (['ban'], self.ban), (['unban'], self.unban))
        self.friendly_name = 'AdminModule'
        self._register_module()

    def help(self, message, args):
        self._telegram_api.send_text_message(message.chat_id,
                                             "This module helps to administrate groups\n"
                                             "Available commands:\n/kick - kicks user from chat\n"
                                             "/ban - bans user from chat\n/unban - unbans user",
                                             reply_to=message.message_id)

    def is_admin(self, chat_id, user_id):
        return not self._telegram_api.is_private_chat(chat_id) and \
               user_id in self._telegram_api.get_admins(chat_id, use_ids=True)

    def main(self, message, fn):
        if not self.is_admin(message.chat_id, message.from_user.id):
            self._telegram_api.send_text_message(message.chat_id, "You have no power!",
                                                 reply_to=message.message_id)
            return

        user_id = message.reply_to_message.from_user.id
        return fn(message.chat_id, user_id)

    def kick(self, message, args):
        if self.main(message, self._telegram_api.kick_member):
            self._telegram_api.send_text_message(message.chat_id,
                                                 "{0} kicked {1}".format(
                                                     message.from_user.name,
                                                     message.reply_to_message.from_user.name
                                                 ), reply_to=message.message_id)

    def ban(self, message, args):
        if self.main(message, self._telegram_api.ban_member):
            self._telegram_api.send_text_message(message.chat_id,
                                                 "{0} banned {1}".format(
                                                     message.from_user.name,
                                                     message.reply_to_message.from_user.name
                                                 ), reply_to=message.message_id)

    def unban(self, message, args):
        if self.main(message, self._telegram_api.unban_member):
            self._telegram_api.send_text_message(message.chat_id,
                                                 "{0} unbanned {1}".format(
                                                     message.from_user.name,
                                                     message.reply_to_message.from_user.name
                                                 ), reply_to=message.message_id)
