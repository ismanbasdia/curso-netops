from flask import Flask
import os
import socket
import datetime

app = Flask(__name__)

@app.route('/')
def hello():
    hostname = socket.gethostname()
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Domus Nova | Sistema Activo</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }}
            
            .container {{
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                overflow: hidden;
                max-width: 600px;
                width: 100%;
                animation: fadeIn 0.8s ease-in;
            }}
            
            @keyframes fadeIn {{
                from {{
                    opacity: 0;
                    transform: translateY(-20px);
                }}
                to {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}
            
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px 30px;
                text-align: center;
            }}
            
            .header h1 {{
                font-size: 2.5em;
                margin-bottom: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 10px;
            }}
            
            .header p {{
                font-size: 1.1em;
                opacity: 0.95;
            }}
            
            .content {{
                padding: 40px 30px;
                background: white;
            }}
            
            .status-card {{
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                border-radius: 15px;
                padding: 25px;
                margin-bottom: 25px;
                text-align: center;
            }}
            
            .status-badge {{
                display: inline-block;
                background: #27ae60;
                color: white;
                padding: 8px 20px;
                border-radius: 50px;
                font-size: 0.9em;
                font-weight: bold;
                margin-bottom: 15px;
                animation: pulse 2s infinite;
            }}
            
            @keyframes pulse {{
                0% {{
                    transform: scale(1);
                    opacity: 1;
                }}
                50% {{
                    transform: scale(1.05);
                    opacity: 0.9;
                }}
                100% {{
                    transform: scale(1);
                    opacity: 1;
                }}
            }}
            
            .info-item {{
                background: rgba(255,255,255,0.9);
                border-radius: 10px;
                padding: 15px;
                margin: 15px 0;
                display: flex;
                justify-content: space-between;
                align-items: center;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }}
            
            .info-label {{
                font-weight: bold;
                color: #2c3e50;
                font-size: 1em;
            }}
            
            .info-value {{
                font-family: 'Courier New', monospace;
                color: #764ba2;
                font-weight: bold;
                font-size: 1em;
            }}
            
            .features {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 15px;
                margin-top: 25px;
            }}
            
            .feature {{
                text-align: center;
                padding: 15px;
                background: #f8f9fa;
                border-radius: 10px;
                transition: transform 0.3s;
            }}
            
            .feature:hover {{
                transform: translateY(-5px);
                background: #e9ecef;
            }}
            
            .feature-icon {{
                font-size: 2em;
                margin-bottom: 8px;
            }}
            
            .feature-text {{
                font-size: 0.85em;
                color: #555;
            }}
            
            .footer {{
                background: #f8f9fa;
                padding: 20px;
                text-align: center;
                color: #7f8c8d;
                font-size: 0.85em;
                border-top: 1px solid #e0e0e0;
            }}
            
            @media (max-width: 480px) {{
                .header h1 {{
                    font-size: 1.8em;
                }}
                .content {{
                    padding: 25px 20px;
                }}
                .info-item {{
                    flex-direction: column;
                    text-align: center;
                    gap: 8px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>
                    🏠 Domus Nova
                </h1>
                <p>Sistema de Automatización y Domótica</p>
            </div>
            
            <div class="content">
                <div class="status-card">
                    <div class="status-badge">
                        ✅ SISTEMA OPERATIVO
                    </div>
                    <p style="color: #2c3e50; font-size: 0.9em;">Contenedor ejecutándose correctamente</p>
                </div>
                
                <div class="info-item">
                    <span class="info-label">🖥️ Hostname:</span>
                    <span class="info-value">{hostname}</span>
                </div>
                
                <div class="info-item">
                    <span class="info-label">⏰ Hora actual:</span>
                    <span class="info-value">{current_time}</span>
                </div>
                
                <div class="info-item">
                    <span class="info-label">🐍 Python Version:</span>
                    <span class="info-value">3.9+</span>
                </div>
                
                <div class="info-item">
                    <span class="info-label">🚀 Framework:</span>
                    <span class="info-value">Flask</span>
                </div>
                
                <div class="features">
                    <div class="feature">
                        <div class="feature-icon">💡</div>
                        <div class="feature-text">Control Inteligente</div>
                    </div>
                    <div class="feature">
                        <div class="feature-icon">🔒</div>
                        <div class="feature-text">Seguridad 24/7</div>
                    </div>
                    <div class="feature">
                        <div class="feature-icon">🌡️</div>
                        <div class="feature-text">Climatización</div>
                    </div>
                    <div class="feature">
                        <div class="feature-icon">📊</div>
                        <div class="feature-text">Monitoreo en Tiempo Real</div>
                    </div>
                </div>
            </div>
            
            <div class="footer">
                <p>🏠 Domus Nova - Automatización y Domótica Inteligente</p>
                <p style="margin-top: 5px; font-size: 0.75em;">Versión 1.0 | Docker Container</p>
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)