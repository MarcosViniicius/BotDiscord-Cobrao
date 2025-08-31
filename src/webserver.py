"""
Servidor Flask único para servir todos os sites criados dinamicamente
"""
import os
from flask import Flask, send_file, abort

SITES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../sites'))
app = Flask(__name__)

@app.route('/site_<site_id>')
def serve_site(site_id):
    site_path = os.path.join(SITES_DIR, f'site_{site_id}.html')
    if os.path.exists(site_path):
        return send_file(site_path)
    return abort(404)

@app.route('/')
def index():
    # Lista todos os sites disponíveis
    sites = [f for f in os.listdir(SITES_DIR) if f.startswith('site_') and f.endswith('.html')]
    links = [f'<a href="/site_{f[5:-5]}">{f}</a>' for f in sites]
    return f"<h1>Sites Disponíveis</h1><ul>{''.join(f'<li>{l}</li>' for l in links)}</ul>"

if __name__ == '__main__':
    print("Iniciando webserver na porta 8000...")
    app.run(host='0.0.0.0', port=8000)
