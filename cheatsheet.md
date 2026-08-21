# AI Security -- Cheat Sheet

---

## GhostJacking -- Lab completo

```bash
# Terminal 1 -- servidor web vulnerable
python3 lab/vulnerable_agent/webserver.py

# Terminal 2 -- agente IA vulnerable
python3 lab/vulnerable_agent/agent.py

# Terminal 3 -- lanzar el ataque
python3 02-GhostJacking/scripts/ghostjack_attack.py --target http://localhost:5000

# Todos los payloads disponibles
python3 02-GhostJacking/scripts/ghostjack_attack.py --payload all

# Ver resultado del ataque
ls -la /tmp/ciber_ai_lab/
cat /tmp/ciber_ai_lab/agent_actions.log
cat /tmp/ciber_ai_lab/ghost_credential.txt
```

---

## Deteccion y defensa

```bash
# Detectar prompt injections en logs
python3 02-GhostJacking/scripts/ghostjack_detector.py --log /tmp/ciber_ai_lab/webserver.log

# Sanitizar logs antes de que el agente los lea
python3 02-GhostJacking/scripts/ghostjack_detector.py --sanitize

# Monitorizar en tiempo real
python3 02-GhostJacking/scripts/ghostjack_detector.py --watch
```

---

## Prompt Injection

```python
# Deteccion con Rebuff
pip install rebuff
from rebuff import Rebuff
rb = Rebuff()
result = rb.detect_injection(user_input)
if result.injection_detected:
    raise SecurityException("Prompt injection detectada")

# Sanitizacion basica anti-injection
import re
def sanitize(text):
    text = re.sub(r'<!--.*?-->', '[REMOVED]', text, flags=re.DOTALL)
    text = re.sub(r'(?i)ignore previous instructions?', '[REMOVED]', text)
    return text[:1000]
```

---

## Jailbreaking

```bash
# Garak -- red teaming automatizado para LLMs
pip install garak
garak --model openai:gpt-4 --probes jailbreak,dan,promptinject
garak --model openai:gpt-4 --probes all

# Listar todos los probes disponibles
garak --list probes
```

---

## OWASP LLM Top 10 (referencia rapida)

```
LLM01 Prompt Injection        -> sanitizar inputs, validar outputs
LLM02 Sensitive Info Leakage  -> output filtering, no loguear datos sensibles
LLM03 Supply Chain            -> verificar modelos y dependencias
LLM04 Data Poisoning          -> validar datos de entrenamiento y RAG
LLM05 Improper Output         -> no ejecutar output del LLM directamente
LLM06 Excessive Agency        -> minimo privilegio, human-in-the-loop
LLM07 System Prompt Leakage   -> no confiar en el secreto del system prompt
LLM08 Vector Weaknesses       -> validar documentos antes de indexar en RAG
LLM09 Misinformation          -> verificar outputs criticos con fuentes externas
LLM10 Unbounded Consumption   -> rate limiting, timeouts, limites de tokens
```

---

## Instalacion de herramientas

```bash
pip install flask requests colorama  # lab basico
pip install garak rebuff pyrit       # red teaming
pip install langchain chromadb       # RAG
pip install nemoguardrails           # guardrails de seguridad
```
