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
