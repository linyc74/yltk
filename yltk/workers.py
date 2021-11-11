import os
from typing import List, Union, Optional
from .tools import Caller
from .path import LocalFile, LocalDir


class CmdWorker:

    github_repo: str
    caller: Caller
    cmd: str

    def __init__(self, github_repo: str, mock: bool = False):
        self.github_repo = github_repo
        self.caller = Caller(mock=mock)

    def run(self, cmd: str):
        self.cmd = cmd
        self.__clone_repo()
        self.__execute()
        self.__clean_up()

    def __clone_repo(self):
        self.caller.call(f'git clone {self.github_repo}')

    def __execute(self):
        self.caller.call(self.cmd)

    def __clean_up(self):
        # https://github.com/USER/REPO.git -> REPO
        repo_name = self.github_repo.split('/')[-1].split('.')[0]
        self.caller.call(f'rm -rf {repo_name}')


class DockerBuilder:

    IMAGE_TAG = 'latest'

    docker_hub_user: str
    github_repo: str
    caller: Caller

    repo_name: str
    image: str

    def __init__(
            self,
            docker_hub_user: str,
            github_repo: str,
            mock: bool = False):

        self.docker_hub_user = docker_hub_user
        self.github_repo = github_repo
        self.caller = Caller(mock=mock)

    def build(self) -> str:
        self.__clone_repo()
        self.__set_repo_name()
        self.__set_image()
        self.__build()
        self.__clean_up()
        return self.image

    def __clone_repo(self):
        self.caller.call(f'git clone {self.github_repo}')

    def __set_repo_name(self):
        """
        https://github.com/USER/REPO_NAME.git -> REPO_NAME
        """
        self.repo_name = self.github_repo.split('/')[-1].split('.')[0]

    def __set_image(self):
        """
        REPO_NAME -> repo-name
        """
        repo_name = self.repo_name.lower().replace('_', '-')
        self.image = f'{self.docker_hub_user}/{repo_name}:{self.IMAGE_TAG}'

    def __build(self):
        os.chdir(self.repo_name)
        self.caller.call(f'docker build -t {self.image} .')

    def __clean_up(self):
        os.chdir('../')
        self.caller.call(f'rm -rf {self.repo_name}')


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
