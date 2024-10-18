import yaml
import os
import sys
import subprocess

"""
remoteLogin
Version: 1.0.5
Author: Andreas Günther
License: GNU General Public License v3.0 or later
"""

def load_yaml_config(file_path):
    """
    Loads a YAML configuration file from the '~/Logins' directory.
    
    Args:
        file_path (str): The filename of the YAML file.

    Raises:
        FileNotFoundError: If the '~/Logins' directory or the specified file does not exist.
        ValueError: If the file is not a YAML file or there is an error parsing the file.

    Returns:
        dict: The loaded YAML data as a Python dictionary.
    """
    logins_dir = os.path.expanduser("~/Logins")
    
    if not os.path.exists(logins_dir):
        raise FileNotFoundError(
            "\033[0m\033[91mError: The directory 'Logins' in the home directory was not found.\n\n"
            "Please place the YAML file in the 'Logins' directory of your home directory.\n\033[0m"
        )
    
    full_path = os.path.join(logins_dir, file_path)
    
    if not full_path.endswith(('.yaml', '.yml')):
        raise ValueError("\033[0m\033[91mOnly files with the extension '.yaml' or '.yml' are accepted as YAML files.\033[0m")
    
    try:
        with open(full_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"\033[0m\033[91mThe file '{file_path}' was not found in the directory '{logins_dir}'.\033[0m")
    except yaml.YAMLError as e:
        raise ValueError(f"\033[0m\033[91mError parsing YAML file: {e}\033[0m")

def display_menu(servers):
    """
    Displays a menu for selecting a server.

    Args:
        servers (list): List of servers with their details stored in the YAML file.

    Returns:
        dict: The server dictionary selected by the user.

    Raises:
        ValueError: If the user input is not a valid number.
    """
    print()
    print(f"\033[1m\033[38;5;214m{'====================================': >50}")
    print(f"{'SSH logins for the following servers': >50}")
    print(f"{'====================================': >50}\033[0m")
    print()
    for i, server in enumerate(servers, start=1):
        print(f"\033[1m\033[94m{server['name']: <70} {i}\033[0m\n\033[38;5;214mLocation:\033[0m {'': <4}{server['location']}\n\033[38;5;214mDescription:\033[0m {'': <1}{server['description']}")
        print()
    choice = int(input("\n\033[38;5;230mPlease select a number for the SSH login: \033[0m"))
    print()
    return servers[choice - 1]

def ssh_login(server):
    """
    Establishes an SSH connection to a selected server.

    Args:
        server (dict): The server details, including 'name', 'ip', 'port', 'user' and 'x-option'.

    Raises:
        subprocess.CalledProcessError: If the SSH command fails.
        KeyboardInterrupt: When the user disconnects.
    """

    command = ["ssh"]

    if server.get('x-option', 'no') == 'yes':
        command.append("-X")

    command.extend(["-p", server['port']])
    
    command.append(f"{server['user']}@{server['ip']}")

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"\033[0m\033[91mError connecting to {server['name']}: {e}\033[0m")
    except KeyboardInterrupt:
        print()
        print("\033[0m\033[91m\nCancellation by user.\033[0m")
        print()

def info(name, ip, port):
    """
    Displays a message confirming that a connection to a specific server is being established.

    Args:
        name (str): The name of the SSH connection.
        ip (str): The IP address of the SSH connection.
        port (str): The SSH port of the SSH connection.
    """
    print()
    print(f"\033[1m\033[92mConnecting to '{name}' at IP address '{ip}' and SSH port '{port}' is now established.\033[0m")
    print()


def clear_console():
    """
    Clears the console based on the operating system.
    
    Works on both Linux/macOS (with 'clear') and Windows (with 'cls').
    """
    if os.name == 'posix':  
        os.system('clear')
    elif os.name == 'nt':  
        os.system('cls')

if __name__ == "__main__":
    clear_console()
    try:
        sys.tracebacklimit = 0
        config = load_yaml_config('ssh_login.yaml')
    except Exception as e:
        print(e)
        sys.exit(1)

    try:        
        server_choice = display_menu(config['login']['server'])
        info(server_choice['name'], server_choice['ip'], server_choice['port'])
        ssh_login(server_choice)
    except KeyboardInterrupt:
        print()
        print("\n\033[1m\033[91mCancellation by user.\033[0m")
        print()
        sys.exit(0)
