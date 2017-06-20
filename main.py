import logging
from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from api import ConfigAPI, LangAPI, StorageAPI
import modloader
import utils
import time

logging.basicConfig(level=logging.DEBUG,
                    format='[{levelname:<9}] ({asctime}) {name}: {message}',
                    style='{', filename='bot.log')

logger = logging.getLogger(__name__)
logger.debug('Starting py_mbot...')

data = StorageAPI('main')
config = ConfigAPI('main')
tr = LangAPI('main')

updater = Updater(config.token)
dp = updater.dispatcher

start_time = time.time()


@utils.log(logger, print_ret=False)
def start(bot, update):
    lang = utils.get_lang(data, update.effective_user)
    update.effective_message.reply_text(tr(lang, 'start'))


@utils.log(logger, print_ret=False)
def help_command(bot, update, args):
    lang = utils.get_lang(data, update.effective_user)
    if len(args) == 0:
        update.effective_message.reply_text(tr(lang, 'help'))
    else:
        module_name = " ".join(args)
        if module_name in modloader.DISABLED or module_name in modloader.FAILURE:
            update.effective_message.reply_text('Module is disabled')
        elif module_name in modloader.ENABLED:
            modloader.ENABLED.get(module_name).help(update.effective_message, [], lang)
        else:
            update.effective_message.reply_text('Module not found')


@utils.log(logger, print_ret=False)
def about(bot, update):
    lang = utils.get_lang(data, update.effective_user)
    update.effective_message.reply_text(tr(lang, 'about').format(config.version))


@utils.log(logger, print_ret=False)
def module_list(bot, update):
    lang = utils.get_lang(data, update.effective_user)
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


@utils.log(logger, print_ret=False)
def settings(bot, update):
    keyboard = []
    for i, (lang, flag) in enumerate(config.flags.items()):
        text = '{0} {1}'.format(flag, lang)
        callback_data = 'settings:lang:{0}'.format(lang)
        if i % 2 == 0:
            keyboard.append([InlineKeyboardButton(text, callback_data=callback_data)])
        else:
            keyboard[-1].append(InlineKeyboardButton(text, callback_data=callback_data))
    update.message.reply_text('Choose your language',
                              reply_markup=InlineKeyboardMarkup(keyboard))


@utils.log(logger, print_ret=False)
def language(bot, update):
    lang = update.callback_query.data.split(':')[2]
    if not data.languages:
        data.languages = {}
    data.languages.update({update.effective_user.id: lang})
    data.save()
    update.callback_query.answer('Now your language is {0}'.format(lang))


@utils.log(logger, print_ret=False)
def main():
    modloader.load_modules(updater, data)

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help_command, pass_args=True))
    dp.add_handler(CommandHandler('about', about))
    dp.add_handler(CommandHandler('modules', module_list))
    dp.add_handler(CommandHandler('settings', settings))
    dp.add_handler(CallbackQueryHandler(language, pattern=r'^settings:lang:\w+$'))

    dp.add_error_handler(lambda bot, update, error: logger.exception('Exception was raised',
                                                                     exc_info=error))

    updater.start_polling(clean=True)

    logger.info('Bot started in {0:.3} seconds'.format(time.time() - start_time))

    updater.idle()

    data.save()

if __name__ == '__main__':
    main()
