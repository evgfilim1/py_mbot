from os import listdir
import api
import logging

ENABLED = {}
DISABLED = []
FAILURE = {}
MODULE_COUNT = 0

logger = logging.getLogger('modloader')


def load_modules(updater):
    global MODULE_COUNT
    telegram_api = api.TelegramAPI(updater)

    for module_name in listdir('./modules'):
        if module_name.endswith('.py'):
            module_name = module_name[:-3]
        if module_name.startswith('_'):
            logger.info('Skipping module "{0}"'.format(module_name))
            continue

        try:
            logger.info('Loading module "{0}"... '.format(module_name))
            current_module = getattr(__import__('modules.{0}'.format(module_name)), module_name)
            loaded_module = current_module.TelegramModule(telegram_api)
        except InterruptedError:
            logger.info('Skipping module "{0}": module is disabled'.format(module_name))
            DISABLED.append(module_name)
            continue
        except Exception as e:
            logger.warning('Cannot load module "{0}": {1}'.format(module_name, str(e)))
            FAILURE.update({module_name: str(e)})
            continue

        if loaded_module.friendly_name:
            module_name = loaded_module.friendly_name

        if module_name in ENABLED or module_name in DISABLED:
            FAILURE.update({module_name: 'Module is already loaded'})
            logger.warning('Module "{0}" is already loaded'.format(module_name))

        ENABLED.update({module_name: loaded_module})
        logger.info('Module "{0}" loaded successfully'.format(module_name))
        MODULE_COUNT += 1

    logger.info('Loaded {0} modules'.format(MODULE_COUNT))
