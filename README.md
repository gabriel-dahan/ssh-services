# TextConverter

### Install and Import the module :

Installing the module :
```bash
~ git clone https://github.com/gabriel-dahan/ssh-services/
~ cd sshservices/

# Linux / MacOS
~ python3 -m pip install -U .

# Windows 
~ py -3 -m pip install -U .
```
_Consider using the `--user` parameter if you're not a root/admin user._

Importing the module :
```python
import sshservices
```
### Create an SSH connection.
```python
from sshservices import SSHConnection

ssh_conn = SSHConnection(
    '0.0.0.0', # IPv4
    'testuser', # Username
    'Testing1234', # Password
    22 # Port (default: 22)
)

ssh_conn.connect() # Launches a connection to the specified server.
```
### Save and Delete an SSH connection.
#### Save
```python
from sshservices import SSHConnection, SSHManager

ssh_conn = SSHConnection(...)
ssh_conn.save('MySSHConnection') # Save the profile with a name (don't reuse the same name as others profiles, it'll override them).

# Later
sshm = SSHManager()

sshm.get('MySSHConnection').connect() # Connect to a specific profile.
sshm.interactive_conn() # Prompt a list of the profiles and let the user choose one.
```
#### Delete
```python
sshm = SSHManager()
sshm.delete('MySSHConnection')
```
### Get all profiles.
```python
sshm = SSHManager()
sshm.profiles() # --> Returns a list of all the profiles.
```