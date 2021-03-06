from socket import*
import argparse
import os
import hashlib
import time

i=0
seq_int =1
client = socket(AF_INET,SOCK_DGRAM)

parser = argparse.ArgumentParser('Argumentos')
parser.add_argument('-f','--nome_arq',type= str, help= 'Nome do arquivo' )
parser.add_argument('-p', '--port',type=int, help = 'porta')
parser.add_argument('-i','--host',type = str , help= 'Ip')
parser.add_argument('-q', '--frame',type = int, help='Tamanho dos quadros')
options = parser.parse_args()
host_andress = (options.host,options.port) # Armazena o host e a porta em uma variavel 

frames = options.frame 
name_file = options.nome_arq
file_open = open(options.nome_arq, 'rb') # Abre o arquivo para leitura, passado pelo usuario

file_size = os.path.getsize(options.nome_arq) # Pega o tamanho do arquivo
div =  (file_size // frames) # Divide o tamanho do arquivo pelos frames
 

h = hashlib.md5()
client.settimeout(1)    #
for i in range(div+1) :
 
    h.update(str(seq_int).encode())
    cod = h.hexdigest() # Transforma o codiog em hash
 
    cargaUtil = file_open.read(frames) # Lê o frame do arquivo
    envio  = str(seq_int) + ' ' + cod + ' ' + "{}".format(cargaUtil.decode('utf-8'))   

    if(client.sendto(envio.encode(),(host_andress))) : # Envia a o frame jundo com o numero sequecial e o codigo para o receptor
          
        try :
    
            request, clientAddress = client.recvfrom(1024)#Recebe confirmação de envio
           
            if(request == b'ACK') :
                print(request.decode('utf-8')) # Printa ACK
                print("Frame Gravado")
                            
            elif(request == b'NACK') :
                print(request.decode('utf-8')) # Printa NACK
                print("Recording error | Frame  < "+str(seq_int)+" >") # Printa em qual frame deu erro
            
        except:
            print("ERRO Timeout - CLOSE") # Printa se excedeu o tempo e fecha e para de enviar os frames
            break
           
    
    seq_int +=1 #Incrementa o numero da sequencia
   
    
close_file = 'End'
client.sendto(close_file.encode(),(host_andress)) # Envia uma mensagem de fim
file_open.close() # Fecha o arquivo
client.close() # Fecha o transmissor