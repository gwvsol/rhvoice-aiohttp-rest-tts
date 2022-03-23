from gunicorn.app.base import BaseApplication
from asyncio.exceptions import CancelledError

from rhvoiceaio.config import conf
from rhvoiceaio.api import rhvoiceaio
# from rhvoiceaio.log import logging as log


class Application(BaseApplication):
    """ Gunicorn Custom Application """
    def __init__(self, app, options=None):
        self.application = app
        self.options = options or {}
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def main():
    try:
        options = {
            'bind': f'{conf.RHVOICEAIO_HOST}:{conf.RHVOICEAIO_PORT}',
            'workers': conf.RHVOICEAIO_WORKER,
            'keepalive': conf.RHVOICEAIO_KEEPALIVE,
            'timeout': conf.RHVOICEAIO_TIMEOUT,
            'worker_class': conf.RHVOICEAIO_WORKER_CLASS,
            'accesslog': conf.RHVOICEAIO_LOG,
            'access_log_format': conf.RHVOICEAIO_LOG_FORMAT,
        }
        Application(rhvoiceaio(), options).run()
    except CancelledError:
        pass


if __name__ == '__main__':
    main()
