import subprocess

class SSHServer(object):

    def __init__(self, user: str, ip: str, port: int = 22):
        self._user = user
        self._ip = ip
        self._port = port

    def _cmd(self, command: str): return command.split(' ')

    def connect(self):
        print(f'Connection to {self._ip}:{self._port}...')
        try:
            subprocess.call(self._cmd(f'ssh {self._user}@{self._ip} -p {self._port}'))
        except KeyboardInterrupt:
            print('Exit...\nConnection interrupted.')