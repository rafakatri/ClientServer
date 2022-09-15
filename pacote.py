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
    
    


if __name__ =="__main__":
    print(build_pacote(1,1,2,payload=b'\xFF\xFF'))
    
    