#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import time
import numpy as np
import random
from pacote import *

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM5"                  # Windows(variacao de)


def main():
    try:
        print("Iniciou o main")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()

        # Envio do byte de sacrificio
        time.sleep(.2)
        com1.sendData(b'00')
        time.sleep(1)

        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Abriu a comunicação")
        
                     
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são um array bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.

        #txBuffer = Mensagem a ser enviada


        # Byte startAll
        txBuffer = bytearray()

        with open("datagrama.md", "rb") as f:
            txBuffer += f.read()

        print("meu array de bytes tem tamanho {}" .format(len(txBuffer)))
        
        # fragmentação da mensagem
        number_of_segments = (len(txBuffer)//114)
        segments = []
        # Segmentos de 114 bytes
        for i in range(number_of_segments):
            segments.append(txBuffer[i*114:(i+1)*114])
        # Segmento que sobra
        segments.append(txBuffer[number_of_segments*114:])
        print("O número de pacotes é {}" .format(len(segments)))

        cont = 1
        id = 69
        inicia = False
            
        while not inicia:
            com1.sendData(build_pacote(1,0,len(segments),id,0))
            then = time.time()
            while time.time() - then < 5:
                if not (com1.rx.getIsEmpty()):
                    rxBuffer, nrx = com1.getData(10)
                    if rxBuffer[0] == 2 and id == rxBuffer[5]:
                        inicia = True
                        break
        
        com1.rx.clearBuffer()
        timer1 = time.time()
        timer2 = time.time()
        timeout = False

        while cont <= len(segments) and not timeout:
            while time.time() - timer2 > 20:
                print("Timeout")
                com1.sendData(build_pacote(5,cont,len(segments),id,cont-1,payload=segments[cont-1]))
                timeout = True
                break
            else:
                while time.time() - timer1 > 5:
                    timer1 = time.time()
                else:
                    com1.sendData(build_pacote(3,cont,len(segments),id,cont-1,payload=segments[cont-1]))
                    if not com1.rx.getIsEmpty():
                        print('Pacote {} de {}' .format(cont, len(segments)))
                        print("Recebeu algo")
                        rxBuffer, nrx = com1.getData(10)
                        print(rxBuffer)
                        if rxBuffer[0] == 4:
                            print("Recebeu ACK")
                            cont += 1
                            timer1 = time.time()
                            timer2 = time.time()
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
             
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        
if __name__ == "__main__":
    main()
            