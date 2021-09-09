from typing import List, Union
import json
import os
from os.path import dirname, abspath, exists

from exceptions import ProfileNotFoundError

CONNS_FILE = dirname(abspath(__file__)) + '/conns.json'

def _load_json():
    if not exists(CONNS_FILE):
        print('Creating \'conns.json\' file...')
        with open(CONNS_FILE, 'w') as f:
            json.dump({'conns': {}}, f, indent = 4)
    with open(CONNS_FILE) as f:
        conns_file = json.load(f)
    return conns_file

def _cls():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

class SSHConnection(object):

    __slots__ = ('_conns_file', '_ip', '_username', '_passwd', '_port', 'profile',)

    def __init__(self, ip: str, username: str, passwd: str, port: int = 22):
        self._ip = ip
        self._username = username
        self._passwd = passwd
        self._port = port
        self._conns_file = _load_json()
        self.profile = self._check_profile()

    def _cmd(self, command: str) -> List[str]: 
        return command.split(' ')

    def _check_profile(self) -> Union[str, None]:
        """ Checks whether the current class configuration matches an existing profile. """

        current_config = {
            'ip': self._ip,
            'username': self._username,
            'passwd': self._passwd,
            'port': self._port
        }

        for k, v in self._conns_file['conns'].items():
            if v == current_config:
                return k

    def save(self, profile: str) -> None:
        """ Save the current SSH profile. """

        ip, username, passwd, port = self.credentials()

        if profile in self._conns_file['conns']:
            print(f'Editing \'{profile}\' profile to new configuration...')
        data = {
            'ip': ip,
            'username': username,
            'passwd': passwd,
            'port': port
        }
        self._conns_file['conns'][profile] = data
        with open(CONNS_FILE, 'w') as f:
            json.dump(self._conns_file, f, indent = 4)

        self.profile = profile

    def connect(self) -> None:
        """ Connect to SSH using paramiko. """

        import sys
        import traceback
        import paramiko
        try:
            import interactive
        except ImportError:
            from . import interactive

        ip, username, passwd, port = self.credentials()

        try:
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.WarningPolicy())
            print(f"Connecting to {username}@{ip}:{port}...")
            client.connect(ip, port, username, passwd)
            chan = client.invoke_shell()
            interactive.interactive_shell(chan)
            chan.close()
            client.close()
        except Exception as e:
            print("An error occured : %s: %s" % (e.__class__, e))
            traceback.print_exc()
            try:
                client.close()
            except:
                pass
            sys.exit(1)
    
    def credentials(self) -> tuple:
        """ ip, username, passwd, port = conn.credentials() """
        return (
            self._ip, 
            self._username, 
            self._passwd, 
            self._port
        )

    def get_ip(self) -> str: return self._ip

    def get_username(self) -> str: return self._username

    def get_passwd(self) -> str: return self._passwd

    def get_port(self) -> int: return self._port

    def get_profile(self) -> Union[str, None]: return self.profile

    def __repr__(self) -> str:
        return 'SSHConnection(\n' \
              f'    ip: {self._ip},\n' \
              f'    username: {self._username},\n' \
              f'    passwd: {self._passwd},\n' \
              f'    port: {self._port},\n' \
               ')'

    def __str__(self) -> str:
        return self.__repr__()

class SSHManager(object):

    __slots__ = ('_conns_file',)

    def __init__(self):
        self._conns_file = _load_json()

    def get(self, profile: str) -> SSHConnection:
        try:
            profile = self._conns_file['conns'][profile]
        except TypeError:
            raise ProfileNotFoundError(f'Profile \'{profile}\' was not found.')
        return SSHConnection(
            profile['ip'], 
            profile['username'],
            profile['passwd'],
            profile['port']
        )

    def delete(self, profile: str) -> None:
        try:
            self._conns_file['conns'][profile]
        except TypeError:
            raise ProfileNotFoundError(f'Profile \'{profile}\' was not found.')
        self._conns_file['conns'].pop(profile)
        with open(CONNS_FILE, 'w') as f:
            json.dump(self._conns_file, f, indent = 4)

    def profiles(self) -> List[SSHConnection]:
        json_profiles = self._conns_file['conns']
        profiles = [SSHConnection(
            json_profiles[profile]['ip'],
            json_profiles[profile]['username'],
            json_profiles[profile]['passwd'],
            json_profiles[profile]['port']
        ) for profile in json_profiles]
        return profiles

    def interactive_conn(self) -> None:
        profiles = self.profiles()
        choices = ''
        for i, profile in enumerate(profiles):
            choices += f'   [{i + 1}] {profile.profile} : {profile.get_username()}@{profile.get_ip()}:{profile.get_port()}\n'
        if not choices:
            choices = '    No profile created.\n'
        try:
            index = int(input(f"\nChoose a profile :\n{choices}\n")) - 1
        except KeyboardInterrupt:
            exit()
        _cls()
        profiles[index].connect()
    
    def __repr__(self) -> str:
        profiles = ', '.join(self.profiles())
        return f'ConnectionManager({profiles})'

    def __str__(self) -> str:
        return self.__repr__()

if __name__ == '__main__':
    SSHManager().interactive_conn()