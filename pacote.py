import time

def build_pacote(operacao,numeroAtual,numeroTotal,id,lastPackage,payload=b'', isWrongIndex=False, rightIndex=0):
    pacote = b''
    pacote += int.to_bytes(operacao, 1, 'big') # head 0
    pacote += b'\x00\x00' #head 1,2
    pacote += int.to_bytes(numeroTotal, 1, 'big') #head 3
    pacote += int.to_bytes(numeroAtual, 1, 'big') #head 4

    if operacao in [1,2]:
        pacote += int.to_bytes(id, 1, 'big') #head 5
    else:
        pacote += int.to_bytes(len(payload), 1, 'big') #head 5

    if isWrongIndex:
        pacote += int.to_bytes(rightIndex, 1, 'big') #head 6
    else:
        pacote += int.to_bytes(0, 1, 'big') #head 6

    pacote += int.to_bytes(lastPackage, 1, 'big') #head 7

    pacote += b'\x00\x00' #head 8,9

    pacote += payload

    pacote += b'\xAA\xBB\xCC\xDD' #eop

    return pacote

def check_data_header_client(package,ind,total):
    if package[0]!= 3 and package[0]!=4:
        return False
    if package[1] != ind:
        return False
    if package[2] != total:
        return 
    return True

def build_log(pacote,send): 
    """
    Cria uma linha de texto com o log de um pacote

    -pacote: pacote que o log ira descrever
    -send: bool que indica se esta sendo enviado ou nao
    -retorna o texto do log como string
    """ 
    log=''
    
    log+=time.strftime('%X %x / ')
    if type(pacote)==bool:
        log+='Timeout error'
    else:
        if send:
            log+='envio / '
        else:
            log+='receb / '
            
        log+= f'type {pacote[0]} / '
        
        log+= f'{len(pacote)} bytes / '
        
        if pacote[0]==3:
            log+=f'{pacote[4]} of '
            log+=f'{pacote[3]} / '
        
    log+='\n'
    return log
    
"""
if com1.rx.getIsEmpty() == False:
                rxBuffer, nrx = com1.getData(10)
                if rxBuffer[0] == 3:
                    payload_overflow = False
                    try:
                        payload, nRx = com1.getData(rxBuffer[5])
                        eop, nrx = com1.getData(4)
                    except:
                        payload_overflow = True
                    finally:
                        if eop != b'\xAA\xBB\xCC\xDD' or  payload_overflow or rxBuffer[4] != cont:
                            com1.sendData(build_pacote(6,cont,total_packages,serverNumber,cont-1,isWrongIndex=True,rightIndex=cont))
                        else:
                            com1.sendData(build_pacote(4,cont,total_packages,serverNumber,cont-1))
                            data += payload
                            cont += 1
"""


if __name__ =="__main__":
    print(build_pacote(3,1,2,payload=b'\xFF\xFF',id=69,lastPackage=0))
    print(build_log(build_pacote(3,1,2,payload=b'\xFF\xFF',id=69,lastPackage=0),True))
    
    