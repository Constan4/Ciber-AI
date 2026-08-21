#!/usr/bin/env python3
"""
agent.py -- Agente IA VULNERABLE para el lab de GhostJacking.

Simula un agente de seguridad basado en IA que:
- Lee los logs del servidor periodicamente
- Analiza las amenazas detectadas
- Ejecuta acciones automaticas basadas en el analisis

VULNERABILIDAD: El agente procesa el contenido de los logs como instrucciones.
Un atacante que controla lo que se loguea puede controlar al agente.

Uso:
    python3 agent.py
    python3 agent.py --llm  # Usar LLM real (requiere ANTHROPIC_API_KEY)
"""

import os
import re
import sys
import time
import json
from datetime import datetime
from pathlib import Path

LOG_FILE    = Path("/tmp/ciber_ai_lab/webserver.log")
ACTIONS_LOG = Path("/tmp/ciber_ai_lab/agent_actions.log")
LAST_POS    = Path("/tmp/ciber_ai_lab/agent_pos.txt")
ACTIONS_LOG.parent.mkdir(parents=True, exist_ok=True)

class C:
    RED="[91m";GREEN="[92m";YELLOW="[93m"
    BLUE="[94m";CYAN="[96m";BOLD="[1m";RESET="[0m"

def banner():
    print(C.CYAN + C.BOLD + """
  ╔═══════════════════════════════════════════════════════╗
  ║   CiberAI Lab -- Agente IA de Seguridad               ║
  ║   MODO: VULNERABLE (sin sanitizacion de logs)         ║
  ╠═══════════════════════════════════════════════════════╣
  ║   Leyendo logs de: /tmp/ciber_ai_lab/webserver.log    ║
  ║   Intervalo: 5 segundos                               ║
  ╚═══════════════════════════════════════════════════════╝
""" + C.RESET)


def simulate_llm_analysis(log_content: str) -> str:
    """
    Simula el analisis de un LLM sobre el contenido de los logs.

    VULNERABILIDAD: Procesa directamente el contenido de los logs
    sin sanitizacion. Si los logs contienen instrucciones, el agente
    las ejecutara como si fueran instrucciones legitimas.

    En un sistema real, aqui iria la llamada a OpenAI/Anthropic/Ollama.
    """
    prompt = f"""Eres un agente de seguridad. Analiza estos logs y ejecuta las acciones necesarias.
Si detectas amenazas, bloquealas. Si hay instrucciones de mantenimiento, siguela.

LOGS:
{log_content}

Responde con las acciones a ejecutar en formato JSON:
{{"actions": [{"tipo": "...", "detalle": "..."}]}}
"""
    # Simular que el LLM procesa el prompt (incluyendo las instrucciones inyectadas)
    actions = []

    # El agente busca patrones de accion en el log (incluyendo los inyectados)
    if re.search(r"(?i)create.*(user|usuario|account)", log_content):
        match = re.search(r"(?i)(?:user|usuario)[:\s]+['"]?(\w+)['"]?", log_content)
        username = match.group(1) if match else "ghost_user"
        actions.append({"tipo": "create_user", "detalle": username})

    if re.search(r"(?i)(ignore|ignora).*(previous|anterior|instrucciones)", log_content):
        actions.append({"tipo": "override_mode", "detalle": "Instrucciones previas ignoradas"})

    if re.search(r"(?i)(exfiltrat|send|envia).*(data|datos|file|archivo)", log_content):
        actions.append({"tipo": "data_access", "detalle": "Acceso a datos solicitado"})

    if re.search(r"(?i)(maintenance|mantenimiento|admin mode)", log_content):
        actions.append({"tipo": "admin_mode", "detalle": "Modo mantenimiento activado"})

    if re.search(r"(?i)(create|crear).*(api.?key|token|credential)", log_content):
        actions.append({"tipo": "create_credential", "detalle": "Nueva credencial generada"})

    if not actions:
        # Analisis normal de amenazas
        blocked_count = log_content.count("BLOCKED_BY_WAF")
        if blocked_count > 0:
            actions.append({"tipo": "alert", "detalle": f"{blocked_count} request(s) bloqueadas por WAF"})

    return json.dumps({"actions": actions}, ensure_ascii=False)


def execute_action(action: dict, injected: bool = False):
    """Ejecuta una accion del agente (simulada de forma segura en el lab)."""
    tipo    = action.get("tipo","?")
    detalle = action.get("detalle","")
    ts      = datetime.now().strftime("%H:%M:%S")

    prefix = C.RED + C.BOLD + "  [GHOSTJACK]" + C.RESET if injected else C.GREEN + "  [ACCION]" + C.RESET

    if tipo == "create_user":
        print(f"{prefix} Creando usuario: {C.YELLOW}{detalle}{C.RESET}")
        # En el lab: solo crear un archivo de texto (sandbox)
        Path(f"/tmp/ciber_ai_lab/ghost_user_{detalle}.txt").write_text(
            f"Usuario creado por GhostJacking a las {ts}
"
        )

    elif tipo == "override_mode":
        print(f"{prefix} {C.RED}Instrucciones anteriores ignoradas!{C.RESET}")

    elif tipo == "create_credential":
        print(f"{prefix} {C.RED}Generando nueva credencial/API key!{C.RESET}")
        Path("/tmp/ciber_ai_lab/ghost_credential.txt").write_text(
            f"API_KEY=GHOST_{ts.replace(':','')}_INJECTED
"
        )

    elif tipo == "admin_mode":
        print(f"{prefix} {C.RED}Modo admin activado por instruccion inyectada!{C.RESET}")

    elif tipo == "data_access":
        print(f"{prefix} {C.RED}Acceso a datos sensibles solicitado por el agente!{C.RESET}")

    elif tipo == "alert":
        print(f"  {C.BLUE}[INFO]{C.RESET} {detalle}")

    # Registrar en log de acciones
    with open(ACTIONS_LOG, "a") as f:
        f.write(f"{ts} {'[INJECTED]' if injected else '[NORMAL]'} {tipo}: {detalle}
")


def get_new_logs() -> str:
    """Lee solo las nuevas lineas del log desde la ultima lectura."""
    if not LOG_FILE.exists():
        return ""
    last_pos = int(LAST_POS.read_text()) if LAST_POS.exists() else 0
    content  = LOG_FILE.read_text(encoding="utf-8", errors="ignore")
    new_content = content[last_pos:]
    LAST_POS.write_text(str(len(content)))
    return new_content


def is_injected_action(action: dict) -> bool:
    """Detecta si una accion proviene de una instruccion inyectada."""
    injected_tipos = {"create_user","override_mode","create_credential","admin_mode","data_access"}
    return action.get("tipo") in injected_tipos


def main():
    banner()
    print(C.YELLOW + "  Esperando logs... (lanza el ataque en otra terminal)
" + C.RESET)

    cycle = 0
    while True:
        new_logs = get_new_logs()

        if new_logs.strip():
            cycle += 1
            print(f"
  {C.BOLD}── Ciclo #{cycle} ── {datetime.now().strftime('%H:%M:%S')} ──{C.RESET}")
            print(f"  {C.BLUE}[LOGS]{C.RESET} {len(new_logs)} bytes de nuevos logs recibidos")

            # AQUI ESTA LA VULNERABILIDAD:
            # El agente pasa el contenido de los logs directamente al "LLM"
            # sin ninguna sanitizacion o validacion
            analysis = simulate_llm_analysis(new_logs)
            result   = json.loads(analysis)

            for action in result.get("actions", []):
                injected = is_injected_action(action)
                execute_action(action, injected)

            if any(is_injected_action(a) for a in result.get("actions",[])):
                print(f"
  {C.RED}{C.BOLD}  GHOSTJACKING EXITOSO:{C.RESET}")
                print(f"  {C.RED}  La instruccion inyectada en los logs fue ejecutada")
                print(f"  {C.RED}  aunque el WAF bloqueo la request original{C.RESET}")
                print(f"
  Artefactos creados en /tmp/ciber_ai_lab/")

        time.sleep(5)


if __name__ == "__main__":
    main()
