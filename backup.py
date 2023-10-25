import paramiko
import os
from datetime import datetime
import getpass
import time
import pandas as pd

# Reset
Color_Off="\033[0m"       # Text Reset

# Regular Colors
Black="\033[0;30m"        # Black
Red="\033[0;31m"          # Red
Green="\033[0;32m"        # Green
Yellow="\033[0;33m"       # Yellow
Blue="\033[0;34m"         # Blue
Purple="\033[0;35m"       # Purple
Cyan="\033[0;36m"         # Cyan
White="\033[0;37m"        # White

# Bold
BBlack="\033[1;30m"       # Black
BRed="\033[1;31m"         # Red
BGreen="\033[1;32m"       # Green
BYellow="\033[1;33m"      # Yellow
BBlue="\033[1;34m"        # Blue
BPurple="\033[1;35m"      # Purple
BCyan="\033[1;36m"        # Cyan
BWhite="\033[1;37m"       # White

# Underline
UBlack="\033[4;30m"       # Black
URed="\033[4;31m"         # Red
UGreen="\033[4;32m"       # Green
UYellow="\033[4;33m"      # Yellow
UBlue="\033[4;34m"        # Blue
UPurple="\033[4;35m"      # Purple
UCyan="\033[4;36m"        # Cyan
UWhite="\033[4;37m"       # White

# Background
On_Black="\033[40m"       # Black
On_Red="\033[41m"         # Red
On_Green="\033[42m"       # Green
On_Yellow="\033[43m"      # Yellow
On_Blue="\033[44m"        # Blue
On_Purple="\033[45m"      # Purple
On_Cyan="\033[46m"        # Cyan
On_White="\033[47m"       # White

# High Intensty
IBlack="\033[0;90m"       # Black
IRed="\033[0;91m"         # Red
IGreen="\033[0;92m"       # Green
IYellow="\033[0;93m"      # Yellow
IBlue="\033[0;94m"        # Blue
IPurple="\033[0;95m"      # Purple
ICyan="\033[0;96m"        # Cyan
IWhite="\033[0;97m"       # White

# Bold High Intensty
BIBlack="\033[1;90m"      # Black
BIRed="\033[1;91m"        # Red
BIGreen="\033[1;92m"      # Green
BIYellow="\033[1;93m"     # Yellow
BIBlue="\033[1;94m"       # Blue
BIPurple="\033[1;95m"     # Purple
BICyan="\033[1;96m"       # Cyan
BIWhite="\033[1;97m"      # White

# High Intensty backgrounds
On_IBlack="\033[0;100m"   # Black
On_IRed="\033[0;101m"     # Red
On_IGreen="\033[0;102m"   # Green
On_IYellow="\033[0;103m"  # Yellow
On_IBlue="\033[0;104m"    # Blue
On_IPurple="\033[10;95m"  # Purple
On_ICyan="\033[0;106m"    # Cyan
On_IWhite="\033[0;107m"   # White
df = pd.read_csv("ips.txt", sep=",", header=None)
total_equipamentos = df[df.columns[0]].count() # quantidade de linhas ou de equipamentos
total_feitos = 0
conta_erros = 0
contador = 0
#conta_erros = ""
os.system('cls')
# tot = os.path.getsize("ips.txt")
mensagens = []  # Inicialize uma lista para armazenar as mensagens

comentarios = ""
def tela():
    print(BBlue + " ")
    print("    ____             _  ")
    print("   |  _ \           | | ")
    print("   | |_) | __ _  ___| | ___   _ _ __    ")
    print("   |  _ < / _` |/ __| |/ / | | | '_ \   ")
    print("   | |_) | (_| | (__|   <| |_| | |_) |  ")
    print("   |____/ \__,_|\___|_|\_\\__,__| .__/   ")
    print("                               | |      ")
    print(BYellow + "   Desenvolvido por Abimael" + BBlue + "    |_|     \n")
    print(Color_Off+"   Realizados....:", total_feitos)
    print("   Faltam........:", total_equipamentos)
    if conta_erros == 0:
        print("   Erros.........:")
    else:
        print(Color_Off + "   Erros.........:"+ Red ,conta_erros,  Color_Off)
    print(BYellow + "   ========================================================================" + Color_Off)
    print("\n".join(mensagens))
    print(BYellow + "   ========================================================================" + Color_Off)

#função para tela
tela()
# Formate a data atual
current_date = datetime.now().strftime("%Y-%m-%d")

# Crie o nome da pasta com a data atual
backup_folder = current_date
os.makedirs(backup_folder, exist_ok=True)


# Função para realizar o backup
def backup_switch(ip, port, model, username, password):
    global contador
    contador += 1
    if contador >= 10:
        mensagens.clear() # Limpe a lista
        contador = 0

    # Formate a data atual
    current_date = datetime.now().strftime("%Y-%m-%d__%H-%M-%S")

    # Crie o nome do arquivo de backup
    backup_filename = f"{backup_folder}/{ip}___{current_date}.txt"

    # Inicialize a variável ssh_session
    ssh_session = None

    # Crie uma conexão SSH
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        #client.connect(ip, username=username, password=password)
        client.connect(ip, port=port, username=username, password=password)

        # Abra uma sessão SSH
        ssh_session = client.invoke_shell()

        if model == 'cisco':
            # Entre no modo de execução privilegiado (enable)
            ssh_session.send("enable\n")
            ssh_session.send("\n")
            ssh_session.send("terminal length 0\n")
            ssh_session.send("show running-config\n")
            ssh_session.send("\n")
            ssh_session.send("\n")
        elif model == '3com':
            ssh_session.send("\n")
            ssh_session.send("xxx\n")
            ssh_session.send("\n")
            ssh_session.send("\n")
            ssh_session.send("screen-length disable\n")
            ssh_session.send("display current-configuration\n")
            ssh_session.send("\n")
            ssh_session.send("\n")

        # Aguarde a saída
        time.sleep(30)

        # output = commands.recv(1000000)
        # output = ssh_session.recv(65535).decode()
        output = ssh_session.recv(1000000).decode(errors='ignore')

        # Salve o backup em um arquivo
        # with open(backup_filename, 'w') as backup_file:
        with open(backup_filename, 'w', encoding='utf-8', errors='ignore') as backup_file:
            backup_file.write(output)

        comentarios = '   ['+ BIGreen + '+' + Color_Off + '] ' + ip + ':22 - Backup executado com sucesso'
        mensagens.append(comentarios)
        grava_log("exito.txt", ip, model, user, port)

    except paramiko.ssh_exception.AuthenticationException:
        comentarios = '   ['+ BIRed + '-' + Color_Off + '] ' + ip + ':22 - Autenticação falhou'
        mensagens.append(comentarios)
        grava_log("err_auth.txt", ip, model, user, port)

    except paramiko.ssh_exception.NoValidConnectionsError:
        comentarios = '   ['+ BIRed + '-' + Color_Off + '] ' + ip + ':22 - Nenhuma conexão válida'
        mensagens.append(comentarios)
        grava_log("err_sem_conexao.txt", ip, model, user, port)

    except Exception as e:
        global conta_erros  # Indica que estamos usando a variável global
        conta_erros += 1
        comentarios = '   ['+ BIRed + '-' + Color_Off + '] ' + ip + ':22 - Não foipossivel excutar comandos em ' + ip + ':22'
        mensagens.append(comentarios)
        grava_log("err_outros.txt", ip, model, user, port)


    finally:
        if ssh_session:
            # Feche a conexão SSH apenas se estiver inicializada.
            #print(f'[+] {ip}:22 - Backup executado com sucesso')
            ssh_session.close()
        client.close()

def grava_log(nome_arq, ip, model, user, port):
    #global conta_erros  # Indica que estamos usando a variável global
    global total_feitos
    global total_equipamentos

    total_feitos += 1
    total_equipamentos -= 1

    arq = open(backup_folder + '/' + nome_arq, 'a')
    arq.write(ip + "," + model + "," + user + "," + port +"\n")
    arq.close()

    os.system('cls')
    tela()


os.system('cls')
tela()
#print('=' * 115 + '\n')
# Ler os IPs e modelos a partir do arquivo ips.txt
with open("ips.txt", "r") as file:
    for line in file:
        parts = line.strip().split(",")
        if len(parts) == 4:
            ip, model, user, port = [p.strip() for p in parts]  # Remova espaços em branco
            #print(switch_auth(user))
            if user == '0':
                username = 'user'
                password = '********'
            elif user == '1':
                username = 'admin'
                password = '********'
            elif user == '2':
                username = 'grulocal'
                password = '********'
            elif user == '3':
                username = 'admin'
                password = '********'
            elif user == '4':
                username = 'admin'
                password = '********'
            elif user == '5':
                username = 'admin'
                password = '********'

            backup_switch(ip, port, model, username, password)
        else:
            print(f"   Formato inválido na linha: {line}")
