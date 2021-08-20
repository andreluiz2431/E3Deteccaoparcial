from socket import*
import argparse
import os
import hashlib

server = socket(AF_INET, SOCK_DGRAM)

parser = argparse.ArgumentParser(description='Argumentos')
parser.add_argument('-p', '--port',type=int, help = 'porta')
parser.add_argument('-i','--host',type = str, help= 'Ip')
parser.add_argument('-f','--nome_arq',type= str, help= 'Nome do arquivo de gravacao ' )
options = parser.parse_args()

host_andress = (options.host,options.port) # Armazena o host e a porta em uma variavel 
server.bind((host_andress)) # Abre o server

print('O servidor esta pronto!')
file_open = open(options.nome_arq,'a') # Abre o arquivo para escrita, passado pelo usuario

h = hashlib.md5()

#num = 3567  #numero de sequencia inicial
while True : # loop infinito

    message ,  clientAddress = server.recvfrom(1024) # Recebe a mensagem do transmissor

    if message == b'End' : # Faz comparacao se acabou o arquivo
        file_open.close() # Fecha arquivo de saída
        print('Fechamento do Server') 
        break

    else :
       
        envio = message.decode('utf-8').split(' ',2)
        num_seq = envio[0] #Recebe o numero de sequencia provinda do transmissor
        cod_veri = envio[1]#Recebe o codigo de verificação provinda do transmissor
        cargaUtil = envio[2]#Recebe a carga util provinda do transmissor

        h.update(str(num_seq).encode())
        numseq = h.hexdigest()


        if((numseq == cod_veri) ):#Verifica se o numero de sequencia e o codigo de verifcação condizem com o esperado
            server.sendto(str.encode('ACK'),clientAddress)#envia para o transmissor que tudo foi verificado e está OK
            server.sendto(str.encode('Frame gravado'),clientAddress) # Envia mensagem de confirmação de gravaçao do frame          
            file_open.write(cargaUtil) # Escreve a mensagem contida no frame no arquivo de saída

        else:   
            server.sendto(str.encode('NACK'),clientAddress) #Envia para o transmissor que houve um NACK
            server.sendto(str.encode('Erro na gravaçao'),clientAddress)    
        
    

server.close()