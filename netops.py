from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException
import logging

# Configuración de la VLAN
VLAN_ID = "100"
VLAN_NAME = "Water_Temperature_Management"

# Diccionario base para las credenciales (asumimos las mismas para todos por simplicidad)
common_credentials = {
    'device_type': 'cisco_ios', # Cambiar según el fabricante (hp_procurve, juniper_junos, etc.)
    'username': 'admin',
    'password': 'TuPasswordSeguro',
    'secret': 'TuEnablePassword', # Requerido para entrar en modo privilegiado
}

# Generamos la lista de 50 switches (Simulado: 5 zonas con 10 switches cada una)
switches = []
for zona in range(1, 6):
    for n in range(1, 11):
        switches.append({
            **common_credentials,
            'host': f'10.{zona}.1.{n}', # Ejemplo de IP: 10.Zona.1.Switch
        })

def configure_vlan(device_params):
    host = device_params['host']
    try:
        # 1. Establecer conexión
        print(f"[*] Conectando al switch {host}...")
        net_connect = ConnectHandler(**device_params)
        net_connect.enable() # Entrar en modo 'enable'

        # 2. Comprobar si la VLAN ya existe
        # Ejecutamos 'show vlan id 100' y verificamos la salida
        check_command = f"show vlan id {VLAN_ID}"
        output = net_connect.send_command(check_command)

        if "not found" in output.lower() or "not in" in output.lower():
            print(f"[+] La VLAN {VLAN_ID} no existe en {host}. Creándola...")
            
            # 3. Crear la VLAN si no existe
            config_commands = [
                f"vlan {VLAN_ID}",
                f"name {VLAN_NAME}",
                "exit"
            ]
            net_connect.send_config_set(config_commands)
            print(f"[OK] VLAN {VLAN_ID} creada exitosamente en {host}.")
        else:
            print(f"[-] La VLAN {VLAN_ID} ya existe en {host}. Saltando...")

        # 4. Desconectar
        net_connect.disconnect()

    except NetmikoTimeoutException:
        print(f"[!] ERROR: Tiempo de espera agotado para {host}. ¿Está encendido?")
    except NetmikoAuthenticationException:
        print(f"[!] ERROR: Fallo de autenticación en {host}. Revisa las credenciales.")
    except Exception as e:
        print(f"[!] ERROR inesperado en {host}: {e}")

# Ejecución principal
if __name__ == "__main__":
    print(f"--- Iniciando despliegue de VLAN {VLAN_ID} ---")
    for switch in switches:
        configure_vlan(switch)
    print("--- Proceso finalizado ---")