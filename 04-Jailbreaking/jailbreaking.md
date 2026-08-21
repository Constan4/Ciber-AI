# Jailbreaking de LLMs

OWASP LLM01 | LLM07

## Tecnicas

### DAN (Do Anything Now)
Asumir un rol sin restricciones via role-playing.

### Virtualizacion
Situar la peticion en un contexto ficticio.

### Token Smuggling
Separar palabras clave: inst-ruct-ions, l33tspeak, base64.

### System Prompt Leakage
Extraer el system prompt confidencial del modelo.

## Herramientas



## Defensa

- Output moderation (OpenAI Moderation API)
- Constitutional AI
- NeMo Guardrails
- Rate limiting y deteccion de patrones
