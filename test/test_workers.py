from yltk.workers import LocalFile, LocalDir, CmdWorker, DockerBuilder, DockerWorker
from .setup import TestCase


class TestCmdWorker(TestCase):

    def test_github(self):
        CmdWorker(
            repo='https://github.com/USER/REPO.git',
            mock=True
        ).run(cmd=f'echo "Hello, World!"')

    def test_local(self):
        CmdWorker(
            repo='REPO',
            mock=True
        ).run(cmd=f'echo "Hello, World!"')


class TestDockerBuilder(TestCase):

    def test_github(self):
        DockerBuilder(
            docker_hub_user='user',
            repo='https://github.com/account/my_repo.git',
            mock=True
        ).build()

    def test_local(self):
        DockerBuilder(
            docker_hub_user='user',
            repo='my_repo',
            mock=True
        ).build()


class TestDockerWorker(TestCase):

    def test_run(self):
        local_file = LocalFile('./subfolder/file.txt')
        local_dir = LocalDir('./dir')

        DockerWorker(
            image='image:latest',
            mock=True
        ).run(
            cmd=f'echo "Hello, World!"',
            mount=[local_file, local_dir]
        )
