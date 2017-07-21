from bases import BaseTelegramModule


class TelegramModule(BaseTelegramModule):
    RU = r"""ёЁ"№;:?йЙцЦуУкКеЕнНгГшШщЩзЗхХъЪ\/фФыЫвВаАпПрРоОлЛдДжЖэЭяЯчЧсСмМиИтТьЬбБюЮ.,"""
    EN = r"""`~@#$^&qQwWeErRtTyYuUiIoOpP[{]}\|aAsSdDfFgGhHjJkKlL;:'"zZxXcCvVbBnNmM,<.>/?"""
    SWAP = str.maketrans(RU + EN, EN + RU)
    
    def __init__(self, *args):
        super().__init__(*args)
        self._telegram_api.register_command(['sk', 'fixkb'], self.swap)
        self.friendly_name = 'SwapKeyLayout'
    
    def swap(self, message, args, lang):
        reply = message.reply_to_message
        try:
            text = reply.text or reply.caption
        except AttributeError:
            text = ''
        if text != '':
            self._telegram_api.send_text_message(message.chat_id, text.translate(self.SWAP),
                                                 reply_to=reply.message_id, force_reply_to=True)
        else:
            self._telegram_api.send_text_message(message.chat_id, self._tr(lang, 'notext'),
                                                 markdown=True, reply_to=message.message_id)
