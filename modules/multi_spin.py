# Kostilniy modul
from bases import BaseTelegramModule
from main import dp
from telegram import (Bot, Update)


class TelegramModule(BaseTelegramModule):
    def __init__(self, api):
        super(TelegramModule, self).__init__(api)
        self.friendly_name = "Multi Spin"
        self._telegram_api.register_command(['spin'], self.spin)
        dp.add_handler(MessageHandler(Filters.all, self.update_cache, edited_updates=True), group=-1)
        

    def do_the_spin(bot: Bot, update: Update):
        chat_id = update.message.chat_id
        s = escape_markdown(core.spin_name.get(chat_id, config.DEFAULT_SPIN_NAME))
        p = core.results_today.get(chat_id)
        if chat_id in locks:
            return
        if p is not None:
            bot.send_message(chat_id=chat_id, text=config.TEXT_ALREADY.format(s=s, n=p),
                             parse_mode=ParseMode.MARKDOWN)
        else:
            p = escape_markdown(core.choose_random_user(chat_id, bot))
            from time import sleep
            curr_text = choice(config.TEXTS)
            locks.append(chat_id)
            for t in curr_text:
                bot.send_message(chat_id=chat_id, text=t.format(s=s, n=p),
                                 parse_mode=ParseMode.MARKDOWN)
                sleep(2)
        locks.pop(locks.index(chat_id))


    def update_cache(bot: Bot, update: Update):
        user = update.effective_user
        chat_id = update.effective_message.chat_id
        # Also skip first update when the bot is added
        if not core.is_private(chat_id) and core.chat_users.get(chat_id) is not None:
            core.chat_users[chat_id].update({user.id: user.name})

