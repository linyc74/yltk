from os.path import abspath, dirname
from typing import List, Union, Optional
from .template import Caller


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


class CmdWorker:

    repo: Optional[str]
    caller: Caller

    def __init__(self, repo: Optional[str], mock: bool = False):
        self.repo = repo
        self.caller = Caller(mock=mock)

    def run(self, cmd: str):
        self.__clone_repo()
        self.caller.call(cmd)
        self.__clean_up()

    def __clone_repo(self):
        if self.repo is not None:
            if self.repo.startswith('https://github.com'):
                self.caller.call(f'git clone {self.repo}')

    def __clean_up(self):
        if self.repo is not None:
            if self.repo.startswith('https://github.com'):  # clean up only if repo was cloned from github
                repo_name = self.repo.split('/')[-1].split('.')[0]  # https://github.com/USER/REPO.git -> REPO
                self.caller.call(f'rm -rf {repo_name}')


class DockerBuilder:

    DEFAULT_TAG = 'latest'

    docker_hub_user: str
    repo: str
    caller: Caller

    __repo: str
    __image: str

    def __init__(
            self,
            docker_hub_user: str,
            repo: str,
            mock: bool = False):

        self.docker_hub_user = docker_hub_user
        self.repo = repo
        self.caller = Caller(mock=mock)

    def build(self) -> str:
        self.__clone_repo()
        self.__set_image()
        self.__build()
        self.__clean_up()
        return self.__image

    def __clone_repo(self):
        if self.repo.startswith('https://github.com'):
            self.caller.call(f'git clone {self.repo}')

    def __set_image(self):
        repo = self.repo

        if repo.startswith('https://github.com'):
            repo = repo.split('/')[-1].split('.')[0]  # https://github.com/USER/REPO.git -> REPO

        self.__repo = repo

        name = repo.lower().replace('_', '-')  # REPO_NAME -> repo-name
        self.__image = f'{self.docker_hub_user}/{name}:{self.DEFAULT_TAG}'

    def __build(self):
        self.caller.call(f'cd {self.__repo} && docker build -t {self.__image} . && cd ..')

    def __clean_up(self):
        if self.repo.startswith('https://github.com'):  # clean up only if repo was cloned from github
            self.caller.call(f'rm -rf {self.__repo}')


MOUNT_TYPE = Union[
    LocalFile,
    LocalDir,
    List[Union[LocalFile, LocalDir]],
]


class DockerWorker:

    LINEBREAK = ' \\\n'

    image: str
    caller: Caller

    cmd: str
    mount: List[Union[LocalFile, LocalDir]]
    docker_cmd: str

    def __init__(self, image: str, mock: bool = False):
        self.image = image
        self.caller = Caller(mock=mock)

    def run(self, cmd: str, mount: Optional[MOUNT_TYPE] = None):
        self.cmd = cmd
        self.__set_mount(mount)

        self.__set_docker_cmd()
        self.__execute()
        self.__clean_up()

    def __set_mount(self, mount: Optional[MOUNT_TYPE]):
        if mount is None:
            self.mount = []
        elif type(mount) in [LocalFile, LocalDir]:
            self.mount = [mount]
        else:
            self.mount = mount

    def __set_docker_cmd(self):
        lines = [
            'docker run',
            *self.__mount_lines(),
            self.image,
            self.cmd,
        ]
        self.docker_cmd = self.LINEBREAK.join(lines)

    def __mount_lines(self) -> List[str]:
        lines = [m.to_docker_volume() for m in self.mount]
        return list(set(lines))

    def __execute(self):
        return self.caller.call(self.docker_cmd)

    def __clean_up(self):
        self.caller.call('docker system prune --force')
