import yaml
from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

# =========================
# CONFIGURACIÓN
# =========================

VLAN_ID = "100"
VLAN_NAME = "Water_Temperature_Management"


# =========================
# CARGA DE YAML
# =========================

def load_devices(file):
    with open(file, "r") as f:
        data = yaml.safe_load(f)
    return data["devices"]


# =========================
# FUNCIONES
# =========================

def vlan_exists(vlans, vlan_id):
    for vlan in vlans:
        if vlan.get("vlan_id") == vlan_id:
            return True
    return False


def get_vlans(connection):
    output = connection.send_command(
        "show vlan brief",
        use_textfsm=True
    )

    if not isinstance(output, list):
        raise ValueError("Error al parsear con TextFSM")

    return output


def configure_vlan(connection):
    commands = [
        f"vlan {VLAN_ID}",
        f"name {VLAN_NAME}"
    ]
    connection.send_config_set(commands)
    connection.save_config()


def process_device(device):
    ip = device["host"]

    try:
        print(f"\nConectando a {ip}...")

        connection = ConnectHandler(**device)

        # ENTRAR A MODO PRIVILEGIADO
        connection.enable()

        # =========================
        # VALIDACIÓN INICIAL
        # =========================
        vlans_before = get_vlans(connection)

        if vlan_exists(vlans_before, VLAN_ID):
            print(f" VLAN {VLAN_ID} ya existe en {ip}")
        else:
            print(f" Creando VLAN {VLAN_ID} en {ip}")

            configure_vlan(connection)

            # VALIDACIÓN FINAL
            vlans_after = get_vlans(connection)

            if vlan_exists(vlans_after, VLAN_ID):
                print(f" VLAN creada correctamente en {ip}")
            else:
                print(f" Error en validación en {ip}")

        connection.disconnect()
    except NetmikoTimeoutException:
        print(f" Timeout en {ip}")
    except NetmikoAuthenticationException:
        print(f" Error de autenticación en {ip}")
    except Exception as e:
        print(f" Error en {ip}: {e}")


# =========================
# MAIN
# =========================

if __name__ == "__main__":
    devices = load_devices("devices.yaml")

    print(" Iniciando automatización...\n")

    for device in devices:
        print(f" Procesando dispositivo: {device['host']}")
        process_device(device)

    print("\n Finalizado.")