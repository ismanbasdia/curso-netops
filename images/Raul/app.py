from flask import Flask, request, render_template_string

app = Flask(__name__)

# HTML + CSS básico dentro del mismo archivo
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Saludo Flask</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin-top: 100px;
            background: #f0f2f5;
        }
        .container {
            background: white;
            padding: 2rem;
            border-radius: 20px;
            width: 300px;
            margin: auto;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        input, button {
            padding: 8px;
            margin: 5px;
            font-size: 1rem;
        }
        button {
            background: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .mensaje {
            margin-top: 20px;
            font-size: 1.2rem;
            color: #28a745;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>📝 Aplicación Sencilla</h2>
        <form method="POST">
            <input type="text" name="nombre" placeholder="Escribe tu nombre" required>
            <button type="submit">Saludar</button>
        </form>
        {% if mensaje %}
            <div class="mensaje">{{ mensaje }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    mensaje = None
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        if nombre:
            mensaje = f"¡Hola {nombre}! 👋 Bienvenido a Flask."
        else:
            mensaje = "Por favor ingresa un nombre."
    return render_template_string(HTML, mensaje=mensaje)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)