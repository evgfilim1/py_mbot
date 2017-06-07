from os import listdir
import api

ENABLED = {}
DISABLED = []
FAILURE = {}


def load_modules(updater):
    telegram_api = api.TelegramAPI(updater)

    for module_name in listdir('./modules'):

        if module_name.endswith('.py'):
            module_name = module_name[:-3]
        else: continue
        try:
            print("Loading module '%s'... " % module_name, end='', flush=True)
            current_module = getattr(__import__('modules.{0}'.format(module_name)), module_name)
            loaded_module = current_module.TelegramModule(telegram_api)
        except Exception as e:
            print("failed")
            FAILURE.update({module_name: str(e)})
            continue


        if loaded_module.friendly_name:
            module_name = loaded_module.friendly_name

        if module_name in ENABLED or module_name in DISABLED:
            FAILURE.update({module_name: "module %s is already loaded" % module_name})
            print("already loaded")

        if loaded_module.disabled:
            DISABLED.append(module_name)
            print("disabled")
            continue

        ENABLED.update({module_name: loaded_module})
        print("OK")
