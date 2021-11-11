import unittest
from yltk.workers import CmdWorker, DockerBuilder, DockerWorker
from yltk.path import LocalFile, LocalDir


class TestCmdWorker(unittest.TestCase):

    def setUp(self):
        self.worker = CmdWorker(
            github_repo='https://github.com/linyc74/qiime2_pipeline.git',
            mock=False)

    def test_run(self):
        self.worker.run(cmd='python qiime2_pipeline --help')


class TestDockerBuilder(unittest.TestCase):

    def setUp(self):
        self.builder = DockerBuilder(
            docker_hub_user='linyc74',
            github_repo='https://github.com/linyc74/qiime2_pipeline.git',
            mock=False)

    def test_build(self):
        self.builder.build()


class TestDockerWorker(unittest.TestCase):

    def setUp(self):
        self.worker = DockerWorker(
            image='ubuntu:20.04',
            mock=False)

    def test_run(self):
        self.worker.run(
            cmd=f'echo "Hello World"',
            mount=None)

    def test_run_mount_file(self):
        self.worker.run(
            cmd=f'ls {__file__}',
            mount=LocalFile(__file__)
        )

    def test_run_mount_dir(self):
        self.worker.run(
            cmd=f'ls /home',
            mount=LocalDir('/home')
        )

    def test_run_mount_file_dir(self):
        self.worker.run(
            cmd=f'ls {__file__} && ls /home',
            mount=[
                LocalFile(__file__),
                LocalDir('/home')
            ]
        )
