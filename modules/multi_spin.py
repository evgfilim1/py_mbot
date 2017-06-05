# Kostilniy modul
from bases import BaseTelegramModule
from main import dp
from telegram import (Bot, Update)


class TelegramModule(BaseTelegramModule):
    def _load(filename: str):
        with open(filename, 'rb') as ff:
            return pickle.load(ff)


    def _save(obj: dict, filename: str):
        with open(filename, 'wb') as ff:
            pickle.dump(obj, ff, pickle.HIGHEST_PROTOCOL)
    

    def __init__(self, api):
        super(TelegramModule, self).__init__(api)
        self.friendly_name = "Multi Spin"
        self._telegram_api.register_command(['spin'], self.spin)
        self._telegram_api.register_command(['spin_setname'], self.spin_setname)
        dp.add_handler(MessageHandler(Filters.all, self.update_cache, edited_updates=True), group=-1)
        self.spin_name = self._load("spins.pkl")
        self.results_today = {}
        

    def spin_setname(self, message, args):
        #pass
        try:
            spin_num = int(args.split()[0])
        except Exception:
            self._telegram_api.send_text_message(chat_id, "Usage `/spin_setname <num> <name>`", markdown=True)
            return
        try:
            self.spin_name[chat_id][spin_num].update(args[len(args.split()[0])+1:])
        except Exception:
            self.spin_name[chat_id]={}
            self.spin_name[chat_id][spin_num].update(args[len(args.split()[0])+1:])
        self._telegram_api.send_text_message(chat_id, "*Done*", markdown=True)


    def spin(self, message, args):
        chat_id = message.chat_id
        try:
            spin_num = int(args[0])
        except Exception:
            self._telegram_api.send_text_message(chat_id, "Gimme int dumbass")
            return
        s = escape_markdown(self.spin_name[chat_id].get(spin_num))
        try:
            p = self.results_today[chat_id].get(spin_num)
        except Exception:
            p = None
            self.results_today[chat_id] = {}
        if chat_id in locks:
            return
        if p is not None:
            self._telegram_api.send_text_message(chat_id, self.TEXT_ALREADY.format(s=s, n=p),
                             markdown=True)
        else:
            p = escape_markdown(self.choose_random_user(chat_id))
            from time import sleep
            curr_text = choice(self.TEXTS)
            locks.append(chat_id)
            for t in curr_text:
                self._telegram_api.send_message(chat_id, self.t.format(s=s, n=p),
                                 mardown=True)
                sleep(2)
        locks.pop(locks.index(chat_id))


    def update_cache(bot: Bot, update: Update):
        user = update.effective_user
        chat_id = update.effective_message.chat_id
        # Also skip first update when the bot is added
        if not core.is_private(chat_id) and core.chat_users.get(chat_id) is not None:
            core.chat_users[chat_id].update({user.id: user.name})

