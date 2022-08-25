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

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM11"                  # Windows(variacao de)


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

        startAll = b"\xCC"
        endAll = b"\xEE"
        sep = b"\x45"

        while True:
            data = com1.rx.buffer
            if startAll in data and endAll in data:
                break

        firstInd = data.find(b"\xCC")
        lastInd = data.find(b"\xEE")
        data = data[firstInd+1:lastInd]
        data = data.split(sep)

        print(f'Recebeu {len(data)} comandos')
        print(data)    
      
        #acesso aos bytes recebidos
        #txLen = len(txBuffer)
        #rxBuffer, nRx = com1.getData(txLen)
        #print("recebeu {} bytes" .format(len(rxBuffer)))
        
        #for i in range(len(rxBuffer)):
        #    print("recebeu {}" .format(rxBuffer[i]))
            
    
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
