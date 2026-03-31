import yaml
import logging
import time
from netmiko import ConnectHandler
from netmiko.exceptions import NetMikoTimeoutException, NetMikoAuthenticationException

# Configuración de logging (archivo y consola) para facilitar depuracion y seguimiento
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('vlan_config.log'),
        logging.StreamHandler()
    ]
)

# Datos de la VLAN
VLAN_ID = "100"
VLAN_NAME = "Water_Temperature_Management"

#abre el archivo YAML especificado y lo parsea
def load_inventory(file_path):
    """Carga el inventario desde un archivo YAML."""
    try:
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        return data
    except Exception as e:
        logging.error(f"Error al cargar el archivo YAML: {e}")
        raise

def create_vlan_on_switch(switch_info, creds):
    """
    Conecta al switch, verifica si la VLAN existe, la crea si no, guarda y valida.
    Retorna True si todo fue exitoso, False en caso contrario.
    """
    device = {
        'device_type': creds.get('device_type', 'cisco_ios'),
        'host': switch_info['host'],
        'username': creds['username'],
        'password': creds['password'],
        'secret': creds.get('enable_password', ''),
        'timeout': 30,
        'fast_cli': False
    }
    name = switch_info['name']
    host = switch_info['host']

    try:
        logging.info(f"Conectando a {name} ({host})...")
        conn = ConnectHandler(**device)
        conn.enable()  # entrar en modo enable

        # Verificar si la VLAN ya existe
        output = conn.send_command("show vlan brief")
        if f"VLAN{VLAN_ID}" in output or f" {VLAN_ID} " in output:
            logging.info(f"{name}: La VLAN {VLAN_ID} ya existe. No se requiere acción.")
            conn.disconnect()
            return True

        # Crear la VLAN
        commands = [
            f"vlan {VLAN_ID}",
            f"name {VLAN_NAME}",
            "exit"
        ]
        logging.info(f"{name}: Creando VLAN {VLAN_ID}...")
        conn.send_config_set(commands)

        # Guardar configuración
        logging.info(f"{name}: Guardando configuración...")
        conn.save_config()

        # Validar que la VLAN ahora aparece
        verify_output = conn.send_command("show vlan brief")
        if f"VLAN{VLAN_ID}" in verify_output or f" {VLAN_ID} " in verify_output:
            logging.info(f"{name}: Verificación exitosa - VLAN {VLAN_ID} presente.")
            result = True
        else:
            logging.warning(f"{name}: Verificación fallida - No se encontró VLAN {VLAN_ID} después de crear.")
            result = False

        conn.disconnect()
        return result

    except NetMikoTimeoutException:
        logging.error(f"{name}: Timeout al conectar.")
    except NetMikoAuthenticationException:
        logging.error(f"{name}: Fallo de autenticación.")
    except Exception as e:
        logging.error(f"{name}: Error inesperado: {str(e)}")
    return False

def main():
    # Cargar inventario
    try:
        inventory = load_inventory('switches.yaml')
    except Exception:
        logging.critical("No se pudo cargar el inventario. Abortando.")
        return

    defaults = inventory.get('defaults', {})
    switches = inventory.get('switches', [])
    if not switches:
        logging.error("No se encontraron switches en el inventario.")
        return

    logging.info("=== Inicio del proceso de configuración de VLANs ===")
    total = len(switches)
    success = 0
    failure = 0

    for sw in switches:
        # Combinar credenciales (si el switch tuviera credenciales propias, se podrían sobreescribir)
        creds = defaults.copy()
        if create_vlan_on_switch(sw, creds):
            success += 1
        else:
            failure += 1
        time.sleep(1)  # pausa para no saturar la red

    logging.info(f"=== Proceso completado: {success} exitosos, {failure} fallidos de {total} ===")
    print(f"\nResumen: {success} switches configurados correctamente, {failure} con errores.")

if __name__ == "__main__":
    main()