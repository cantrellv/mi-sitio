# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, redirect, flash
from markupsafe import escape
import os

app = Flask(__name__)
app.secret_key = 'clave_segura'

contactos = []

BASE_TEMPLATE = '''
<!doctype html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Embarazo a temprana edad - Información y soluciones</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
      body { font-family: Arial, sans-serif; }
      h1,h2,h3 { margin-top: 20px; }
    </style>
  </head>
  <body class="bg-light">
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
      <div class="container">
        <a class="navbar-brand" href="/">EmbarazoTemprano</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#nav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="nav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item"><a class="nav-link" href="/">Inicio</a></li>
            <li class="nav-item"><a class="nav-link" href="/soluciones">Soluciones</a></li>
            <li class="nav-item"><a class="nav-link" href="/recursos">Recursos</a></li>
            <li class="nav-item"><a class="nav-link" href="/contacto">Contacto</a></li>
          </ul>
        </div>
      </div>
    </nav>

    <div class="container my-5">
      {% with messages = get_flashed_messages() %}
        {% if messages %}
          <div class="alert alert-success">{{ messages[0] }}</div>
        {% endif %}
      {% endwith %}
      {{ body|safe }}
    </div>

    <footer class="bg-white border-top py-3 mt-5">
      <div class="container text-center small text-muted">
        Proyecto educativo - Si estás en riesgo, consulta a un profesional de salud o a una línea de ayuda local.
      </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
  </body>
</html>
'''

INDEX_BODY = '''
<h1>Embarazo a temprana edad</h1>
<p class="lead">Información clara, sin juicios, sobre causas, consecuencias y soluciones prácticas.</p>

<h3>Qué es</h3>
<p>El embarazo a temprana edad ocurre en la adolescencia (usualmente menores de 20 años). Puede deberse a falta de educación sexual, barreras a anticoncepción, presión social o violencia.</p>

<h3>Consecuencias</h3>
<ul>
  <li>Riesgos para la salud materna e infantil.</li>
  <li>Interrupción de la educación y oportunidades laborales.</li>
  <li>Impacto emocional y social en la joven y su familia.</li>
</ul>

<a class="btn btn-primary mt-3" href="/soluciones">Ver soluciones recomendadas</a>
'''

SOLUCIONES_BODY = '''
<h2>Soluciones efectivas</h2>
<ol>
  <li>Educación sexual integral</li>
  <li>Acceso a anticoncepción</li>
  <li>Apoyo emocional</li>
  <li>Continuidad educativa</li>
  <li>Programas comunitarios y mentoría</li>
</ol>
'''

RECURSOS_BODY = '''
<h2>Recursos y líneas de ayuda (ejemplo)</h2>
<ul>
  <li>Centro de Salud Juvenil: consulta en tu sistema público.</li>
  <li>Línea de apoyo emocional: 01-800-XXX-XXXX (ejemplo).</li>
  <li>Organizaciones con consejería y anticoncepción.</li>
</ul>
'''

CONTACTO_BODY = '''
<h2>Contacto</h2>
<form method="post" action="/contacto">
  <div class="mb-3">
    <label class="form-label">Nombre (opcional)</label>
    <input class="form-control" name="nombre" maxlength="100">
  </div>
  <div class="mb-3">
    <label class="form-label">Correo electrónico</label>
    <input class="form-control" name="email" type="email" required>
  </div>
  <div class="mb-3">
    <label class="form-label">Mensaje</label>
    <textarea class="form-control" name="mensaje" rows="4" required></textarea>
  </div>
  <button class="btn btn-success" type="submit">Enviar</button>
</form>

<hr>
<h5>Contactos recibidos</h5>
<ul>
  {% for c in contactos %}
    <li><strong>{{ c.email|e }}</strong> - {{ c.mensaje|e }} {% if c.nombre %} ({{ c.nombre|e }}){% endif %}</li>
  {% else %}
    <li class="text-muted">No hay contactos aún.</li>
  {% endfor %}
</ul>
'''

@app.route('/')
def index():
    return render_template_string(BASE_TEMPLATE, body=INDEX_BODY)

@app.route('/soluciones')
def soluciones():
    return render_template_string(BASE_TEMPLATE, body=SOLUCIONES_BODY)

@app.route('/recursos')
def recursos():
    return render_template_string(BASE_TEMPLATE, body=RECURSOS_BODY)

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        nombre = escape(request.form.get('nombre', '').strip())
        email = escape(request.form.get('email', '').strip())
        mensaje = escape(request.form.get('mensaje', '').strip())
        if not email or not mensaje:
            flash('Completa los campos obligatorios.')
            return redirect('/contacto')
        contactos.insert(0, {'nombre': nombre, 'email': email, 'mensaje': mensaje})
        flash('Gracias, tu mensaje ha sido recibido.')
        return redirect('/contacto')
    return render_template_string(BASE_TEMPLATE, body=CONTACTO_BODY, contactos=contactos)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
