from ast import Str
from codecs import utf_8_decode
from numpy import byte
import serial
import serial.tools.list_ports
from datetime import datetime
import time

# Variables
rawData=[]
arduino=str
compt=0
coef = 1.01905

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
inter=int(input("Inteval des mesures en seconde (min 2sec)..."))
while inter < 2:
    print("Mesures impossible...")
    inter=float(input("Inteval des mesures en seconde (min 2sec)..."))


# Ecriture dans le TXT _____________________________________________
def write(L): 
    D = datetime.now()
    N = str(datetime.now())
    H = str(D.hour).zfill(2)
    M = str(D.minute).zfill(2)
    S = str(D.second).zfill(2)
    
    if compt == 0:
        file=open(name_file, 'x')
        file.write('Analyse intensite de charge'+'\n')
        file.write('Chargeur 220v -- Partage de connexion active'+'\n')
        file.write('Debut des mesures :     '+ N +' Charge: 3%'+'\n')
        file.close()
        
    for i in range(len(L)):
        file=open(name_file, 'a')
        file.write(L[i]+' A / '+H+':'+M+':'+S+' / '+ str(compt).zfill(7) +' s'+'\n')
    file.close()
    return print("txt OK")


# Demande & Recupération des valeurs _____________________________________________
def py_to_ard():
    arduino.write('1'.encode())
    rawData.append(str(arduino.readline().decode('utf').rstrip('\n'+'\r')))
    print(rawData)
    write(rawData)
    rawData.clear()

# Boucle infinie _____________________________________________
while True:
    py_to_ard()
    delay = inter - coef
    time.sleep(delay)
    compt=(compt+inter)
    
    





