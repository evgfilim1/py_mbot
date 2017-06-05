from bases import JSONAPI
from telegram import ParseMode
from telegram.ext import CommandHandler


class TelegramAPI(object):
    """Class which represents Telegram API between module and wrapper

    Attributes:
        bot_id(int): bot ID

    Args:
        updater(:class:`telegram.ext.Updater`): updater instance

    """
    _commands = []

    def __init__(self, updater):
        self._bot = updater.bot
        self._dispatcher = updater.dispatcher

    def _register_command(self, command):
        if command in self._commands:
            raise ValueError('Command "{0}" is already registered'.format(command))
        self._commands.append(command)

    def register_command(self, commands, callback, allow_edited=False):
        """Registers commands handler

        Args:
            commands(list|tuple): list of commands to register
            callback(function): callable object to execute
            allow_edited(Optional[bool]): pass edited messages

        """
        for command in commands:
            self._register_command(command)

        def process_update(bot, update):
            callback(update.effective_message,
                     update.effective_message.text.split(' ')[1:])
        self._dispatcher.add_handler(CommandHandler(commands, process_update,
                                                    allow_edited=allow_edited))

    def send_text_message(self, chat, text, markdown=False, html=False, reply_to=None, **kwargs):
        """Sends message

        Notes:
            For now, this method supports only sending message with markdown or HTML parsing

        Args:
            chat(int|str): chat ID or '@channel_name'
            text(str): text to send
            markdown(Optional[bool]): parse text as markdown
            html(Optional[bool]): parse text as html
            reply_to(Optional[int]): ID of message to reply to

        Returns:
            bool: ``True`` if message was sent

        Raises:
            ValueError: if ``markdown`` and ``html`` are both ``True``

        """
        if markdown and html:
            raise ValueError("`markdown` and `html` are self-exclusive")

        if markdown:
            parse_mode = ParseMode.MARKDOWN
        elif html:
            parse_mode = ParseMode.HTML
        else:
            parse_mode = None

        self._bot.send_message(chat, text, parse_mode=parse_mode, reply_to_message_id=reply_to,
                               **kwargs)

    def delete_message(self, chat=None, message_id=None, message=None):
        """Deletes message

        Args:
            chat(Optional[str|int]): chat ID or '@channel_name'
            message_id(Optional[int]): ID of message to be deleted
            message(Optional[:class:`telegram.Message`]): message to be deleted

        Returns:
            bool: True if success

        Raises:
            ValueError: if ``chat``, ``message_id`` and ``message`` are ``None``

        """
        if (chat is None or message_id is None) and message is None:
            raise ValueError('Either `chat` and `message_id` or `message` must be given')
        if message is not None:
            chat = message.chat_id
            message_id = message.message_id

        self._bot.delete_message(chat, message_id)

    def ban_member(self, chat, user_id=None, user=None):
        if user_id is None and user is None:
            raise ValueError('Either `user_id` or `user` must be given')
        if user is not None:
            user_id = user.id

        self._bot.kick_chat_member(chat, user_id)

    def unban_member(self, chat, user_id=None, user=None):
        if user_id is None and user is None:
            raise ValueError('Either `user_id` or `user` must be given')
        if user is not None:
            user_id = user.id

        self._bot.unban_chat_member(chat, user_id)

    def kick_member(self, chat, user_id=None, user=None):
        self.ban_member(chat, user_id, user)
        self.unban_member(chat, user_id, user)

    def get_admins(self, chat, use_ids=False):
        admins = self._bot.get_chat_administrators(chat)
        if use_ids:
            return [admin.user.id for admin in admins]
        else:
            return list(admins)

    @property
    def bot_id(self):
        return self._bot.id


class ConfigAPI(JSONAPI):
    def __init__(self, name):
        super(ConfigAPI, self).__init__('config', name)


class LangAPI(JSONAPI):
    def __init__(self, name):
        super(LangAPI, self).__init__('lang', name)

    def __getitem__(self, item):
        if item is None:
            return None
        lang = item.split('-')[0].lower()
        return self._raw_data.get(lang, None)

    def __call__(self, lang, string):
        tr = self[lang]
        if lang is not None:
            tr = tr.get(string.lower(), None)

        if tr is None:
            return self['en'].get(string.lower(), None)
        return tr
