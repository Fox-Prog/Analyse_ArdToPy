import serial
import serial.tools.list_ports
import time
import mysql.connector
import datetime

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'ard_to_py'
}


def create_table(table_name):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        create_table_query = f"""
            CREATE TABLE {table_name} (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                current FLOAT,
                hour DATETIME
            )
        """
        cursor.execute(create_table_query)
        print("Table "+table_name+" created")
    
    except mysql.connector.Error as err:
        print("Une erreur MySQL s'est produite:", err)

    finally:
        try:
            cursor.close()
            conn.close()
        except: pass

def replace_table(table_name):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(f"DROP TABLE {table_name}")
        print("Table "+ table_name +" drop"+'\n')
                
    except mysql.connector.Error as err:
        print("Une erreur MySQL s'est produite:", err)

    finally:
        try:
            cursor.close()
            conn.close()
        except: pass
    
    create_table(table_name)


def print_dbb(arduino, table_name, data, hour):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = "INSERT INTO {} (current, hour) VALUES (%s, %s)".format(table_name)
        value = (data, hour)
        cursor.execute(query, value)
        conn.commit()
        print("Data INSERT INTO "+table_name+'\n')
                
    except mysql.connector.Error as err :
        print("Erreur MySQL... Reprise de la mesure...", err)

    finally:
        try:
            cursor.close()
            conn.close()
        except: pass
        
        mesure(arduino, table_name)


def mesure(arduino, table_name):

    time.sleep(1)
    arduino.write('1'.encode())
    data = (str(arduino.readline().decode('utf').rstrip('\n'+'\r')))     

    data_bdd = float(data.strip())
    current_time = datetime.datetime.now()
    print('Data received: '+ str(data_bdd))
    print_dbb(arduino, table_name, data_bdd, current_time)


def main():
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

    table_name = input("Nom de la table SQL... ")

    try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
            table_exists = cursor.fetchone()

    except mysql.connector.Error as err:
        print("Une erreur MySQL s'est produite:", err)

    finally:
        if conn is not None and conn.is_connected():
            cursor.close()
            conn.close()


    if(table_exists):
        replace = input("Table déjà existante, Y pour remplacer... ")
        if (replace == 'Y' or replace == 'y'):
            replace_table(table_name)
        else: exit(table_name)

    else:
        create_table(table_name)


    mesure(arduino, table_name)
    




if __name__ == '__main__':
    main()