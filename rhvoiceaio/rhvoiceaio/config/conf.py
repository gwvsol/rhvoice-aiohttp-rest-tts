from os import getenv as env

from rhvoiceaio.exeption import ConfigError
# from rhvoiceaio.log import logging as log

# on = ['on', 'On', 'ON', '1', 'True', 'TRUE', 'true']
#
# =====================================================
#
RHVOICEAIO_HOST = env('RHVOICEAIO_HOST', default=None)
if RHVOICEAIO_HOST is None:
    raise ConfigError('RHVOICEAIO_HOST ERROR in env')
#
RHVOICEAIO_PORT = env('RHVOICEAIO_PORT', default=None)
if RHVOICEAIO_PORT.isdigit():
    RHVOICEAIO_PORT = int(RHVOICEAIO_PORT)
else:
    raise ConfigError('RHVOICEAIO_PORT ERROR in env')
#
RHVOICEAIO_URL = env('RHVOICEAIO_URL', default=None)
if RHVOICEAIO_URL is None:
    raise ConfigError('RHVOICEAIO_URL ERROR in env')
#
RHVOICEAIO_WORKER = 1
RHVOICEAIO_WORKER_CLASS = 'aiohttp.GunicornWebWorker'
RHVOICEAIO_KEEPALIVE = 2
RHVOICEAIO_TIMEOUT = 5
RHVOICEAIO_LOG = None
RHVOICEAIO_LOG_FORMAT = '%a %t "%r" %s %b "%{Referer}i" "%{User-Agent}i"'
#
# =====================================================
#
TTS_DEFAULT_VOICE = env('TTS_DEFAULT_VOICE', default=None)
if TTS_DEFAULT_VOICE is None:
    raise ConfigError('TTS_DEFAULT_VOICE ERROR in env')
#
TTS_DEFAULT_FORMAT = env('TTS_DEFAULT_FORMAT', default=None)
if TTS_DEFAULT_FORMAT is None:
    raise ConfigError('TTS_DEFAULT_FORMAT ERROR in env')
#
# =====================================================
