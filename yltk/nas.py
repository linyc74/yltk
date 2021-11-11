from typing import Union
from subprocess import check_call


class NAS:

    CIPHER = 'aes128-cbc'

    user: str
    ip: str
    port: Union[int, str]
    base_cmd: str

    def __init__(
            self,
            ip: str,
            port: Union[int, str],
            user: str,
            password_env_var: str):

        self.ip = ip
        self.port = port
        self.user = user
        self.base_cmd = f'sshpass -p ${{{password_env_var}}} scp -c {self.CIPHER} -P {self.port} -r'

    def download(self, src: str, dst: str):
        cmd = f'{self.base_cmd} {self.user}@{self.ip}:{src} {dst}'
        check_call(cmd, shell=True)

    def upload(self, src: str, dst: str):
        cmd = f'{self.base_cmd} {src} {self.user}@{self.ip}:{dst}'
        check_call(cmd, shell=True)
