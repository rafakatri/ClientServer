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
serialName = "COM4"                  # Windows(variacao de)


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

        comandos = [b"\x00\xFA\x00\x00",b"\x00\x00\xFA\x00",b"\xFA\x00\x00",b"\x00\xFA\x00",b"\x00\x00\xFA",b"\x00\xFA",b"\xFA\x00",b"\xFA",b"\x00"]
        
        #txBuffer = Mensagem a ser enviada

        # Numero de comandos a ser utilizados
        length = random.randint(10,30)
        print(f"O numero de comandos sera {length}")

        # Byte startAll
        txBuffer = b"\xCC"

        for i in range(0,length):
            cmd = random.choice(comandos)
            txBuffer += cmd + b"\x45"
        
        # Byte endAll
        txBuffer += b"\xEE"

        print("meu array de bytes tem tamanho {}" .format(len(txBuffer)))
        print(f"Comandos: {txBuffer}")
            
        com1.sendData(np.asarray(txBuffer))  #as array apenas como boa pratica para casos de ter uma outra forma de dados
          
        while(com1.tx.getIsBussy()):
            pass
        txSize = com1.tx.getStatus()
        print('enviou = {}' .format(txSize))

        #Esperando confirmacao
        print("Esperando confirmacao")
        
        then = time.time()

        rxdata, nrx = com1.getData(len(int.to_bytes(length,byteorder='big',length=3)))

        deu_certo = False 

        while (time.time() - then < 5):
            if int.from_bytes(rxdata,byteorder='big') == length:
                print(f"A confirmacao demorou {time.time() - then}")
                print(f"O numero bateu")
                deu_certo = True
                break

        if not(deu_certo):
            if nrx > 0:
                print("Erro de servidor")
            else:
                print('Timeout')
    
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
