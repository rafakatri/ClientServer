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
from pacote import build_pacote,build_log, check_package

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM4"                  # Windows(variacao de)


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
        total_packages = None
        serverNumber=69
        log ='' 

        #time.sleep(20)

        while ocioso:
            if com1.rx.getIsEmpty() == False:
                rxBuffer, nRx = com1.getData(10)
                log += build_log(rxBuffer,False)
                eop,nrx = com1.getData(4) #TODO Revisars check de segurança do EOP
                log += build_log(eop,False)
                
                if rxBuffer[0] == 1 and rxBuffer[5] == 69 and eop ==b'\xAA\xBB\xCC\xDD': # if is request comunication start 
                    print("Handshake recebido")
                    total_packages = rxBuffer[3]
                    ocioso = False
                    time.sleep(1)
                    
        com1.sendData(build_pacote(2,1,total_packages,serverNumber,1)) # accept communication start
        log += build_log(build_pacote(2,1,total_packages,serverNumber,1),True)
        
        cont = 1 # was 'ind'
        com1.rx.clearBuffer()
        timer1 = time.time()
        timer2 = time.time()

        while cont <= total_packages:
            if com1.rx.getIsEmpty() == False:
                print("Pacote desejado: {}".format(cont))
                rxBuffer, nrx = com1.getData(10)
                log += build_log(rxBuffer,False)
                if rxBuffer[0] == 3:
                    payload_overflow = False
                    try:
                        payload, nRx = com1.getData(rxBuffer[5])
                        log += build_log(payload,False)
                        eop, nrx = com1.getData(4)
                        log += build_log(eop,False)
                    except:
                        payload_overflow = True
                    finally:
                        if eop != b'\xAA\xBB\xCC\xDD' or  payload_overflow or rxBuffer[4] != cont:
                            print(eop)
                            print(payload_overflow)
                            print(rxBuffer[4] != cont)
                            print(cont)
                            print("Pacote {} corrompido".format(cont))
                            com1.sendData(build_pacote(6,cont,total_packages,serverNumber,cont-1,isWrongIndex=True,rightIndex=cont))
                            log += build_log(build_pacote(6,cont,total_packages,serverNumber,cont-1,isWrongIndex=True,rightIndex=cont),True)
                        else:
                            print("Pacote {} recebido".format(cont))
                            com1.sendData(build_pacote(4,cont,total_packages,serverNumber,cont-1))
                            log += build_log(build_pacote(4,cont,total_packages,serverNumber,cont-1),True)
                            data += payload
                            cont += 1
                            timer1 = time.time()
                            timer2 = time.time()
                            continue
                com1.rx.clearBuffer()
            time.sleep(1)
            if time.time() - timer2 > 20:
                print("Timeout")
                com1.sendData(build_pacote(5,cont,total_packages,serverNumber,cont-1))
                log += build_log(build_pacote(5,cont,total_packages,serverNumber,cont-1),True)
                break
            if time.time() - timer1 > 2:
                print("Pacote {} reenviado".format(cont))
                com1.sendData(build_pacote(4,cont,total_packages,serverNumber,cont-1))
                log += build_log(build_pacote(4,cont,total_packages,serverNumber,cont-1),True)
                timer1 = time.time()
            else:
                continue
                

        with open('recebido.md','wb') as f:
            f.write(data)

        with open('log.txt','w') as f:
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
