def build_pacote(operacao,numeroAtual,numeroTotal,payload=b''):
    pacote=b''
    pacote+=int.to_bytes(operacao, 1, 'big') # head 0 
    pacote+=int.to_bytes(numeroAtual, 1, 'big') # head 1
    pacote+=int.to_bytes(numeroTotal, 1, 'big') # head 2

    payload_size=int.to_bytes(len(payload), 1, 'big')
    
    pacote+=payload_size # head 3
    
    total=0
    for el in payload:
        total+=el
        
    checksum_array=int.to_bytes(total, 4,'big')
    pacote+=checksum_array # head 4,5,6,7
    print(checksum_array)
    pacote+=b'\x00\x00' #head 8,9
    
    pacote+=payload
    
    pacote+= b'\x45\x69\x45\x69' # EoP
    
    return pacote

if __name__ =="__main__":
    print(build_pacote(1,1,2,payload=b'\xFF\xFF'))
    
    