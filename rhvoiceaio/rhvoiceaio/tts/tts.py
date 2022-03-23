from rhvoice_wrapper import TTS as RHTTS

from rhvoiceaio.log import logging as log
from rhvoiceaio.config import conf
from rhvoiceaio.exeption import TTSError


class TTS(object):
    """ Преобразование текста в речь """
    def __init__(self):
        self.tts = RHTTS(threads=1)
        self.log = log
