
# SSH-Login

RemoteLogin is a small script that is designed to facilitate SSH login to remote hosts via a ***YAML file***. If the SSH login is set up via SSH keys, it can be more efficient to search for the connection each time and enter it into the terminal.
## Features
To transfer X sessions over the SSH connection, the X option can be activated in the ***YAML file***.

## Installation

### Requirements
- Python 3.x
- python3-yaml

### Install dependencies
To run the program, the following Python modules are installed with `apt install` to make them available system-wide for a cron job:

```bash
apt-get update
apt install python3 python3-yaml
```

## Usage
Clone the project onto your Linux system  
```Bash
git clone https://github.com/itlinuxmaker/remoteLogin.git  
```
Change to the project directory and follow these steps:
1.   Navigate to the remoteLogin directory:
```Bash  
 cd remoteLogin/src/ 

```
2. Create the configuration directory:
 ```Bash  
 mkdir -p ~/Logins  
 ```
3. Copy the configuration and script files to their locations:
```
 cp ssh_login.yaml ~/Logins
 cp remoteLogin.py /usr/local/bin/
 ```
4. Edit the YAML configuration file to fit your ssh connections with your preferred text editor (vi, emacs, nano, etc.):
```
vi ~/Logins/ssh_login.yaml 
```
5. Run the backup script:
```
  python3 /usr/local/bin/remoteLogin.py
  ```

``
## License
The program is licensed under the GNU General Public License v3.0 or later in 2024.

## Disclaimer
IN NO EVENT WILL I BE LIABLE FOR ANY DAMAGES WHATSOEVER (INCLUDING, WITHOUT LIMITATION, THOSE RESULTING FROM LOST PROFITS, LOST DATA, LOST REVENUE OR BUSINESS INTERRUPTION) ARISING OUT OF THE USE, INABILITY TO USE, OR THE RESULTS OF USE OF, THIS PROGRAM. WITHOUT LIMITING THE FOREGOING, I SHALL NOT BE LIABLE FOR ANY SPECIAL, INDIRECT, INCIDENTAL, OR CONSEQUENTIAL DAMAGES THAT MAY RESULT FROM THE USE OF THIS SCRIPT OR ANY PORTION THEREOF WHETHER ARISING UNDER CONTRACT, NEGLIGENCE, TORT OR ANY OTHER LAW OR CAUSE OF ACTION. I WILL ALSO PROVIDE NO SUPPORT WHATSOEVER, OTHER THAN ACCEPTING FIXES AND UPDATING THE SCRIPT AS IS DEEMED NECESSARY.