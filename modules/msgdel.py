from bases import BaseTelegramModule


class TelegramModule(BaseTelegramModule):
    def __init__(self, telegram_api):
        super(TelegramModule, self).__init__(telegram_api)
        self._telegram_api.register_command(['delete'], self.delete)
        self.friendly_name = 'DeleteMessageModule'

    def help(self, message, args):
        self._telegram_api.send_text_message(message.chat_id,
                                             'This module helps to delete any message sent by bot'
                                             '\nUsage:\nReply to message which you want to delete '
                                             'and type /delete', reply_to=message.message_id)

    def delete(self, message, args):
        if message.reply_to_message.from_user.id == self._telegram_api.bot_id:
            self._telegram_api.delete_message(message=message.reply_to_message)
