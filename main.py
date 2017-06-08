import logging
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler
from api import ConfigAPI, LangAPI
import modloader
import time

logging.basicConfig(level=logging.INFO, format='%(name)s: %(levelname)s: %(message)s')

logger = logging.getLogger('main')
config = ConfigAPI('main')
tr = LangAPI('main')

updater = Updater(config['token'])
dp = updater.dispatcher

start_time = time.time()


def start(bot, update):
    lang = update.effective_user.language_code
    update.effective_message.reply_text(tr(lang, 'start'))


def help(bot, update, args):
    lang = update.effective_user.language_code
    if len(args) == 0:
        update.effective_message.reply_text(tr(lang, 'help'))
    else:
        module_name = " ".join(args)
        if module_name in modloader.DISABLED or module_name in modloader.FAILURE:
            update.effective_message.reply_text('Module is disabled')
        elif module_name in modloader.ENABLED:
            try:
                modloader.ENABLED.get(module_name).help(update.effective_message, [])
            except NotImplementedError:
                update.effective_message.reply_text('Module developer had not implemented `help()`',
                                                    parse_mode=ParseMode.MARKDOWN)
        else:
            update.effective_message.reply_text('Module not found')


def about(bot, update):
    lang = update.effective_user.language_code
    update.effective_message.reply_text(tr(lang, 'about').format(config['version']))


def module_list(bot, update):
    lang = update.effective_user.language_code
    modlist = ''
    for module_name in sorted(modloader.ENABLED):
        modlist += ' - {0}\n'.format(module_name)
    fail_modlist = ''
    for (module_name, e) in sorted(modloader.FAILURE.items()):
        fail_modlist += ' - {0}: {1}\n'.format(module_name, e)
    disabled_modlist = ''
    for module_name in sorted(modloader.DISABLED):
        disabled_modlist += ' - {0}\n'.format(module_name)
    update.effective_message.reply_text(tr(lang, 'modules').format(modlist, fail_modlist,
                                                                   disabled_modlist),
                                        parse_mode='HTML')


def main():
    modloader.load_modules(updater)

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help, pass_args=True))
    dp.add_handler(CommandHandler('about', about))
    dp.add_handler(CommandHandler('modules', module_list))
    dp.add_error_handler(lambda bot, update, error: print(error))

    updater.start_polling(clean=True)

    logger.info('Bot started in {0:.3} seconds'.format(time.time() - start_time))

    updater.idle()

if __name__ == '__main__':
    main()
