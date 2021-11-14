import os
from typing import List, Tuple, Any, Optional
from .template import Caller


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


def get_temp_path(
        prefix: str = 'temp',
        suffix: str = '') -> str:
    """
    Returns a temp file name that does not exist, i.e. temp000.txt

    Args:
        prefix:
            Can include the path

        suffix:
            Usually the file extension
    """
    i = 1
    while True:
        fpath = f'{prefix}{i:03}{suffix}'
        if not os.path.exists(fpath):
            return fpath
        i += 1


def gzip(
        file: str,
        dstdir: Optional[str] = None,
        keep: bool = True) -> str:

    if dstdir is None:
        dstdir = os.path.dirname(file)

    fname = os.path.basename(file) + '.gz'

    call(f'gzip --stdout {file} > {os.path.join(dstdir, fname)}')

    if not keep:
        os.remove(file)

    return f'{dstdir}/{fname}'


def gunzip(
        file: str,
        dstdir: Optional[str] = None,
        keep: bool = True) -> str:

    if dstdir is None:
        dstdir = os.path.dirname(file)

    fname = os.path.basename(file)[:-3]

    call(f'gzip --decompress --stdout {file} > {os.path.join(dstdir, fname)}')

    if not keep:
        os.remove(file)

    return f'{dstdir}/{fname}'
