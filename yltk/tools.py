import os
from typing import List, Tuple, Any, Optional
from os.path import join, exists, basename, dirname
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

    ret = []
    s, e = startswith, endswith
    for path, dirs, files in os.walk(source):
        if path == source:
            ret = [f for f in files if (f.startswith(s) and f.endswith(e))]

    if isfullpath:
        ret = [join(source, f) for f in ret]

    if ret:
        ret.sort()  # make the order consistent across OS platforms
    return ret


def get_dirs(
        source: str = '.',
        startswith: str = '',
        endswith: str = '',
        isfullpath: bool = False) -> List[str]:

    ret = []
    s, e = startswith, endswith
    for path, dirs, files in os.walk(source):
        if path == source:
            ret = [d for d in dirs if (d.startswith(s) and d.endswith(e))]

    if isfullpath:
        ret = [join(source, d) for d in ret]

    if ret:
        ret.sort()  # make the order consistent across OS platforms
    return ret


def get_temp_path(
        prefix: str = 'temp',
        suffix: str = '') -> str:

    i = 1
    while True:
        fpath = f'{prefix}{i:03}{suffix}'
        if not exists(fpath):
            return fpath
        i += 1


def gzip(
        file: str,
        dstdir: Optional[str] = None,
        keep: bool = True) -> str:

    if dstdir is None:
        dstdir = dirname(file)

    fname = basename(file) + '.gz'

    call(f'gzip --stdout {file} > {os.path.join(dstdir, fname)}')

    if not keep:
        os.remove(file)

    return f'{dstdir}/{fname}'


def gunzip(
        file: str,
        dstdir: Optional[str] = None,
        keep: bool = True) -> str:

    if dstdir is None:
        dstdir = dirname(file)

    fname = basename(file)[:-3]

    call(f'gzip --decompress --stdout {file} > {join(dstdir, fname)}')

    if not keep:
        os.remove(file)

    return f'{dstdir}/{fname}'
