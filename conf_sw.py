import yaml
from netmiko import ConnectHandler


# Nombre del archivo YAML con los datos de los switches
YAML_FILE = "lista_switches.yaml"

def check_vlan_exists(connection, vlan_id):

    output = connection.send_command(f"show vlan id {vlan_id}")# verificando si la vlan 100 existe
    return f"VLAN {vlan_id} not found" not in output

def create_vlan(connection, vlan_id, vlan_name):# funcion para crear vlan, con los parametros necarios

    config_commands = [
        f"vlan {vlan_id}",
        f"name {vlan_name}",
        "exit"
    ]
    output = connection.send_config_set(config_commands)#enviando la lista de comandos
    return output

def main():
 
    try:
        with open(YAML_FILE, 'r') as f: #abriendo el archivo
            data = yaml.safe_load(f)
    except FileNotFoundError:#validacion ante errores
        print(f"Error: No se encontró el archivo '{YAML_FILE}'.")
        return
    except yaml.YAMLError as e:
        print(f"Error al leer el archivo YAML: {e}")
        return

    switches = data.get('switches', {})#guardando los datos en un diccionario
    if not switches:
        print("No se encontraron switches en el archivo YAML.")
        return

    vlan_id = 100
    vlan_name = "Temp_agua"

    
    for sw_name, sw_params in switches.items():
        print(f"\n--- Procesando {sw_name} ({sw_params['ip']}) ---")

        # Preparar parámetros de conexión para Netmiko, leyendo los datos del archivo yaml
        device = {
            'device_type': sw_params['device_type'],
            'ip': sw_params['ip'],
            'username': sw_params['username'],
            'password': sw_params['password'],
            'secret': sw_params['secret'],  # enable password
            
        }

        try:
            # Conectando al dispositivo
            connection = ConnectHandler(**device) #desempaquetando el diccionario
            # Entrar en modo enable 
            connection.enable()
            print(f" Conexión exitosa a {sw_name} ({sw_params['ip']})")

            # Verificar si la VLAN existe
            if check_vlan_exists(connection, vlan_id):
                print(f" La VLAN {vlan_id} ya existe en {sw_name}.")
            else:
                print(f"  VLAN {vlan_id} no encontrada. Creando VLAN...")
                output = create_vlan(connection, vlan_id, vlan_name)
                print("Comandos aplicados:")
                print(output)
                print(f" VLAN {vlan_id} creada correctamente en {sw_name} con nombre '{vlan_name}'.")

            # Desconectar
            connection.disconnect()

        except Exception as e:
            print(f" Error inesperado con {sw_name}: {e}")

    print("\n--- Proceso finalizado ---")

if __name__ == "__main__":
    main()