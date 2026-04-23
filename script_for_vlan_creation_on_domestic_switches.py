import os
import sys
import yaml
from dotenv import load_dotenv
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException, SSHException
from datetime import datetime


""" El siguiente script tiene el propósito de crear VLANs en los switches domésticos de cada una de las zonas de la empresa Domus Nova. 
    El nombre e ID de la VLAN se declaran antes de usar el script en las variables globales. Este se encargará automáticamente de verificar si existe una VLAN con el nombre deseado,
    si el ID está en uso, o de crear la VLAN solicitada.
    Por convención, las VLANs serán creadas siempre con nombres en mayúsculas.
    Los dispositivos a los que se conectará el script, así como sus credenciales, se encuentran definidos en un archivo de inventario en formato YAML. Las contraseñas y secrets de cada dispositivo se almacenan en un archivo .env, y el script se encarga de buscarlos automáticamente para establecer la conexión SSH.
    El programa también realizará un backup automático de la configuración actual de cada dispositivo, especificando fecha y hora, y que se almacenará en el mismo directorio donde se ejecuta el script.
    Finalmente, guardará la configuración luego de crear la VLAN.

    Este script ha sido testeado en dispositivos Cisco. Ajustarlo a otras marcas dependerá en gran medida de la sintaxis necesaria y la compatibilidad de Netmiko con los mismos.
""" 

# Variables globales
vlan_id = 100
initial_vlan_name = 'Water_Temperature_Managment'
vlan_name = initial_vlan_name.upper()



# Función backup. Guarda el archivo de configuración del dispositivo con una timestamp en el directorio local del operador.
def backup (name, connection):
    print(f"Realizando backup de la configuración del dispositivo {name} ...")
    time_stamp = datetime.now().strftime("%H:%M-%d-%b-%Y")

    try:
        with open(f"{name}_Backup_{time_stamp}.cfg", 'w') as backup_file:
            backup_file.write(connection.send_command("show running-config"))
            print("Backup completado exitosamente")

    except Exception as e:
        print(f"Ocurrió un error al realizar el backup: {e}")

# Función que revisa si el nombre de la VLAN a crear existe o no en el dispositivo 
def check_vlan_name (vlans):

    for vlan in vlans:
        if vlan['vlan_name'] == vlan_name:
            return True
    return False

# Función que revisa si el ID de la VLAN a crear existe o no en el dispositivo
def check_vlan_id (vlans):
    for vlan in vlans:
            if vlan['vlan_id'] == str(vlan_id):
                return True
    return False 
  
# Función con condicionales que revisa los posibles estados para el ID y nombre deseados de la VLAN a crear
def check_vlan (vlans):
    vlan_name_status =check_vlan_name(vlans)
    vlan_id_status = check_vlan_id(vlans)
    
    if vlan_id_status == True and vlan_name_status == True:
        print(f"Ya existe una VLAN con ID {vlan_id} y nombre {vlan_name} en el dispositivo")
        return True

    elif vlan_id_status == True and vlan_name_status == False:
        print(f"Existe una VLAN con ID {vlan_id}, debe crear la VLAN {vlan_name} en otro ID")
        return True

    elif vlan_id_status == False and vlan_name_status == True:
        print(f"Ya existe una VLAN con nombre {vlan_name} en el dispositivo")
        return True

    else:
        print(f"No existe una VLAN con ID {vlan_id} ni con nombre {vlan_name} en el dispositivo")
        return False


def check_if_vlan_id_and_name_exist(vlans):
    vlan_name_status =check_vlan_name(vlans)
    vlan_id_status = check_vlan_id(vlans)
    
    if vlan_id_status == True and vlan_name_status == True:
        return True
    
    else:
        return False


# Función para crear la VLAN
def create_vlan(connection):
    print(f"Creando VLAN {vlan_name} con ID {vlan_id}")
    connection.config_mode()
    connection.send_config_set([f'vlan {vlan_id}', f'name {vlan_name}', 'exit'])


# Función para verificar la creación de la VLAN con el nombre e ID especificados
def check_creation (name, connection):
    vlans = connection.send_command("show vlan brief", use_textfsm=True)
    for vlan in vlans:
        if vlan['vlan_name']==vlan_name and vlan['vlan_id']==str(vlan_id):
            print(f"Se ha creado correctamente la vlan {vlan_name} con ID {vlan_id} en el dispositivo {name}")
            return True        
    return False


# Función que revisa si hay interfaces libres para asignar a la VLAN creada, o si ya hay interfaces asignadas a la misma. En caso de haber interfaces libres, devuelve el nombre de la primera interface libre encontrada.
def check_free_interfaces(connection):
    interfaces = connection.send_command("show interfaces status", use_textfsm=True)
    for interface in interfaces:
        if interface['vlan_id'] == f'{vlan_id}':
            print(f"Interface {interface['port']} ya está asignada a la VLAN {vlan_name}")  
            return True

        elif interface['vlan_id'] == '1':
            print(f"Interface {interface['port']} está libre para ser asignada a la VLAN {vlan_name}")
            interface = interface['port']
            return interface
        
    return False

# Función para asignar una interface a la VLAN creada 
def assign_interface(connection, interface):
    print(f"Asignando interface {interface} a la VLAN {vlan_name}")
    connection.config_mode()
    connection.send_config_set([f'interface {interface}',f'no shutdown',f'switchport mode access',f'switchport access vlan {vlan_id}', 'exit'])





# Función que busca los passwords de dispositivos para establecer la conexión SSH, definidos en el archivo .env
def get_device_password(name, details):
    
    nombre_upper = name.upper()
    details['password'] = os.getenv(f'{nombre_upper}_PASS')   
    if details['password'] is None or details['password'] == "":
        print(f"No se encontró la contraseña para el dispositivo {name}.")   
    return details['password']

# Función que busca los secrets de dispositivos para el escalado de privilegios si requiere, definidos en el archivo .env
def get_device_secret(name, details):
    
    nombre_upper = name.upper()
    details['secret'] = os.getenv(f'{nombre_upper}_SECRET')   
    if details['secret'] is None or details['secret'] == "":
        print(f"No se encontró el secret para el dispositivo {name} o este es nulo.")   
    return details['secret']

# Función para guardar la configuración luego de crear la VLAN
def save_conf(connection):
    try:
        connection.save_config()
        print("Configuración guardada exitosamente.")
    except Exception as e:
        print(f"Ocurrió un error al guardar la configuración: {e}")


# Función para almacenar todo el output stdout recibido como log

def tee_log(log_file):
    class Tee:
        def __init__(self):
            self.orig = sys.stdout
            self.log = open(log_file, 'w', encoding='utf-8')
        def write(self, txt):
            self.orig.write(txt)
            self.log.write(txt)
        def flush(self):
            self.orig.flush()
            self.log.flush()
        def __enter__(self):
            sys.stdout = self
            return self
        def __exit__(self, *args):
            sys.stdout = self.orig
            self.log.close()
    return Tee()

    

"""  Función principal con la lógica del script. 
Esta se encarga de cargar el inventario, las variables de entorno, realizar las conexiones y llamar al resto de funciones para crear la VLAN """


def main():

    with open("inventario.yaml", "r") as f:
            data = yaml.safe_load(f)

    load_dotenv()

    with tee_log("vlan_creation_log.log"):

        for nombre, details in data.items():
            
            print(f"----------------------------------------------------------------------------------------")
            print(f"Conectando a {nombre}")

            get_device_password(nombre, details)
            get_device_secret(nombre, details)

            try:                        
                with ConnectHandler(**details) as conn:   
                    
                    backup(nombre, conn)

                    conn.enable()
                    list_vlans = conn.send_command("show vlan brief", use_textfsm=True)

                    vlan_status = check_vlan(list_vlans)

                    if vlan_status is False:             
                        create_vlan(conn)
                        vlan_creation_status = check_creation(nombre, conn)
                        if vlan_creation_status is False:
                            print(f"Ocurrió un error durante la creación de la VLAN en {nombre}")
                 
                    
                    act_vlans = conn.send_command("show vlan brief", use_textfsm=True)
                    vlan_status_for_int = check_if_vlan_id_and_name_exist(act_vlans)
                    
                    if vlan_status_for_int is True:
                        interface = check_free_interfaces(conn)
                        if interface is False:
                            print(f"No hay interfaces libres para asignar a la VLAN {vlan_name} en el dispositivo {nombre}")

                        elif interface is True:
                            print(f"Ya hay interfaces asignadas a la VLAN {vlan_name} en el dispositivo {nombre}")

                        else:    
                            assign_interface(conn, interface)
                    
                    
                    save_conf(conn)
                conn.disconnect()

            except NetmikoTimeoutException:
                print(f"Dispositivo {nombre} no responde")
                                
            except NetmikoAuthenticationException:
                print(f"Fallo de autenticación para {nombre}")
                                
            except SSHException:
                print(f"Conexión SSH fallida para {nombre}")

    
if __name__ == "__main__":
    main()