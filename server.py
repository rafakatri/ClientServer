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
from pacote import build_pacote,build_log

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
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Abriu a comunicação")

        print("esperando 1 byte de sacrifício")
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        print("Recebeu o byte de sacrifício")
        
        ocioso = True
        data = bytearray()
        end = False
        serverNumber=69 
        caso=1
        log=''

        #time.sleep(20)

        while ocioso:
            if com1.rx.getIsEmpty() == False:
                rxBuffer, nRx = com1.getData(10)
                eop,nrx = com1.getData(4) #TODO Revisars check de segurança do EOP
                
                if rxBuffer[0] == 1 and rxBuffer[5] == 69 and eop ==b'\xAA\xBB\xCC\xDD': # if is request comunication start 
                    print("Handshake recebido")
                    log+=build_log(rxBuffer+eop, False)
                    
                    ocioso = False
                    time.sleep(1)
                    
        com1.sendData(build_pacote(2,1,1)) # accept communication start
        log+=build_log(build_pacote(2,1,1), True)
        
        cont = 0 # was 'ind'
        com1.rx.clearBuffer()

        while not end:
            if com1.rx.getIsEmpty() == False:
                rxBuffer, nRx = com1.getData(10)
                if rxBuffer[0] == 3: # if is data transmission
                    numPckg = rxBuffer[3]
                    now2 = time.time()
                    now1 = time.time()
                    while time.time() - now2 < 20: # timer 2
                        while time.time() - now1 < 2:# timer 1
                            if com1.rx.getBufferLen() >= rxBuffer[3]: 
                                payload, nRx = com1.getData(rxBuffer[3])
                                eop, nrx = com1.getData(4)
                                log+=build_log(rxBuffer + payload + eop, False)
                                
                                print(eop)
                                print(cont+1)
                                print(rxBuffer[1])
                                if eop == b'\xAA\xBB\xCC\xDD' and rxBuffer[4] == cont+1 and len(payload) == rxBuffer[5]:
                                    data += payload
                                    if rxBuffer[4] == rxBuffer[3]:
                                        print("Recebeu todos os pacotes")
                                        com1.sendData(build_pacote(4,rxBuffer[1],rxBuffer[2])) #TODO id
                                        log+=build_log(build_pacote(4,rxBuffer[1],rxBuffer[2]),True)
                                        
                                        end = True
                                        break
                                    else:
                                        print(f"Recebeu pacote {cont+1}")
                                        com1.sendData(build_pacote(4,rxBuffer[1],rxBuffer[2])) # TODO id
                                        log+=build_log(build_pacote(4,rxBuffer[1],rxBuffer[2]), True)
                                        
                                        cont += 1
                                        break
                                else:
                                    print("Erro no pacote")
                                    if rxBuffer[4] != cont + 1:
                                        com1.sendData(build_pacote(6,rxBuffer[1] -2,rxBuffer[2]))
                                        log+=build_log(build_pacote(6,rxBuffer[1] -2,rxBuffer[2]),True)
                                        
                                    else:
                                        com1.sendData(build_pacote(6,rxBuffer[1] - 1,rxBuffer[2]))
                                        log+=build_log(build_pacote(6,rxBuffer[1] -1,rxBuffer[2]),True)
                                        
                                    
                        else:
                            com1.sendData(build_pacote(4,1,1))
                            log+=build_log(build_pacote(4,1,1), True)
                            
                            now1 = time.time()
                    else:
                        print("Timeout")
                        ocioso=True
                        
                        com1.sendData(build_pacote(5,rxBuffer[1] - 1,rxBuffer[2]))
                        log+=build_log(build_pacote(5,rxBuffer[1] - 1,rxBuffer[2]), True)
                        
                com1.rx.clearBuffer()
                time.sleep(1)

        with open("recebido.txt", "wb") as f:
            f.write(data)
        
        with open(f'client{caso}_log.txt','w') as f:
            f.write(log)

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
