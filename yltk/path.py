from os.path import abspath, dirname


class LocalFile:

    path: str
    dirpath: str

    def __init__(self, path: str):
        self.path = abspath(path)
        self.dirpath = dirname(self.path)

    def __str__(self):
        return self.path

    def __repr__(self):
        return f"LocalFile(path='{self.path}')"

    def to_docker_volume(self) -> str:
        return f'--volume "{self.dirpath}":"{self.dirpath}"'


class LocalDir:

    path: str

    def __init__(self, path: str):
        self.path = abspath(path)

    def __str__(self):
        return self.path

    def __repr__(self):
        return f"LocalDir(path='{self.path}')"

    def to_docker_volume(self) -> str:
        return f'--volume "{self.path}":"{self.path}"'
