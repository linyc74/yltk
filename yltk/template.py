import subprocess
from .logger import Logger


class Settings:

    workdir: str
    outdir: str
    threads: int
    debug: bool
    mock: bool

    def __init__(
            self,
            workdir: str,
            outdir: str,
            threads: int,
            debug: bool,
            mock: bool):

        self.workdir = workdir
        self.outdir = outdir
        self.threads = threads
        self.debug = debug
        self.mock = mock


class Processor:

    settings: Settings
    workdir: str
    outdir: str
    threads: int
    debug: bool
    mock: bool

    logger: Logger

    def __init__(self, settings: Settings):

        self.settings = settings
        self.workdir = settings.workdir
        self.outdir = settings.outdir
        self.threads = settings.threads
        self.debug = settings.debug
        self.mock = self.settings.mock

        self.logger = Logger(
            name=self.__class__.__name__,
            level=Logger.DEBUG if self.debug else Logger.INFO
        )

    def call(self, cmd: str):
        self.logger.info(cmd)
        if not self.mock:
            subprocess.check_call(cmd, shell=True)
