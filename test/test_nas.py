import os
import unittest
from yltk.nas import NAS


class TestNAS(unittest.TestCase):

    def setUp(self):
        self.nas = NAS(
            ip=os.environ['YCL_NAS_1_IP'],
            port=os.environ['YCL_NAS_1_PORT'],
            user=os.environ['MY_NAS_USER'],
            password_env_var='MY_NAS_PASSWORD'
        )

    def __test_download(self):
        self.nas.download(src='~/Drive/Working/21_0515_deseq2', dst='./')

    def __test_upload(self):
        f = './temp.txt'
        open(f, 'w').close()
        self.nas.upload(src=f, dst='~/Drive')
        os.remove(f)
