from os import listdir
import api
import logging

ENABLED = {}
DISABLED = []
FAILURE = {}

logger = logging.getLogger('modloader')


def load_modules(updater):
    telegram_api = api.TelegramAPI(updater)

    for module_name in listdir('./modules'):
        if module_name.endswith('.py'):
            module_name = module_name[:-3]
        try:
            logger.info('Loading module "{0}"... '.format(module_name))
            current_module = getattr(__import__('modules.{0}'.format(module_name)), module_name)
            loaded_module = current_module.TelegramModule(telegram_api)
        except Exception as e:
            logger.warning('Cannot load module "{0}": {1}'.format(module_name, str(e)))
            FAILURE.update({module_name: str(e)})
            continue

        if loaded_module.friendly_name:
            module_name = loaded_module.friendly_name

        if module_name in ENABLED or module_name in DISABLED:
            FAILURE.update({module_name: 'Module is already loaded'})
            logger.warning('Module "{0}" is already loaded'.format(module_name))

        if loaded_module.disabled:
            DISABLED.append(module_name)
            logger.info('Module "{0}" is disabled'.format(module_name))
            continue

        ENABLED.update({module_name: loaded_module})
        logger.info('Module "{0}" loaded successfully'.format(module_name))
