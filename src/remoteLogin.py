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
    logins_dir = os.path.expanduser("~/Logins")
    
    if not os.path.exists(logins_dir):
        raise FileNotFoundError(
            "\033[0m\033[91mFehler: Das Verzeichnis 'Logins' im Home-Verzeichnis wurde nicht gefunden.\n\n"
            "Legen Sie die YAML-Datei bitte im Verzeichnis 'Logins' Ihres Home-Verzeichnis ab.\n\033[0m"
        )
    
    full_path = os.path.join(logins_dir, file_path)
    
    if not full_path.endswith(('.yaml', '.yml')):
        raise ValueError("\033[0m\033[91mNur Dateien mit den Endungen '.yaml' oder '.yml' werden als YAML-Dateien akzeptiert.\033[0m")
    
    try:
        with open(full_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"\033[0m\033[91mDie Datei '{file_path}' wurde nicht im Verzeichnis '{logins_dir}' gefunden.\033[0m")
    except yaml.YAMLError as e:
        raise ValueError(f"\033[0m\033[91mFehler beim Parsen der YAML-Datei: {e}\033[0m")

def display_menu(servers):
    print()
    print(f"\033[1m\033[38;5;214m{'==============================': <50}")
    print(f"{'SSH-Logins für folgende Server': >50}")
    print(f"{'==============================': >50}\033[0m")
    print()
    for i, server in enumerate(servers, start=1):
        print(f"\033[1m\033[94m{server['name']: <70} {i}\033[0m\n\033[38;5;214mStandort:\033[0m {'': <5}{server['location']}\n\033[38;5;214mBeschreibung:\033[0m {'': <1}{server['description']}")
        print()
    choice = int(input("\n\033[38;5;230mBitte wählen Sie eine Zahl für den SSH-Login: \033[0m"))
    print()
    return servers[choice - 1]

def ssh_login(server):

    command = ["ssh"]

    if server.get('x-option', 'no') == 'yes':
        command.append("-X")

    command.extend(["-p", server['port']])
    
    command.append(f"{server['user']}@{server['ip']}")

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"\033[0m\033[91mFehler beim Verbinden mit {server['name']}: {e}\033[0m")
    except KeyboardInterrupt:
        print()
        print("\033[0m\033[91m\nAbbruch durch Benutzer.\033[0m")
        print()

def info(name, ip, port):
    print()
    print(f"\033[1m\033[92mDie Verbindung zu '{name}' unter der IP-Adresse '{ip}' und dem SSH-Port '{port}' wird jetzt hergestellt.\033[0m")
    print()


def clear_console():
    """Clears the console output based on the operating system."""
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
        print("\n\033[1m\033[91mAbbruch durch Benutzer.\033[0m")
        print()
        sys.exit(0)
