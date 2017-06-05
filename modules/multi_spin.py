# Kostilniy modul
from bases import BaseTelegramModule
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


    def _is_private(self, chat_id):
        return chat_id > 0


    def __init__(self, api):
        super(TelegramModule, self).__init__(api)
        self.friendly_name = "Multi Spin"
        self._telegram_api._dispatcher.add_handler(MessageHandler(Filters.all, self.update_cache, edited_updates=True),
                       group=-1)
        self._telegram_api.register_command(['spin'], self.spin)
        self._telegram_api.register_command(['spin_setname'], self.spin_setname)
        self.spin_name = self._load("spins.pkl")
        self.results_today = {}
        self.chat_users = self._load("chat.pkl")
        self.locks = []
        self.TEXTS = [["Итак, кто же сегодня *{s} дня*?", "_Хмм, интересно..._", "*АГА!*",
         "Сегодня ты *{s} дня,* {n}"],
         ["*Колесо Сансары запущено!*", "_Что за дичь?!_", "Ну ок...",
          "Поздравляю, ты *{s} дня,* {n}"],
         ["Кручу-верчу, *наебать* хочу", "Сегодня ты *{s} дня*, @spin\_everyday\_bot",
          "_(нет)_", "На самом деле, это {n}"],
         ["Эмм... Ты уверен?", "Ты *точно* уверен?", "Хотя ладно, процесс уже необратим",
          "Сегодня я назначаю тебе должность *{s} дня*, {n}!"],
         ["_Ищем рандомного кота на улице..._", "_Ищем палку..._", "_Ищем шапку..._", "_Рисуем ASCII-арт..._",
          "*Готово!*", """```
.∧＿∧
( ･ω･｡)つ━☆・*。
⊂　 ノ 　　　・゜+.
しーＪ　　　°。+ *´¨)
　　　　　　　　　.· ´¸.·*´¨) ¸.·*¨)
　　　　　　　　　　(¸.·´ (¸.·'* ☆ ВЖУХ, И ТЫ {s} ДНЯ,```{n}
"""]]
 

    def spin_setname(self, message, args):
        #pass
        chat_id = message.chat_id
        #print(args)
        try:
            spin_num = int(args[0])
        except Exception:
            self._telegram_api.send_text_message(chat_id,
                                                 "Usage `/spin_setname <num> <name>`",
                                                 markdown=True)
            return
        try:
            self.spin_name[chat_id][spin_num].update(args[1])
        except Exception:
            self.spin_name[chat_id] = {}
            self.spin_name[chat_id].update({spin_num: args[1]})
        self._telegram_api.send_text_message(message.chat_id, "*Done*", markdown=True)


    def spin(self, message, args):
        chat_id = message.chat_id
        try:
            spin_num = int(args[0])
        except Exception:
            #self._telegram_api.send_text_message(chat_id, "Gimme int dumbass")
            spin_num = choice(list(self.spin_name.get(chat_id, [0])))
        #print(self.spin_name[chat_id].get(spin_num, "79|0ub0d0u9|"))
        s = escape_markdown(self.spin_name[chat_id].get(spin_num, "79|0ub0d0u9|"))
        try:
            p = self.results_today[chat_id].get(spin_num)
        except Exception:
            p = ""
            p = None
            self.results_today[chat_id] = {}
        if chat_id in self.locks:
            return
        if p is not None:
            self._telegram_api.send_text_message(chat_id, self.TEXT_ALREADY.format(s=s, n=p),
                                                 markdown=True)
        else:
            p = escape_markdown(self.choose_random_user(chat_id, spin_num))
            from time import sleep
            curr_text = choice(self.TEXTS)
            self.locks.append(chat_id)
            for t in curr_text:
                self._telegram_api.send_text_message(chat_id, t.format(s=s, n=p),
                                                mardown=True)
                sleep(2)
        self.locks.pop(self.locks.index(chat_id))


    def update_cache(self, bot: Bot, update: Update):
        #print("IM WORKING")
        user = update.effective_user
        chat_id = update.effective_message.chat_id
        # Also skip first update when the bot is added
        if not self._is_private(chat_id):
            try:
                self.chat_users[chat_id].update({user.id: user.name})
            except KeyError:
                self.chat_users[chat_id]={}
                self.chat_users[chat_id].update({user.id: user.name})


    def choose_random_user(self, chat_id, spin_num):
        #print(self.chat_users[chat_id])
        i = choice(list(self.chat_users[chat_id]))
        self.results_today[chat_id][spin_num] = self.chat_users[chat_id][i]
        return self.chat_users[chat_id][i]
