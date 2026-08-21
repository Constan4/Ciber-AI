# Defensa de Sistemas IA

---

## Principios de diseño seguro para agentes IA

### 1. Minimo privilegio
```python
# MAL -- agente con acceso total
agent = Agent(permissions=["read", "write", "execute", "admin"])

# BIEN -- agente con solo lo necesario
agent = Agent(permissions=["read_logs"])
```

### 2. Humano en el circuito (Human-in-the-Loop)
```python
def execute_action(action):
    if action.severity in ("HIGH", "CRITICAL"):
        approved = request_human_approval(action)
        if not approved:
            return False
    return perform_action(action)
```

### 3. Sanitizacion anti-GhostJacking
```python
import re

def sanitize_logs_for_llm(log_content):
    # Eliminar HTML comments
    clean = re.sub(r'<!--.*?-->', '[LOG_COMMENT_REMOVED]', log_content, flags=re.DOTALL)
    # Eliminar patrones de injection conocidos
    patterns = [
        r'(?i)ignore.{0,30}previous.{0,30}instructions?',
        r'(?i)system\s+override',
        r'(?i)\[agent\s+(instruction|command|override)',
        r'(?i)you are now (in|a|an)',
    ]
    for p in patterns:
        clean = re.sub(p, '[INJECTION_REMOVED]', clean, flags=re.IGNORECASE)
    return clean[:5000]  # limitar tamano
```

---

## Checklist de seguridad para agentes IA

```
Diseno:
[ ] Principio de minimo privilegio en permisos del agente
[ ] Human-in-the-loop para acciones de alta severidad
[ ] Timeout y limites de tokens en llamadas al LLM

Input:
[ ] Sanitizacion de logs antes de pasarlos al LLM
[ ] Deteccion de patrones de prompt injection
[ ] Limitar longitud de campos

Output:
[ ] Validacion del output del LLM antes de ejecutar acciones
[ ] Lista blanca de acciones permitidas
[ ] Logging de todas las acciones del agente

Monitoreo:
[ ] Alertar sobre injections detectadas en logs
[ ] Monitorizar acciones anomalas del agente
[ ] Auditorias periodicas
```

---

## Herramientas de defensa

```bash
pip install rebuff           # deteccion de prompt injection
pip install nemoguardrails   # rails de seguridad NVIDIA
pip install garak            # red teaming automatizado
# Azure Prompt Shield: azure.microsoft.com/services/ai-services/prompt-shield
```
