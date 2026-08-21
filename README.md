# 🤖 Ciber-AI — AI Security & Red Teaming

<p align="center">
  <img src="https://img.shields.io/badge/AI%20Security-Red%20Team-red?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/OWASP-LLM%20Top%2010-blue?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/GhostJacking-Lab%20Propio-orange?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge"/>
</p>

<p align="center">
  <b>AI Red Teaming — atacar y defender sistemas de Inteligencia Artificial.</b><br/>
  GhostJacking, Prompt Injection, RAG Poisoning, Jailbreaking y Model Extraction.<br/>
  Lab funcional con agente IA vulnerable y scripts de ataque y defensa.
</p>

---

## Por que AI Security?

Los agentes de IA procesan logs, emails, documentos y datos externos.
Un atacante que controla esos datos puede **controlar al agente**.
El WAF protege el servidor. Los logs lo traicionan.

> *"Los agentes de IA son tan seguros como los datos que leen."*

---

## GhostJacking — El ataque estrella

```
  Atacante ──► envia request con prompt injection oculto
      |
      v
  [WAF] ──► BLOQUEADO (el WAF hace su trabajo)
      |
      v
  [LOGS] ──► registra la request bloqueada (incluyendo el payload)
      |
      v
  [Agente IA] ──► lee los logs para "analizar amenazas"
      |           encuentra el prompt injection en los logs
      v
  [Acciones] ──► crear usuario / cambiar config / exfiltrar datos
                 El WAF no pudo proteger al agente
```

**El vector de ataque son los propios logs de seguridad.**

---

## Modulos

| # | Modulo | Tecnica | OWASP LLM |
|---|--------|---------|-----------|
| 01 | [Prompt Injection](01-Prompt-Injection/) | Direct, Indirect, Virtualizacion | LLM01 |
| 02 | [GhostJacking](02-GhostJacking/) | Log injection, Telemetry poisoning | LLM01 |
| 03 | [RAG Poisoning](03-RAG-Poisoning/) | Vector DB injection, Document poisoning | LLM04 |
| 04 | [Jailbreaking](04-Jailbreaking/) | DAN, Role-play, Token manipulation | LLM01 |
| 05 | [Model Extraction](05-Model-Extraction/) | Training data, Membership inference | LLM02 |
| 06 | [AI Red Teaming](06-AI-Red-Teaming/) | Metodologia, OWASP LLM Top 10 | Todos |
| 07 | [Defensa](07-Defensa/) | Input sanitization, Output validation | Todos |

---

## Lab funcional

El directorio `lab/` contiene un entorno completo y autocontenido:

```bash
# Instalar dependencias
pip install flask requests colorama

# Terminal 1 -- Lanzar el servidor web vulnerable
python3 lab/vulnerable_agent/webserver.py

# Terminal 2 -- Lanzar el agente IA vulnerable (lee los logs)
python3 lab/vulnerable_agent/agent.py

# Terminal 3 -- Ejecutar el ataque GhostJacking
python3 02-GhostJacking/scripts/ghostjack_attack.py --target http://localhost:5000

# Observar como el agente ejecuta las instrucciones del atacante
# aunque el WAF bloqueo la request original
```

---

## OWASP LLM Top 10 (2025)

| ID | Vulnerabilidad | Modulo |
|----|---------------|--------|
| LLM01 | Prompt Injection | 01, 02, 04 |
| LLM02 | Sensitive Information Disclosure | 05 |
| LLM03 | Supply Chain | 06 |
| LLM04 | Data and Model Poisoning | 03 |
| LLM05 | Improper Output Handling | 07 |
| LLM06 | Excessive Agency | 02 (GhostJacking) |
| LLM07 | System Prompt Leakage | 04 |
| LLM08 | Vector and Embedding Weaknesses | 03 |
| LLM09 | Misinformation | 06 |
| LLM10 | Unbounded Consumption | 06 |

---

## Herramientas

| Herramienta | Uso |
|-------------|-----|
| **Garak** | Framework de red teaming para LLMs |
| **PyRIT** | Microsoft AI Red Team toolkit |
| **PromptBench** | Evaluacion de robustez de LLMs |
| **LLM Fuzzer** | Fuzzing de modelos de lenguaje |
| **Rebuff** | Deteccion de prompt injection |

---

*Constan4 -- AI Security / Red Team*
