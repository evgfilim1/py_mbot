from bases import BaseTelegramModule
import pickle
import api
from threading import Timer


class TelegramModule(BaseTelegramModule):

    def _load(self, filename: str):
        try:
            with open(filename, 'rb') as ff:
                return pickle.load(ff)
        except Exception:
            return {}

    def _save(self, obj: dict, filename: str):
        with open(filename, 'wb') as ff:
            pickle.dump(obj, ff, pickle.HIGHEST_PROTOCOL)

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

    def __init__(self,  *args):
        super(TelegramModule, self).__init__(*args)
        self._telegram_api.register_command(['help'], self.help)
        self._telegram_api.register_command(['warn'], self.warn)
        self._telegram_api.register_command(['unwarn'], self.unwarn)
        self._telegram_api.register_command(['max_warns'], self.max_warns)
        self._data = api.StorageAPI('warns')
        if self._data.warns is None:
            self._data.warns = {}
        self.max_warns = 3

    def help(self, message, args, lang):
        self._telegram_api.send_text_message(message.chat_id, self._tr(lang, 'help'))

    def max_warns(self, message, args, lang):
        chat_id = message.chat_id
        try:
            self.max_warns = int(args[0])
            self._telegram_api.send_text_message(message.chat_id, self._tr(lang, 'max_warns'),
                                                 reply_to=message.message_id)
        except Exception:
            self._telegram_api.send_text_message(chat_id,
                                                 self._tr(lang, 'help.max_warns'),
                                                 markdown=True)

    def warn(self, message, args, lang):
        if self._data.warns.get(message.chat_id) is None:
            self._data.warns[message.chat_id] = {}

        if message.reply_to_message.from_user.id == self._telegram_api.bot_id:
            self._telegram_api.send_text_message(message.chat_id, self._tr(lang, 'reply_to_bot'),
                                                 reply_to=message.message_id)
            return 0

        self._data.warns[message.chat_id][message.from_user.id] = self._data.warns[message.chat_id].get(
            message.from_user.id, 0) + 1
        self._data.save()

        text_message = str(self._data.warns[message.chat_id][message.from_user.id]) + "/" + str(self.max_warns)
        self._telegram_api.send_text_message(message.chat_id, text_message,
                                             reply_to=message.message_id)

        if self._data.warns[message.chat_id][message.from_user.id] >= self.max_warns:
            self._telegram_api.send_text_message(message.chat_id, self._tr(lang, 'last_warn'),
                                                 reply_to=message.message_id)
            if self.main(message, lang, self._telegram_api.kick_member):
                self._telegram_api.send_text_message(message.chat_id,
                                                     self._tr(lang, 'kicked').format(
                                                         message.from_user.name,
                                                         message.reply_to_message.from_user.name
                                                     ), reply_to=message.message_id)

        self._data.warns[message.chat_id][message.from_user.id] = 0

    def unwarn(self, message, args):
        if self._data.warns.get(message.chat_id) is None:
            self._data.warns[message.chat_id] = {}

        self._data.warns[message.chat_id][message.from_user.id] = self._data.warns[message.chat_id].get(
            message.from_user.id, 0) - 1
        self._data.save()

        text_message = str(self._data.warns[message.chat_id][message.from_user.id]) + "/" + str(self.max_warns)
        self._telegram_api.send_text_message(message.chat_id, text_message,
                                             reply_to=message.message_id)

    def save(self):
        self._save(self._data.warns, "warns.pkl")
        Timer(60.0, self.save).start()
