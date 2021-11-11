import os
from typing import List, Tuple, Any, Optional
from subprocess import check_call, check_output
from .logger import Logger


class Caller:

    mock: bool

    def __init__(self, mock: bool):
        self.mock = mock
        self.logger = Logger(name=f'{self.__class__.__name__}', level='INFO')

    def call(self, cmd: str):
        self.__log(cmd)
        if not self.mock:
            check_call(cmd, shell=True)

    def check_output(self, cmd: str) -> str:
        self.__log(cmd)
        return '' if self.mock \
            else check_output(cmd, shell=True).decode()

    def __log(self, cmd: str):
        h = 'MOCK' if self.mock else 'CMD'
        self.logger.info(f'{h}: {cmd}')


def call(cmd: str, mock: bool = False):
    caller = Caller(mock=mock)
    caller.call(cmd=cmd)


def build_cmd(
        base_cmd: Optional[str],
        args: List[Tuple[str, Any]]) -> str:

    lines = []

    if base_cmd:
        lines.append(base_cmd)

    for key, val in args:
        d = '-' if len(key) == 1 else '--'
        val = '' if val is None else val
        lines.append(f'{d}{key} {val}')

    return ' \\\n'.join(lines)


def get_files(
        source: str = '.',
        startswith: str = '',
        endswith: str = '',
        isfullpath: bool = False) -> List[str]:
    """
    Get all files that start with or end with some strings in the source folder

    Args:
        startswith

        endswith

        source: path-like
            The source directory

        isfullpath
            If True, return the full file paths in the list

    Returns:
        A list of file names, or file paths
        If no files found, return an empty list []
    """
    ret = []
    s, e = startswith, endswith
    for path, dirs, files in os.walk(source):
        if path == source:
            ret = [f for f in files if (f.startswith(s) and f.endswith(e))]

    if isfullpath:
        ret = [os.path.join(source, f) for f in ret]

    if ret:
        # Sort the file list so that the order will be
        #     consistent across different OS platforms
        ret.sort()
    return ret


def get_dirs(
        source: str = '.',
        startswith: str = '',
        endswith: str = '',
        isfullpath: bool = False) -> List[str]:
    """
    Similar to 'get_files()' but finds directories
    """

    ret = []
    s, e = startswith, endswith
    for path, dirs, files in os.walk(source):
        if path == source:
            ret = [d for d in dirs if (d.startswith(s) and d.endswith(e))]

    if isfullpath:
        ret = [os.path.join(source, d) for d in ret]

    if ret:
        # Sort the file list so that the order will be
        #     consistent across different OS platforms
        ret.sort()
    return ret

