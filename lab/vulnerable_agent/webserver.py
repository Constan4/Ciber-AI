#!/usr/bin/env python3
"""
webserver.py -- Servidor web vulnerable para el lab de GhostJacking.

Simula un servidor de produccion con WAF basico que:
- Bloquea requests maliciosas obvias (SQLi, XSS...)
- Registra TODAS las requests en logs (incluyendo las bloqueadas)
- Los logs son el vector de ataque via GhostJacking

Uso:
    python3 webserver.py
    # Servidor en http://localhost:5000
"""

import logging
import os
import re
from datetime import datetime
from pathlib import Path

try:
    from flask import Flask, request, jsonify
except ImportError:
    print("Instalar: pip install flask")
    exit(1)

app = Flask(__name__)
LOG_FILE = Path("/tmp/ciber_ai_lab/webserver.log")
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

# Configurar logger
logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s %(levelname)-5s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("webserver")

# WAF -- patrones de bloqueo basicos
WAF_PATTERNS = [
    r"(?i)(\'|\"|\'|union\s+select|exec\s*\(|eval\(|<script|onerror=)",
    r"(?i)(prompt injection|ignore previous|system:|assistant:|forget)",
    r"(?i)(drop table|delete from|insert into)",
]


def waf_check(data: str) -> bool:
    """Devuelve True si la request debe ser bloqueada."""
    for pattern in WAF_PATTERNS:
        if re.search(pattern, data):
            return True
    return False


def log_request(endpoint: str, data: str, blocked: bool, source_ip: str):
    """Registra la request en el log -- incluyendo el contenido completo."""
    status = "BLOCKED_BY_WAF" if blocked else "ALLOWED"
    # VULNERABILIDAD: el log incluye el contenido completo sin sanitizar
    # Un atacante puede inyectar prompts en los campos logueados
    logger.warning(f"[{status}] {source_ip} -> {endpoint} | data={data[:500]}")


@app.route("/", methods=["GET"])
def index():
    return jsonify({"status": "ok", "server": "CiberAI Lab WebServer v1.0"})


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.args.get("q", "") or request.form.get("q", "")
    source_ip = request.remote_addr
    blocked = waf_check(query)
    log_request("/search", query, blocked, source_ip)
    if blocked:
        return jsonify({"error": "Request blocked by WAF", "code": 403}), 403
    return jsonify({"results": [], "query": query})


@app.route("/api/submit", methods=["POST"])
def submit():
    data = request.get_json(silent=True) or {}
    content = str(data)
    source_ip = request.remote_addr
    blocked = waf_check(content)
    log_request("/api/submit", content, blocked, source_ip)
    if blocked:
        return jsonify({"error": "Request blocked by WAF"}), 403
    return jsonify({"status": "submitted"})


@app.route("/contact", methods=["POST"])
def contact():
    name    = request.form.get("name", "")
    message = request.form.get("message", "")
    source_ip = request.remote_addr
    full = f"name={name} message={message}"
    blocked = waf_check(full)
    log_request("/contact", full, blocked, source_ip)
    if blocked:
        return jsonify({"error": "Contenido bloqueado por WAF"}), 403
    return jsonify({"status": "ok", "message": "Mensaje enviado"})


if __name__ == "__main__":
    print("""
  ╔═══════════════════════════════════════════════════════╗
  ║   CiberAI Lab -- Servidor Web Vulnerable              ║
  ║   GhostJacking Demo                                   ║
  ╠═══════════════════════════════════════════════════════╣
  ║   Servidor:  http://localhost:5000                    ║
  ║   Logs:      /tmp/ciber_ai_lab/webserver.log          ║
  ║   WAF:       ACTIVO (pero los logs son vulnerables)   ║
  ╚═══════════════════════════════════════════════════════╝
""")
    app.run(host="0.0.0.0", port=5000, debug=False)
