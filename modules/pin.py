from bases import BaseTelegramModule


class TelegramModule(BaseTelegramModule):
    def __init__(self, *args):
        super(TelegramModule, self).__init__(*args)
        self._telegram_api.register_command(['pin'], self.pin)

    def pin(self, message, args, lang):
        if len(args) == 0:
            self.help(message, args, lang)
            return
        markdown = False
        html = False
        if args[0] in ('md', 'html', 'no'):
            fmt = args.pop(0)
            if len(args) == 0:
                self.help(message, args, lang)
                return
            if fmt == 'md':
                markdown = True
            elif fmt == 'html':
                html = True
        msg_id = self._telegram_api.send_text_message(message.chat_id, ' '.join(args),
                                                      markdown=markdown, html=html)
        self._telegram_api.send_text_message(message.chat_id, self._tr(lang, 'pin_it'),
                                             reply_to=msg_id)
