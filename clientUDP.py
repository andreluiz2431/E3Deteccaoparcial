import socket # importando socket
import sys # importando sys para receber por parametros

from  time import sleep # importar bib para tempo de espera

params = sys.argv[1:] # definindo variável igual aos parâmetros

print("\nInicializando socket...")
socketClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("\nSocket inicializado.")

if(len(sys.argv) > 1):
    # Criando HELP da aplicação
    if(params[0] == "--help" or params[0] == "-h"):
        print("Execucao do cliente: python3 <nomeArquivo.py> <entradaDadosArquivo> <tamanhoQuadros> <ip> <porta>")
        print("-------------------- Ex: python3 clientUDP.py enviar.txt 7 127.0.0.1 12000 --------------------")
    
    else:
        nameArqSend = params[0] # definindo variável para o primeiro parâmetro
        
        print("\nLendo arquivo...")
        arqSend = open(nameArqSend, 'r') # ler aquivo para enviar dados e definir na variavel
        print("\nArquivo lido.")
        
        tamQuadros = int(params[1]) # definindo variável para o parâmetro de tamanho de quadros
        
        serverName = params[2] # definindo variável para o parâmetro de ip
        
        serverPort = int(params[3]) # definindo variável para o parâmetro da porta

        for linha in arqSend:
            i = 0
            while(i < len(linha) - 1):
                message = linha[i:(i+tamQuadros)] # particionando mensagerm para envio
                
                #----------- Cod de espera -----------
                for contagem in range(0,2): # repetição de 2X para a suspenção
                    print("Aguarde...")
                    sleep(1) # função para suspender cod por determinado tempo

                print('Olá!')
                #-------------------------------------

                
                print("Pacote enviado: ", message)
                message = str.encode(message) # definindo mensagem para envio
                i = (i + tamQuadros)

                socketClient.sendto(message, (serverName, serverPort)) # enviando mensagem para o servidor

        message = str.encode("@!@") # definindo mensagem de confirmação de dados enviados
        
        socketClient.sendto(message, (serverName, serverPort)) # enviando mensagem de confirmação para o servidor

        print("\nAplicação finalizada.")
        arqSend.close() # fechando arquivo
        socketClient.close() # finalizando socket