import subprocess
import os
from colorama import Fore, Style # type: ignore
import sys
import pwd

# Custom messages
WARNING = Fore.LIGHTYELLOW_EX + "[Warning] " + Style.RESET_ALL
LOADING = Fore.LIGHTYELLOW_EX + "[Loading] " + Style.RESET_ALL
ERROR = Fore.LIGHTRED_EX + "[Error] " + Style.RESET_ALL
DONE = Fore.LIGHTGREEN_EX + "[Done] " + Style.RESET_ALL
INFO = Fore.LIGHTBLUE_EX + "[Info] " + Style.RESET_ALL
def message(mensagem, status=None):
    if status == LOADING:
        sys.stdout.write(f"\r{LOADING} {mensagem}")
        sys.stdout.flush()
    elif status == DONE:
        sys.stdout.write(f"\r{DONE} {mensagem} {Style.RESET_ALL}")
        sys.stdout.flush()
    elif status == ERROR:
        sys.stdout.write(f"\r{ERROR} {mensagem} {Style.RESET_ALL}")
        sys.stdout.flush()
    elif status == WARNING:
        sys.stdout.write(f"\r{WARNING} {mensagem} {Style.RESET_ALL}")
        sys.stdout.flush()
    elif status == INFO:
        sys.stdout.write(f"\r{INFO} {mensagem} {Style.RESET_ALL}")
        sys.stdout.flush()



# Check for root privileges
if os.geteuid() != 0:
    print(WARNING + "This file must be executed with sudo permissions!")
    print("          " + "The script will run 'sudo apt update' and install all dependencies ")
    print("          " + "necessary to configure the Kali Linux shell, as well as set up a new '.zshrc'.")
    print("")
    print("NOTE: Feel free to review the code and ensure that nothing harmful is being executed")
    exit()



#Banner
print("""
██╗  ██╗ █████╗ ██╗     ██╗     ███████╗███████╗██╗  ██╗
██║ ██╔╝██╔══██╗██║     ██║     ╚══███╔╝██╔════╝██║  ██║
█████╔╝ ███████║██║     ██║█████╗ ███╔╝ ███████╗███████║
██╔═██╗ ██╔══██║██║     ██║╚════╝███╔╝  ╚════██║██╔══██║
██║  ██╗██║  ██║███████╗██║     ███████╗███████║██║  ██║
╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝     ╚══════╝╚══════╝╚═╝  ╚═╝
""")



# Function to execute a command
def run_command(command, check=True, cwd=None):
    """
    Executes a command in the shell and provides warning and error messages without displaying the output to the user.

    Args:
        command (str): The command to be executed.
        check (bool): If True, raises an exception in case of error. Default is True.
        cwd (str, optional): Directory where the command will be executed. Default is None.

    Returns:
        bool: Returns True if the command was executed successfully, False otherwise.
    """
    try:
        result = subprocess.run(command, shell=True, cwd=cwd,
                                check=check, text=True, capture_output=True)
        return True

    except subprocess.CalledProcessError as e:
        message(ERROR + f"Error: The command '{command}' failed with exit code {e.returncode}.")
        return False

    except FileNotFoundError:
        message(ERROR + f"Error: The command '{command}' was not found.")
        return False

    except Exception as e:
        message(ERROR + f"Error: An issue occurred while executing the command '{command}'.")
        message(ERROR + f"Details: {str(e)}")
        return False



# Updating the system
command = "sudo apt update -y && sudo apt full-upgrade -y"
print(INFO + "We will run 'sudo apt update -y && sudo apt full-upgrade -y' to ensure the system is updated to install the dependencies")
message("Updating system", status=LOADING)
success = run_command(command)
if success:
    message("System successfully updated", status=DONE)
else:
    message("There was an error updating the system", status=ERROR)
    exit(1)
print("")
print("")


# Installing zsh, zsh-syntax-highlighting, zsh-autosuggestions
command2 = "sudo apt install -y zsh zsh-syntax-highlighting zsh-autosuggestions python3 python3-pip && pip install colorama --break-system-packages"
print(INFO + "We will install all dependencies")
message("Installing dependencies", status=LOADING)
success = run_command(command2)
if success:
    message("Dependencies successfully installed", status=DONE)
else:
    message("There was an error installing the dependencies", status=ERROR)
    exit(1)
print("")
print("")


# Moving .zshrc file to all user home directories
command3 = "cp .zshrc /root/ && cp .zshrc /home/*/"
print(INFO + "Copying '.zshrc' file to user home directories")
message("Copying .zshrc to user home directories", status=LOADING)
success = run_command(command3)
if success:
    message("Copied successfully", status=DONE)
else:
    message("There was an error copying to the directories", status=ERROR)
    exit(1)
print("")
print("")


#Move .zshrc file to user home directory
command4 = "rm .zshrc"
print(INFO + "Deleting original .zshrc file")
message("Erasing", status=LOADING)
success = run_command(command4)
if success:
    message("Deleted successfully", status=DONE)
else:
    message("There was an error deleting the file", status=ERROR)
    exit(1)
print("")
print("")


# Change default shell to Zsh
print(INFO + "Changing the default shell to Zsh")
command5 = "chsh -s $(which zsh)"
message("Changing the shell", status=LOADING)
success = run_command(command5)
if success:
    message("Default shell successfully changed", status=DONE)
else:
    message("There was an error changing the default shell", status=ERROR)
    exit(1)


# Notify the user to reload the Zsh configuration and restart the system
print("")
print("")
print(INFO + "Run 'zsh && source ~/.zshrc' to load the custom Zsh configuration")
print(WARNING + "It is recommended to restart the system to make sure all settings have been changed successfully")
