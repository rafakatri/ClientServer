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
from pacote import build_pacote

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"                  # Windows(variacao de)


def main():
    try:
        print("Iniciou o main")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Abriu a comunicação")

        print("esperando 1 byte de sacrifício")
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        print("Recebeu o byte de sacrifício")
        
        isHandshaken = False
        data = bytearray()
        ind = 0

        #time.sleep(20)

        while not isHandshaken:
            if com1.rx.getIsEmpty() == False:
                rxBuffer, nRx = com1.getData(10)
                if rxBuffer[0] == 0:
                    print("Handshake recebido")
                    isHandshaken = True
                    com1.sendData(build_pacote(1,1,1))
                com1.rx.clearBuffer()

        while True:
            if com1.rx.getIsEmpty() == False:
                rxBuffer, nRx = com1.getData(10)
                if rxBuffer[0] == 5:
                    payload, nRx = com1.getData(rxBuffer[3])
                    eop, nrx = com1.getData(4)
                    print(rxBuffer[3])
                    print(len(payload))
                    if eop == b'\x45\x69\x45\x69' and rxBuffer[1] == ind+1 and len(payload) == rxBuffer[3]:
                        data += payload
                        if rxBuffer[1] == rxBuffer[2]:
                            print("Recebeu todos os pacotes")
                            com1.sendData(build_pacote(4,rxBuffer[1],rxBuffer[2]))
                            break
                        else:
                            print(f"Recebeu pacote {ind+1}")
                            com1.sendData(build_pacote(3,rxBuffer[1],rxBuffer[2]))
                            ind += 1
                    else:
                        print("Erro no pacote")
                        if rxBuffer[1] != ind + 1:
                            com1.sendData(build_pacote(2,rxBuffer[1] -2,rxBuffer[2]))
                        else:
                            com1.sendData(build_pacote(2,rxBuffer[1] - 1,rxBuffer[2]))
                com1.rx.clearBuffer()

        with open("recebido.txt", "wb") as f:
            f.write(data)

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
