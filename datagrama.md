byte0 -> tipo de operação
- 1: request comunication start (payload=0);
- 2: accept communication start (payload=0);
- 3: data transmission;
- 4: request next package (payload=0);
- 5: Time-out
- 6: package error (payload=0);


byte1 -> Livre

byte2 -> Livre

byte3 ->  número total de pacotes do arquivo

byte4 ->  número do pacote sendo enviado 

byte5 -> se tipo for handshake: id do arquivo (crie um) 
se tipo for dados: tamanho do payload
 
byte6 -> pacote solicitado para recomeço quando há erro no envio

byte7 -> último pacote recebido com sucesso.

byte8 -> CRC

byte9 -> CRC

payload -> (b'\x??')*(0-114)

EOP -> b'\xAA\xBB\xCC\xDD'