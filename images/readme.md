## Material Práctico: Despliegue de una Aplicación Dockerizada desde GitHub a una Máquina Virtual con Podman

---

### Objetivo de la Práctica

En esta actividad vas a experimentar el flujo completo de trabajo que siguen los equipos modernos de desarrollo y operaciones:

1. **Escribir y versionar** el código de una aplicación (en este caso, el `Dockerfile`)
2. **Subir el código a GitHub** (control de versiones)
3. **Acceder a una máquina virtual** que simula un entorno de producción (o pruebas)
4. **Descargar el código desde GitHub** (`git pull`)
5. **Construir una imagen Docker** a partir del `Dockerfile`
6. **Ejecutar un contenedor** con Podman (alternativa a Docker)

## Parte 1: Preparación del Código y Subida a GitHub

### Paso 1.1: Crear el Dockerfile

En tu máquina local, crea una carpeta para el proyecto y dentro de ella crea un archivo llamado `Dockerfile` con el siguiente contenido:

```dockerfile
# Usamos una imagen base ligera de Python
FROM python:3.9-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos un archivo de requisitos (lo crearemos después)
COPY requirements.txt .

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto de la aplicación
COPY app.py .

# Exponemos el puerto donde correrá la aplicación
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
```

### Paso 1.2: Crear la aplicación de ejemplo

Crea un archivo `app.py` con una aplicación web sencilla:

```python
from flask import Flask
import os
import socket

app = Flask(__name__)

@app.route('/')
def hello():
    hostname = socket.gethostname()
    return f"""
    <html>
        <body style="background-color: #f0f0f0; text-align: center; padding: 50px;">
            <h1 style="color: #2c3e50;">🏠 Domus Nova - Servicio Activo</h1>
            <p style="font-size: 18px;">Contenedor ejecutándose correctamente</p>
            <p style="font-family: monospace;">Hostname: {hostname}</p>
            <hr>
            <p style="font-size: 12px; color: #7f8c8d;">Domus Nova - Automatización y Domótica</p>
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### Paso 1.3: Crear el archivo de dependencias

Crea un archivo `requirements.txt`:

```
Flask==2.3.2
```

### Paso 1.4: Subir carperta al repositorio en GitHub de la asignatura 

En tu terminal, dentro de la carpeta del proyecto, ejecuta los siguientes comandos:

```bash
# Inicializar el repositorio local
git init

# Agregar todos los archivos
git add .

# Hacer el primer commit
git commit -m "Primera versión: aplicación Flask con Dockerfile"

# Conectar con el repositorio remoto (cambia el usuario y nombre del repo)
git remote add origin https://github.com/ismanbasdia/curso-netops.git

# Subir el código dentro de la carperta images
git push -u origin main/images
```

---

## Parte 2: Acceso a la Máquina Virtual

### Paso 2.1: Conectarse a la VM

Use la dirección IP, usuario y contraseña de la máquina virtual que se le proporcionó en el grupo de whatsapp. Conéctate por SSH:

```bash
ssh -p 2000 usuario@IP
```

### Paso 2.2: Verificar que Podman está instalado

```bash
podman --version
```

Deberías ver algo como: `podman version 4.x.x`


## Parte 3: Descargar el Código desde GitHub

### Paso 3.1: Clonar el repositorio en la VM

Dentro de la VM, clona el repositorio que subiste en la carpeta curso-netops/tu-nombre:

```bash
git clone https://github.com/TU_USUARIO/domus-nova-app.git
# accede luego a tu carpeta
```

### Paso 3.2: Verificar que los archivos están ahí

```bash
ls -la
```

Deberías ver: `Dockerfile`, `app.py`, `requirements.txt`

---

## Parte 4: Construir la Imagen con Podman

Podman es una alternativa a Docker que no requiere un daemon en segundo plano y es compatible con las imágenes de Docker.

### Paso 4.1: Construir la imagen

```bash
podman build -t image_tunombre .
```

El comando `-t` le da un nombre a la imagen. El punto `.` indica que el `Dockerfile` está en el directorio actual.

### Paso 4.2: Verificar que la imagen se creó

```bash
podman images
```

Deberías ver `image_tunombre` en la lista.

---

## Parte 5: Ejecutar el Contenedor con Podman

### Paso 5.1: Ejecutar el contenedor

```bash
podman run -d -p 8080:5000 --name pod_tunombre image_tunombre
```

Explicación:
- `-d`: ejecuta en segundo plano (detached)
- `-p 8080:5000`: mapea el puerto 5000 del contenedor al puerto 8080 de la VM
- `--name`: asigna un nombre al contenedor

### Paso 5.2: Verificar que el contenedor está corriendo

```bash
podman ps
```

Deberías ver el contenedor `pod_tunombre` con estado `Up`.

### Paso 5.3: Probar la aplicación

Desde tu navegador (en tu máquina local), accede a:

```
http://IP_DE_LA_VM:8080
```

Deberías ver el mensaje de Domus Nova.

### Paso 5.4: Ver los logs del contenedor

```bash
podman logs pod_tunombre
```

