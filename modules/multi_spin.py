# Kostilniy modul
from bases import BaseTelegramModule
from main import dp
from telegram import (Bot, Update)
from telegram.ext import (Filters, MessageHandler)
from telegram.utils.helpers import escape_markdown
import pickle
from random import choice

class TelegramModule(BaseTelegramModule):
    def _load(self, filename: str):
        with open(filename, 'rb') as ff:
            return pickle.load(ff)


    def _save(self, obj: dict, filename: str):
        with open(filename, 'wb') as ff:
            pickle.dump(obj, ff, pickle.HIGHEST_PROTOCOL)


    def __init__(self, api):
        super(TelegramModule, self).__init__(api)
        self.friendly_name = "Multi Spin"
        self._telegram_api.register_command(['spin'], self.spin)
        self._telegram_api.register_command(['spin_setname'], self.spin_setname)
        dp.add_handler(MessageHandler(Filters.all, self.update_cache, edited_updates=True),
                       group=-1)
        self.spin_name = self._load("spins.pkl")
        self.results_today = {}
        self.chat_users = self._load("chat.pkl")
        self.locks = []
 

    def spin_setname(self, message, args):
        #pass
        chat_id = message.chat_id
        try:
            spin_num = int(args.split()[0])
        except Exception:
            self._telegram_api.send_text_message(chat_id,
                                                 "Usage `/spin_setname <num> <name>`",
                                                 markdown=True)
            return
        try:
            self.spin_name[chat_id][spin_num].update(args[len(args.split()[0])+1:])
        except Exception:
            self.spin_name[chat_id] = {}
            self.spin_name[chat_id][spin_num].update(args[len(args.split()[0])+1:])
        self._telegram_api.send_text_message(message.chat_id, "*Done*", markdown=True)


    def spin(self, message, args):
        chat_id = message.chat_id
        try:
            spin_num = int(args[0])
        except Exception:
            #self._telegram_api.send_text_message(chat_id, "Gimme int dumbass")
            choice(self.spin_name.get(chat_id, {"79|0ub0d0u9|"}))
            return
        s = escape_markdown(self.spin_name[chat_id].get(spin_num))
        try:
            p = self.results_today[chat_id].get(spin_num)
        except Exception:
            p = None
            self.results_today[chat_id] = {}
        if chat_id in self.locks:
            return
        if p is not None:
            self._telegram_api.send_text_message(chat_id, self.TEXT_ALREADY.format(s=s, n=p),
                                                 markdown=True)
        else:
            p = escape_markdown(self.choose_random_user(chat_id))
            from time import sleep
            curr_text = choice(self.TEXTS)
            self.locks.append(chat_id)
            for t in curr_text:
                self._telegram_api.send_message(chat_id, self.t.format(s=s, n=p),
                                                mardown=True)
                sleep(2)
        self.locks.pop(locks.index(chat_id))


    def update_cache(self, bot: Bot, update: Update):
        user = update.effective_user
        chat_id = update.effective_message.chat_id
        # Also skip first update when the bot is added
        if not _is_private(chat_id) and self.chat_users.get(chat_id) is not None:
            self.chat_users[chat_id].update({user.id: user.name})

