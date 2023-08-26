from ast import Str
from codecs import utf_8_decode
from numpy import byte
import serial
import serial.tools.list_ports
import time

# Variables
arduino=str
compt=0
delay_msr = 22


# Selection du port série _____________________________________________

ports = list( serial.tools.list_ports.comports())
for p in ports :
    print(p.description+'\n')

cp=(input("Indiquez le numéro du port série... "))

try :
    arduino = serial.Serial('COM'+cp, 9600, timeout=1)


except :
    print("Vérifier le port série utilisé")
    print("Port série déja utilisé")
    print("Arrêt du programme")

    for i in range(5):
        print((5-i), "...")
        time.sleep(1)
    exit()

print(arduino.is_open)


# Parametrage

name_file=str(input("Nom du fichier de sortie...")+'.txt')
mode = int(input('''
Mode de fonctionnement :
    1 >>> Automatique
    2 >>> Manuel
    ... '''))
while mode < 1 or mode > 2:
    mode = int(input('''
    Mode de fonctionnement :
        1 >>> Automatique
        2 >>> Manuel
        ... '''))

# Ecriture dans le TXT _____________________________________________
def write(L):
    
    try:
        file=open(name_file, 'a')
        
        file.write("Pin DP: "+L[0]+" V //Pin DM: "+L[1]+" V //I: "+L[2]+" A"+'\n')

        file.close()
        return print("txt OK")
    
    except:
        return print('Data vide...')


def req(code, delay, w):
    arduino.write(code.encode())
    print("Arduino code "+code+'\n')
    time.sleep(delay)

    res = arduino.readline().decode('utf').rstrip('\n'+'\r')

    if w == True:
        data = res.split("/")
        print(data)
        write(data)
        data.clear()
        res = ''
    else:
        return res



if mode == 1:
    while True:
        print("Mode auto activé"+'\n')
        req('1', delay_msr, True)
        


if mode == 2:
    line = req('2', 1, False)
    print(line)

    while True:
        R1 = float(input("Tension data + ... "))
        while R1 < 0 or R1 > 5:
            print("Tension accepté entre 0 et 5v")
            R1 = float(input("Tension data + ... "))

        R2 = float(input("Tension data - ... "))
        while R2 < 0 or R2 > 5:
            print("Tension accepté entre 0 et 5v")
            R2 = float(input("Tension data - ... "))

        r = req(str(R1), 2, False)
        print(r)
        if r == 'received':
            r = req(str(R2), 2, False)
            if r == 'received':
                print("R1 et R2 envoyées")
                req('2', delay_msr, True)

            else:
                print("Erreur envoi R2.value")        
        else:
            print("Erreur envoi R1.value")    
    



    
    