from datetime import datetime


class Logger:

    INFO: str = 'INFO'
    DEBUG: str = 'DEBUG'

    name: str
    level: str

    def __init__(self, name: str, level: str):
        self.name = name
        assert level in [self.INFO, self.DEBUG]
        self.level = level

    def info(self, msg: str):
        print(f'{self.name}\tINFO\t{datetime.now()}', flush=True)
        print(msg + '\n', flush=True)

    def debug(self, msg: str):
        if self.level == self.INFO:
            return
        print(f'{self.name}\tDEBUG\t{datetime.now()}', flush=True)
        print(msg + '\n', flush=True)
