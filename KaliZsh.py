import subprocess
import os
from colorama import Fore, Style # type: ignore
import sys

#Messagens costumizadas
AVISO = Fore.LIGHTYELLOW_EX + "[Warning] " + Style.RESET_ALL
CARREGANDO = Fore.LIGHTYELLOW_EX + "[Loading] " + Style.RESET_ALL
FALHA = Fore.LIGHTRED_EX + "[Error] " + Style.RESET_ALL
TERMINO = Fore.LIGHTGREEN_EX + "[Done] " + Style.RESET_ALL
INFORMATIVO = Fore.LIGHTBLUE_EX + "[Info] " + Style.RESET_ALL
def message(mensagem, status=None):
    if status == CARREGANDO:
        sys.stdout.write(f"\r{CARREGANDO} {mensagem}")
        sys.stdout.flush()
    elif status == TERMINO:
        sys.stdout.write(f"\r{TERMINO} {mensagem} {Style.RESET_ALL}")
        sys.stdout.flush()
    elif status == FALHA:
        sys.stdout.write(f"\r{FALHA} {mensagem} {Style.RESET_ALL}")
        sys.stdout.flush()
    elif status == AVISO:
        sys.stdout.write(f"\r{AVISO} {mensagem} {Style.RESET_ALL}")
        sys.stdout.flush()

#Verificar root
if os.geteuid() != 0:
    print(AVISO + "Esse arquivo preciso ser executado com permissões sudo!")
    print("          " + "O script irá efetuar um 'sudo apt update' e instalar todas as dependências ")
    print("          " + "necessárias para configurar o shell do Kali Linux, além de configurar um novo '.zshrc'.")
    print("")
    print("OBS: Fique a vontade para revisar o codigo e ter certeza de que nada de errado esta sendo executado")
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


#Função executar comando
def run_command(command, check=True, cwd=None):
    """
    Executa um comando no shell e fornece mensagens de aviso e erro sem exibir a saída para o usuário.

    Args:
        command (str): O comando a ser executado.
        check (bool): Se True, levanta uma exceção em caso de erro. Padrão é True.
        cwd (str, opcional): Diretório onde o comando será executado. Padrão é None.

    Returns:
        bool: Retorna True se o comando for executado com sucesso, False caso contrário.
    """
    try:
        result = subprocess.run(command, shell=True, cwd=cwd,
                                check=check, text=True, capture_output=True)

        # Opcional: se você quiser logar a saída padrão ou fazer algo com ela, pode usar result.stdout
        return True

    except subprocess.CalledProcessError as e:
        # Mensagem de erro
        message(FALHA + f"Erro: O comando '{command}' falhou com o código de saída {e.returncode}.")
        return False

    except FileNotFoundError:
        # Mensagem de erro para comando não encontrado
        message(FALHA + f"Erro: O comando '{command}' não foi encontrado.")
        return False

    except Exception as e:
        # Mensagem de erro para outros problemas
        message(FALHA + f"Erro: Ocorreu um problema ao executar o comando '{command}'.")
        message(FALHA + f"Detalhes: {str(e)}")
        return False

#Atualizando sistema
command = "sudo apt update -y && sudo apt full-upgrade -y"
print("")
print(INFORMATIVO + "Iremos executar 'sudo apt update -y && sudo apt full-upgrade -y' para ter certeza que o sistema está atualizado para instalar as dependências")
message("Executando 'sudo apt update -y && sudo apt full-upgrade -y'", status=CARREGANDO)
success = run_command(command)
if success:
    message("Comando executado com sucesso", status=TERMINO)
else:
    message("Houve um erro ao executar o comando", status=FALHA)
    exit(1)

#Instalando zsh, zsh-syntax-highlighting, zsh-autosuggestions
command2 = "sudo apt install -y zsh zsh-syntax-highlighting zsh-autosuggestions"
print("")
print(INFORMATIVO + "Iremos instalar o zsh e baixar os plugins zsh-syntax-highlighting e zsh-autosuggestions")
message("Instalando zsh e configurando os plugins", status=CARREGANDO)
success = run_command(command2)
if success:
    message("Comando executado com sucesso", status=TERMINO)
else:
    message("Houve um erro ao executar o comando", status=FALHA)
    exit(1)

# Alterar o shell padrão para Zsh
print("")
print(INFORMATIVO + "Alterando o shell padrão para Zsh")
command4 = "chsh -s $(which zsh)"
message("Executando alteração do shell", status=CARREGANDO)
success = run_command(command4)
if success:
    message("Comando executado com sucesso", status=TERMINO)
else:
    message("Houve um erro ao executar o comando", status=FALHA)
    exit(1)

print("")
print(INFORMATIVO + "Execute 'zsh && source ~/.zshrc' para carregar o zsh costumizado")

print("")
print(AVISO + "É recomendado reiniciar o sistema para ter certeza de que todas as configurações foram alteradas com sucesso")