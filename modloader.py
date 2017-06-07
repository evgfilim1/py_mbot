from os import listdir
import api
import logging

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
            logging.getLogger("modloader").info("Loading module '%s'... ", module_name)
            current_module = getattr(__import__('modules.{0}'.format(module_name)), module_name)
            loaded_module = current_module.TelegramModule(telegram_api)
        except Exception as e:
            logging.getLogger("modloader").warn("Cannot load module '%s': %s", module_name, str(e))
            FAILURE.update({module_name: str(e)})
            continue


        if loaded_module.friendly_name:
            module_name = loaded_module.friendly_name

        if module_name in ENABLED or module_name in DISABLED:
            FAILURE.update({module_name: "module %s is already loaded" % module_name})
            logging.getLogger("modloader").warn("Module '%s' is already loaded", module_name)

        if loaded_module.disabled:
            DISABLED.append(module_name)
            logging.getLogger("modloader").info("Module '%s' is disabled", module_name)
            continue

        ENABLED.update({module_name: loaded_module})
        logging.getLogger("modloader").info("Module '%s' loaded successfully", module_name)
