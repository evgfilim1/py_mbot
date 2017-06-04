from bases import BaseTelegramModule


class TelegramModule(BaseTelegramModule):
    def __init__(self, telegram_api):
        super(TelegramModule, self).__init__(telegram_api)
        self._telegram_api.register_command(['kick'], self.kick)
        # self._telegram_api.register_command(['ban'], self.ban)
        self.friendly_name = 'AdminModule'

    def help(self, message, args):
        self._telegram_api.send_text_message(message.chat_id,
                                             "This module helps to administrate groups\n"
                                             "Available commands:\n/kick - kicks user from chat\n"
                                             "/ban - bans user from chat\n/unban - unbans user")

    def is_admin(self, chat_id, user_id):
        return user_id in self._telegram_api.get_admins(chat_id, use_ids=True)

    def kick(self, message, args):
        if not self.is_admin(message.chat_id, message.from_user.id):
            self._telegram_api.send_text_message(message.chat_id, "You have no power!",
                                                 reply_to=message.message_id)
            return

        if args:
            try:
                user_id = int(args[0])
            except ValueError:
                user_id = message.reply_to_message.from_user.id
            self._telegram_api.kick_member(message.chat_id, user_id)
