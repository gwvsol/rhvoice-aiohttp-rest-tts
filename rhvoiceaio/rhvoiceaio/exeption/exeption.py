
class RhvoiceAioError(Exception):
    """ Обработка исключений RhvoiceAioError """
    def __init__(self, *args):
        self.args = [a for a in args]


class ConfigError(RhvoiceAioError):
    """ Обработка исключений ConfigError """
    pass


class TTSError(RhvoiceAioError):
    """ Обработка исключений TTSService """
    pass
