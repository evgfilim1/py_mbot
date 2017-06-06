from bases import BaseTelegramModule
from random import choice

FACES_LIST = ["ლ(ಠ益ಠლ)", "/╲/\╭( ͡° ͡° ͜ʖ ͡° ͡°)╮/\╱\\", "(;´༎ຶД༎ຶ`)", "♪~ ᕕ(ᐛ)ᕗ", "♥‿♥",
              "▄︻̷̿┻̿═━一", "( ͡°( ͡° ͜ʖ( ͡° ͜ʖ ͡°)ʖ ͡°) ͡°)", "ʕ•ᴥ•ʔ", "(▀̿Ĺ̯▀̿ ̿)", "(ง ͠° ͟ل͜ ͡°)ง",
              "༼ つ ◕_◕ ༽つ", "(づ｡◕‿‿◕｡)づ", "(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧ ✧ﾟ･: *ヽ(◕ヮ◕ヽ)", "༼ʘ̚ل͜ʘ̚༽",
              "[̲̅$̲̅(̲̅5̲̅)̲̅$̲̅]", "┬┴┬┴┤ ͜ʖ ͡°) ├┬┴┬┴", "( ͡°╭͜ʖ╮͡° )", "(͡ ͡° ͜ つ ͡͡°)",
              "(• ε •)", "(ง'̀-'́)ง", "(ಥ﹏ಥ)", "﴾͡๏̯͡๏﴿ O'RLY?", "(ノಠ益ಠ)ノ彡┻━┻",
              "[̲̅$̲̅(̲̅ ͡° ͜ʖ ͡°̲̅)̲̅$̲̅]", "(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧", "(☞ﾟ∀ﾟ)☞", "| (• ◡•)| (❍ᴥ❍ʋ)",
              "(◕‿◕✿)", "(ᵔᴥᵔ)", "(¬‿¬)", "(☞ﾟヮﾟ)☞ ☜(ﾟヮﾟ☜)", "(づ￣ ³￣)づ", "(~˘▾˘)~",
              "(._.) ( l: ) ( .-. ) ( :l ) (._.)", "༼ ºل͟º ༼ ºل͟º ༼ ºل͟º ༽ ºل͟º ༽ ºل͟º ༽",
              "༼ つ  ͡° ͜ʖ ͡° ༽つ", "(╯°□°）╯︵ ┻━┻", "( ͡ᵔ ͜ʖ ͡ᵔ )", "ヾ(⌐■_■)ノ♪",
              "~(˘▾˘~)", "◉_◉", "\ (•◡•) /", "┬┴┬┴┤(･_├┬┴┬┴", "ᕙ(⇀‸↼‶)ᕗ", "ᕦ(ò_óˇ)ᕤ",
              "┻━┻ ︵ヽ(`Д´)ﾉ︵ ┻━┻", "⚆ _ ⚆", "(•_•) ( •_•)>⌐■-■ (⌐■_■)", "(☞ຈل͜ຈ)☞",
              "(｡◕‿‿◕｡)", "ヽ༼ຈل͜ຈ༽ﾉ", "☜(˚▽˚)☞", "˙ ͜ʟ˙", "(｡◕‿◕｡)", "（╯°□°）╯︵( .o.)",
              ":')", "(°ロ°)☝", "┬──┬ ノ( ゜-゜ノ)", "（╯°□°）╯︵( .o.)", "(っ˘ڡ˘ς)",
              "ლ(´ڡ`ლ)", "｡◕‿‿◕｡", "(/) (°,,°) (/)", "☼.☼", "^̮^"]


class TelegramModule(BaseTelegramModule):
    def __init__(self, telegram_api):
        super(TelegramModule, self).__init__(telegram_api)
        self.commands = ((['lenny'], self.lenny),
                         (['shrug'], self.shrug),
                         (['random_face'], self.random_face))
        self._register_module()

    def help(self, message, args):
        self._telegram_api.send_text_message(message.chat_id, "This module sends /shrug, "
                                             "/lenny or /random_face")"

    def lenny(self, message, args):
        self._telegram_api.send_text_message(message.chat_id, "( ͡° ͜ʖ ͡° )")

    def shrug(self, message, args):
        self._telegram_api.send_text_message(message.chat_id, "¯\_(ツ)_/¯")

    def random_face(self, message, args):
        self._telegram_api.send_text_message(message.chat_id, choice(FACES_LIST)) # random face
