from bases import JSONAPI
from telegram import ParseMode, TelegramError
from telegram.ext import CommandHandler, MessageHandler, Filters
import utils
import pickle
import logging

logger = logging.getLogger(__name__)


class TelegramAPI(object):
    """Class which represents Telegram API between module and wrapper

    Attributes:
        bot_id(int): bot ID

    Args:
        updater(:class:`telegram.ext.Updater`): updater instance
        storage(:class:`api.StorageAPI`): data for ``main.py``

    """
    _commands = []

    @utils.log(logger, print_ret=False)
    def __init__(self, updater, storage):
        self._bot = updater.bot
        self._dispatcher = updater.dispatcher
        self._storage = storage

    @utils.log(logger, print_ret=False)
    def _register_command(self, command):
        if command in self._commands:
            raise ValueError('Command "{0}" is already registered'.format(command))
        self._commands.append(command)

    @utils.log(logger, print_ret=False)
    def register_command(self, commands, callback, allow_edited=False):
        """Registers commands handler

        Args:
            commands(list|tuple): list of commands to register
            callback(function): callable object to execute
            allow_edited(Optional[bool]): pass edited messages

        Raises:
            ValueError: if one of commands in ``commands`` was already registered

        """
        for command in commands:
            self._register_command(command)

        @utils.log(logger, print_ret=False)
        def process_update(bot, update):
            lang = utils.get_lang(self._storage, update.effective_user)
            callback(update.effective_message,
                     update.effective_message.text.split(' ')[1:], lang)
        self._dispatcher.add_handler(CommandHandler(commands, process_update,
                                                    allow_edited=allow_edited))

    @utils.log(logger, print_ret=False)
    def register_text_handler(self, callback, allow_edited=False):
        """Registers text message handler

        Args:
            callback(function): callable object to execute
            allow_edited(Optional[bool]): pass edited messages

        """
        @utils.log(logger, print_ret=False)
        def process_update(bot, update):
            lang = utils.get_lang(self._storage, update.effective_user)
            callback(update.effective_message, lang)
        self._dispatcher.add_handler(MessageHandler(Filters.text, process_update,
                                                    edited_updates=allow_edited))

    @utils.log(logger)
    def send_text_message(self, chat, text, markdown=False, html=False, reply_to=None,
                          force_reply_to=False, **kwargs):
        """Sends message

        Notes:
            For now, this method supports only sending message with markdown or HTML parsing

        Args:
            chat(int|str): chat ID or '@channel_name'
            text(str): text to send
            markdown(Optional[bool]): parse text as markdown
            html(Optional[bool]): parse text as html
            reply_to(Optional[int]): ID of message to reply to
            force_reply_to(Optional[bool]): Replies to message even in private chats

        Returns:
            bool: ``True`` if message was sent, ``False`` otherwise

        Raises:
            ValueError: if ``markdown`` and ``html`` are both ``True``

        """
        if markdown and html:
            raise ValueError('`markdown` and `html` are self-exclusive')

        if markdown:
            parse_mode = ParseMode.MARKDOWN
        elif html:
            parse_mode = ParseMode.HTML
        else:
            parse_mode = None

        if reply_to and self.is_private_chat(chat) and not force_reply_to:
            reply_to = None

        try:
            self._bot.send_message(chat, text, parse_mode=parse_mode, reply_to_message_id=reply_to,
                                   **kwargs)
        except TelegramError as e:
            logger.exception('Exception was raised while sending message', exc_info=e)
            return False
        return True

    @utils.log(logger)
    def delete_message(self, chat=None, message_id=None, message=None):
        """Deletes message

        Args:
            chat(Optional[int|str]): chat ID or '@channel_name'
            message_id(Optional[int]): ID of message to be deleted
            message(Optional[:class:`telegram.Message`]): message to be deleted

        Returns:
            bool: ``True`` on success, ``False`` otherwise

        Raises:
            ValueError: if ``chat``, ``message_id`` and ``message`` are ``None``

        """
        if (chat is None or message_id is None) and message is None:
            raise ValueError('Either `chat` and `message_id` or `message` must be given')
        if message is not None:
            chat = message.chat_id
            message_id = message.message_id

        try:
            return self._bot.delete_message(chat, message_id)
        except TelegramError as e:
            logger.exception('Exception was raised while deleting message', exc_info=e)
            return False

    @utils.log(logger)
    def ban_member(self, chat, user_id=None, user=None):
        """Bans chat member

        Args:
            chat(int|str): chat ID or '@channel_name'
            user_id(Optional[int]): user ID to be banned
            user(Optional[:class:`telegram.User`]): user to be banned

        Returns:
            bool: ``True`` on success, ``False`` otherwise

        Raises:
            ValueError: if both ``user_id`` and ``user`` were (not) given

        """
        if (user_id is None and user is None) or (user_id is not None and user is not None):
            raise ValueError('Either `user_id` or `user` must be given')
        if user is not None:
            user_id = user.id

        try:
            self._bot.kick_chat_member(chat, user_id)
        except TelegramError as e:
            logger.exception('Exception was raised while kicking member', exc_info=e)
            return False
        return True

    @utils.log(logger)
    def unban_member(self, chat, user_id=None, user=None):
        """Unbans chat member

        Args:
            chat(int|str): chat ID or '@channel_name'
            user_id(Optional[int]): user ID to be unbanned
            user(Optional[:class:`telegram.User`]): user to be unbanned

        Returns:
            bool: ``True`` on success, ``False`` otherwise

        Raises:
            ValueError: if both ``user_id`` and ``user`` were (not) given

        """
        if (user_id is None and user is None) or (user_id is not None and user is not None):
            raise ValueError('Either `user_id` or `user` must be given')
        if user is not None:
            user_id = user.id

        try:
            self._bot.unban_chat_member(chat, user_id)
        except TelegramError as e:
            logger.exception('Exception was raised while unbanning member', exc_info=e)
            return False
        return True

    @utils.log(logger)
    def kick_member(self, chat, user_id=None, user=None):
        """Kicks chat member

        Args:
            chat(int|str): chat ID or '@channel_name'
            user_id(Optional[int]): user ID to be unbanned
            user(Optional[:class:`telegram.User`]): user to be unbanned

        Returns:
            bool: ``True`` on success, ``False`` otherwise

        Raises:
            ValueError: if both ``user_id`` and ``user`` were (not) given

        """
        return self.ban_member(chat, user_id, user) and self.unban_member(chat, user_id, user)

    @utils.log(logger)
    def get_admins(self, chat, use_ids=False):
        """Get chat administrators and return them

        Args:
            chat(int|str): chat ID or '@channel_name'
            use_ids(Optional[bool]): if ``True``, returns list of IDs, otherwise returns list of
                ``telegram.ChatMember``

        Returns:
            list: list of admins

        """
        admins = self._bot.get_chat_administrators(chat)
        if use_ids:
            return [admin.user.id for admin in admins]
        else:
            return list(admins)

    @staticmethod
    @utils.log(logger)
    def is_private_chat(chat):
        """Checks whether ``chat`` is private chat

        Notes:
            If ``chat`` is str, it is considered as channel

        Args:
            chat(int|str): chat ID or '@channel_name' to check

        """
        return isinstance(chat, int) and chat > 0

    @property
    def bot_id(self):
        return self._bot.id


class ConfigAPI(JSONAPI):
    """This class gives easy access to config files used by module

    Args:
        name(str): module name

    """
    @utils.log(logger, print_ret=False)
    def __init__(self, name):
        super(ConfigAPI, self).__init__('config', name)


class LangAPI(JSONAPI):
    """This class gives easy access to language files (translations)

    Short usage:
    >>> tr = LangAPI('foo')
    >>> print(tr('en_US', 'bar'))

    If desired string cannot be found in specified language, it will fallback to 'en'.
    If desired string cannot be found in 'en', ``None`` is returned

    Args:
        name(str): module name

    """
    # TODO: use built-in python translation library
    @utils.log(logger, print_ret=False)
    def __init__(self, name):
        super(LangAPI, self).__init__('lang', name)

    @utils.log(logger)
    def __getitem__(self, item):
        if item is None:
            return None
        lang = item.split('-')[0]
        return super(LangAPI, self).__getitem__(lang)

    @utils.log(logger)
    def __call__(self, lang, string):
        tr = self[lang]
        if lang is not None:
            tr = tr.get(string.lower(), None)

        if tr is None:
            return self['en'].get(string.lower(), None)
        return tr


class StorageAPI(object):
    @utils.log(logger, print_ret=False)
    def __init__(self, name, load=True, autosave=True):
        from os import path, mkdir
        if not path.exists('./data'):
            logger.debug('Creating data directory...')
            mkdir('./data')
        self._file = './data/{0}.pkl'.format(name)
        self._autosave = autosave
        self._data = None
        if load:
            self.load()

    @utils.log(logger)
    def __getattr__(self, item):
        return self._data.get(item)

    @utils.log(logger, print_args=True)
    def __setattr__(self, key, value):
        if key[0] != '_':
            logger.debug('Setting data key')
            self.__dict__['_data'][key] = value
            if self._autosave:
                self.save()
        else:
            logger.debug('Setting class property')
            super(StorageAPI, self).__setattr__(key, value)

    @utils.log(logger, print_ret=False)
    def __delattr__(self, item):
        del self._data[item]

    @property
    def raw_data(self):
        return self._data

    @utils.log(logger)
    def load(self):
        try:
            with open(self._file, 'rb') as file:
                self._data = pickle.load(file)
        except FileNotFoundError:
            self._data = {}
        except Exception as e:
            logger.exception('Exception in `StorageAPI` was raised', exc_info=e)
            return False
        return True

    @utils.log(logger)
    def save(self):
        try:
            with open(self._file, 'wb') as file:
                pickle.dump(self._data, file, pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            logger.exception('Exception in `StorageAPI` was raised', exc_info=e)
            return False
        return True
