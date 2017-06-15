from os import listdir
import api
import utils
import logging

ENABLED = {}
DISABLED = []
FAILURE = {}
MODULE_COUNT = 0

logger = logging.getLogger(__name__)


@utils.log(logger, print_ret=False)
def load_modules(updater, storage):
    global MODULE_COUNT
    telegram_api = api.TelegramAPI(updater, storage)

    modules = []
    blacklisted_modules = []
    files = listdir('./modules')
    logger.debug('Parsing modules in `./modules`')
    logger.debug('Found {0} modules'.format(len(files)))
    for filename in files:
        if filename.startswith('_'):
            logger.info('Skipping module "{0}"'.format(filename))
            continue
        if filename.endswith('.py'):
            filename = filename[:-3]
        elif filename.endswith('.pyc'):
            filename = filename[:-4]
        if filename in modules:
            logger.warning('Conflicting modules with the same name: "{0}", '
                           'skipping all...'.format(filename))
            modules.pop(modules.index(filename))
            blacklisted_modules.append(filename)
        if filename in blacklisted_modules:
            continue
        modules.append(filename)

    for module_name in blacklisted_modules:
        FAILURE.update({module_name: 'conflicting modules with the same name'})

    logger.debug('Initializing modules...')
    for module_name in modules:
        lang = api.LangAPI(module_name)
        try:
            logger.info('Loading module "{0}"... '.format(module_name))
            current_module = getattr(__import__('modules.{0}'.format(module_name)), module_name)
            loaded_module = current_module.TelegramModule(telegram_api, lang)
        except InterruptedError:
            logger.info('Skipping module "{0}": module is disabled'.format(module_name))
            DISABLED.append(module_name)
            continue
        except Exception as e:
            logger.exception('Cannot load module "{0}"'.format(module_name), exc_info=e)
            FAILURE.update({module_name: str(e)})
            continue

        filename = module_name
        if loaded_module.friendly_name:
            friendly_module_name = loaded_module.friendly_name
        else:
            friendly_module_name = module_name

        if friendly_module_name in ENABLED or friendly_module_name in DISABLED:
            logger.warning('Module "{0}" is already loaded, '
                           'using "{1}" as module name'.format(friendly_module_name, filename))
            friendly_module_name = filename

        ENABLED.update({friendly_module_name: loaded_module})
        logger.info('Module "{0}" ("{1}") loaded successfully'.format(module_name,
                                                                      friendly_module_name))
        MODULE_COUNT += 1

    logger.info('Loaded {0} modules'.format(MODULE_COUNT))
