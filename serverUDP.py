import socket # importando socket
import sys # importando sys para receber por parametros

params = sys.argv[1:] # definindo variável igual aos parâmetros

if(len(sys.argv) > 1):
    # Criando HELP da aplicação
    if(params[0] == "--help" or params[0] == "-h"):
        print("Execucao do servidor: python3 <nomeArquivo.py> <porta> <nomeArquivoSaida>")
        print("--------------- Ex: python3 serverUDP.py 12000 saida.txt ---------------")
    
    else:
        serverPort = int(params[0]) # definindo variável para o parâmetro da porta
        
        nameArqSave = params[1] # definindo variável para o parâmetro que recebe nome do arquivo para salvar
        
        arqSave = open(nameArqSave, 'w') # sinaliza para escrever no aquivo para salvar dados e definir na variavel

        socketServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # inicializando socket UDP
        
        socketServer.bind(('', serverPort)) # recebendo conecção do socket

        print('Servidor ligado...')

        while 1:
            message, clientAddress = socketServer.recvfrom(2048) # recebendo mensagens do cliente

            # se receber mensagem de confirmação do cliente que os dados foram enviados
            if(message == b'@!@'):
                print("Dados recebidos.")
                arqSave.close() # fechando arquivo
            else:
                message = message.decode("utf-8") # lendo mensagem recebida
                print("Pacote recebido: ", message)
                arqSave.writelines(message) # escrevendo no arquivo a mensagem recebida pelo cliente