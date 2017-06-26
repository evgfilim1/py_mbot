from bases import BaseTelegramModule
import api


class TelegramModule(BaseTelegramModule):
    def __init__(self, *args):
        super(TelegramModule, self).__init__(*args)
        self._telegram_api.register_command(['warn'], self.warn)
        self._telegram_api.register_command(['unwarn'], self.unwarn)
        self._telegram_api.register_command(['max_warns'], self.set_max_warns)
        self._data = api.StorageAPI('warns')
        if self._data.warns is None:
            self._data.warns = {}

        if self._data.max_warns is None:
            self._data.max_warns = 3

    def is_admin(self, chat_id, user_id):
        return not self._telegram_api.is_private_chat(chat_id) and \
               user_id in self._telegram_api.get_admins(chat_id, use_ids=True)

    def set_max_warns(self, message, args, lang):
        if not self.is_admin(message.chat_id, message.from_user.id):
            return
        try:
            if int(args[0]) <= 0:
                raise Exception
            self._data.max_warns = int(args[0])
            self._data.save()
            self._telegram_api.send_text_message(message.chat_id, self._tr(lang, 'max_warns'),
                                                 reply_to=message.message_id)
        except Exception:
            self._telegram_api.send_text_message(message.chat_id,
                                                 self._tr(lang, 'help.max_warns'),
                                                 markdown=True)
    def warn(self, message, args, lang):
        if not self.is_admin(message.chat_id, message.from_user.id):
            self._telegram_api.send_text_message(message.chat_id, self._tr(lang, 'not_admin'),
                                                 reply_to=message.message_id)
            return

        if self._data.warns.get(message.chat_id) is None:
            self._data.warns[message.chat_id] = {}

        if self._telegram_api.bot_id == message.reply_to_message.from_user.id:
            self._telegram_api.send_text_message(message.chat_id, self._tr(lang, 'reply_to_bot'),
                                                 reply_to=message.message_id)
            return

        self._data.warns[message.chat_id][message.reply_to_message.from_user.id] =\
            self._data.warns[message.chat_id].get(message.reply_to_message.from_user.id, 0) + 1

        text_message = \
            str(self._data.warns[message.chat_id][message.reply_to_message.from_user.id]) +\
            "/" + str(self._data.max_warns)

        self._telegram_api.send_text_message(message.chat_id, text_message,
                                             reply_to=message.message_id)

        if self._data.warns[message.chat_id][message.from_user.id] >= self._data.max_warns:
            self._data.warns[message.chat_id][message.from_user.id] = 0
            self.kick(message, lang)

        self._data.save()  # TODO: DECORATORs

    def unwarn(self, message, args, lang):
        if not self.is_admin(message.chat_id, message.from_user.id):
            return

        if self._data.warns[message.chat_id][message.reply_to_message.from_user.id] == 0:
            self._telegram_api.send_text_message(message.chat_id, self._tr(lang, 'good'),
                                                 reply_to=message.message_id)
            return

        if self._data.warns.get(message.chat_id) is None:
            self._data.warns[message.chat_id] = {}

        self._data.warns[message.chat_id][message.reply_to_message.from_user.id] =\
            self._data.warns[message.chat_id].get(message.reply_to_message.from_user.id, 0) - 1

        text_message =\
            str(self._data.warns[message.chat_id][message.reply_to_message.from_user.id]) +\
            "/" + str(self._data.max_warns)
        self._telegram_api.send_text_message(message.chat_id, text_message,
                                             reply_to=message.message_id)

        self._data.save()  # TODO: DECORATORs

    def kick(self, message, lang):
        self._telegram_api.send_text_message(message.chat_id, self._tr(lang, 'last_warn'),
                                             reply_to=message.message_id)
        self._telegram_api.kick_member(message.chat_id, message.reply_to_message.from_user.id)
        self._telegram_api.send_text_message(message.chat_id,
                                             self._tr(lang, 'kicked').format(
                                                message.from_user.name,
                                                message.reply_to_message.from_user.name
                                             ), reply_to=message.message_id)
