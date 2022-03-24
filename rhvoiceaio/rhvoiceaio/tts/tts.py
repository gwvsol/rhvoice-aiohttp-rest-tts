import wave
import audioop
from wave import Error
from io import BytesIO
from rhvoice_wrapper import TTS as RHTTS

from rhvoiceaio.log import logging as log
from rhvoiceaio.config import conf


class TTS(object):
    """ Преобразование текста в речь """
    def __init__(self):
        self.tts = RHTTS(threads=1)
        self.voice = conf.TTS_DEFAULT_VOICE
        self.format = conf.TTS_DEFAULT_FORMAT
        self.log = log

    def voice_streamer(self, text: str, format: str, voice: str):
        """ Преобразование текста в звук """
        format_ = 'wav' if format in conf.TTS_ADD_FORMATS else format
        sound = self.tts.get(text,
                             format_=format_,
                             voice=voice)
        if format in conf.TTS_ADD_FORMATS:
            sound = self.to_alaw(sound, format)
        log.info(f'{format} => {len(sound)} bytes')
        return sound

    def to_alaw(self, wav: bytes, format: str) -> bytes:
        """ Конвертация wav в alaw или ulaw """
        try:
            with wave.open(BytesIO(wav), 'rb') as tsound:
                nchannels, \
                    sampwidth, \
                    framerate, \
                    nframes, \
                    _, _ = tsound.getparams()
                data = tsound.readframes(nframes)
            converted, _ = audioop.ratecv(data,
                                          sampwidth,
                                          nchannels,
                                          framerate,
                                          8000,
                                          None)
            if format == conf.TTS_ADD_FORMATS[0]:
                sound = audioop.lin2alaw(converted, 2)
            else:
                sound = audioop.lin2ulaw(converted, 2)
            return sound
        except (Error, EOFError) as err:
            self.log.info(f"TTS => {err}")
            return bytearray()
