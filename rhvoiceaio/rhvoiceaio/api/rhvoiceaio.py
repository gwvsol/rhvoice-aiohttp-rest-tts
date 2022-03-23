from aiohttp import web
from urllib import parse

from rhvoiceaio.log import logging as log
from rhvoiceaio.config import RHVOICEAIO_HOST, \
                              RHVOICEAIO_PORT, \
                              RHVOICEAIO_URL
from rhvoiceaio.tts import TTS


async def say_handle(request):
    text = ' '.join([x for x in parse.unquote(
        request.query.get('text', '')).splitlines() if x])
    # voice = request.query.get('voice', DEFAULT_VOICE)
    # format_ = request.query.get('format', DEFAULT_FORMAT)
    log.info(f"{text}")
    return web.Response(text="Hello, world")


async def start_tts(app):
    """ Запуск TTS в фоне """
    app['tts'] = TTS()
    log.info("=> start")


async def stop_tts(app):
    """ Остановка TTS """
    log.info("=> stop")
    app['tts'].tts.join()


def rhvoiceaio():
    """ Запуск RHVOICEAIO """
    app = web.Application()
    app.add_routes([web.get(f'/{RHVOICEAIO_URL}', say_handle)])
    app.on_startup.append(start_tts)
    app.on_shutdown.append(stop_tts)
    url = f"http://{RHVOICEAIO_HOST}:{RHVOICEAIO_PORT}/{RHVOICEAIO_URL}"
    log.info(f"Start RHVOICEAIO => {url}")
    return app
