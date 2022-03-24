import asyncio
from aiohttp import web
from shlex import quote
from urllib import parse
from datetime import datetime, timezone
from aiohttp.web_exceptions import HTTPBadRequest
from aiohttp.http_exceptions import BadHttpMessage

from rhvoiceaio.config import TTS_FORMATS, \
                              TTS_DEFAULT_VOICE, \
                              TTS_DEFAULT_FORMAT, \
                              START_TIME
from rhvoiceaio.tts import TTS
from rhvoiceaio.log import logging as log


async def _get_datetime(start: int = 0) -> dict:
    """ Получение текущего времени """
    now = round(datetime.now().timestamp())
    uptime = now - start
    date = datetime.fromtimestamp(uptime, tz=timezone.utc)
    return uptime, date


async def _datetime_to_str(date: datetime) -> str:
    """ Преобразование времени в строку """
    tz = date.strftime('%z')
    tz = f'{tz[:3]}:{tz[3:]}'
    return f"{date.strftime('%y-%m-%dT%H:%M:%S')}{tz}"


async def _get_info() -> dict:
    """ Получение времени работы сервиса """
    _, date = await _get_datetime()
    date = await _datetime_to_str(date)
    uptime, uptime_date = await _get_datetime(START_TIME)
    uptime_date = await _datetime_to_str(uptime_date.replace(year=2000))
    return dict(uptime=uptime, uptime_str=uptime_date, datetime=date)


async def _get_text(request) -> str:
    """ Получение текста для перевода в речь """
    text = quote(' '.join([x for x in parse.unquote(
        request.query.get('text', '')).splitlines() if x])).strip()
    if len(text) > 2:
        log.info(f'<= {text}')
        return text
    else:
        raise HTTPBadRequest(reason='Unset text')


async def _get_format(request, list_: bool = False) -> str or tuple:
    """ Получение списка поддреживаемых форматов """
    formats_ = list(request.app['tts'].tts.formats)
    formats_.extend(['alaw', 'ulaw'])

    if list_:
        return formats_

    format_ = request.query.get('format', TTS_DEFAULT_FORMAT)

    if format_ in formats_:
        return format_, TTS_FORMATS.get(format_)
    else:
        err = f'Unknown format: {format_}'
        log.warning(f"error => {err}")
        raise HTTPBadRequest(reason=err)


async def _get_voice(request, list_: bool = False) -> str:
    """ Получение списка поддреживаемых голосов """
    voices_ = request.app['tts'].tts.voices_info

    if list_:
        return voices_

    voice_ = request.query.get('voice', TTS_DEFAULT_VOICE)

    if voice_ in voices_:
        return voice_
    else:
        err = f'Unknown voice: {voice_}'
        log.warning(f"error => {err}")
        raise HTTPBadRequest(reason=err)


@asyncio.coroutine
async def say_handle(request):
    """ Обработчик перевода текста в речь
        http://192.168.62.148:8040/say?text=привет&format=mp3&voice=arina """
    try:
        text = await _get_text(request)
        voice = await _get_voice(request)
        format_, mime = await _get_format(request)
        log.info(f"text => {text}, voice => {voice}, format => {format_}")
        sound = request.app['tts'].voice_streamer(text=text,
                                                  format=format_,
                                                  voice=voice)

        response = web.StreamResponse(
            status=200,
            headers={'Content-Type': mime},)
        await response.prepare(request)
        await response.write(sound)
        return response

    except BadHttpMessage as err:
        log.error(f"error => {err}")
        raise HTTPBadRequest(err)


@asyncio.coroutine
async def format_handle(request):
    """ Получение данных о поддерживаемых фотматах
        curl -s "http://192.168.62.148:8040/formats" | jq '.' """
    formats_ = await _get_format(request, list_=True)
    return web.json_response({'formats': formats_})


@asyncio.coroutine
async def voices_handle(request):
    """ Получение данных о поддерживаемых голосах
        curl -s "http://192.168.62.148:8040/voices" | jq '.' """
    voices_ = await _get_voice(request, list_=True)
    return web.json_response({'voices_info': voices_})


@asyncio.coroutine
async def info_handle(request):
    """ Проверка работы сервиса
        curl -s "http://192.168.62.148:8040" | jq '.' """
    return web.json_response(await _get_info())


@web.middleware
async def error_middleware(request, handler):
    """ Обработка 400 и 404 """
    try:
        response = await handler(request)
        if response.status != 404:
            return response
        message = response.message
    except web.HTTPException as ex:
        if ex.status not in [400, 404]:
            raise
        message = ex.reason
    return web.json_response({'error': message})


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
    app = web.Application(middlewares=[error_middleware])
    app.add_routes([web.get('/', info_handle),
                    web.get('/say', say_handle),
                    web.get('/voices', voices_handle),
                    web.get('/formats', format_handle)])
    app.on_startup.append(start_tts)
    app.on_shutdown.append(stop_tts)
    log.info("Start RHVOICEAIO")
    return app
