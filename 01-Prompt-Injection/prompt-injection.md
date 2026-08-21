# Prompt Injection

OWASP LLM01

## Tipos

### Direct
El atacante accede directamente al LLM.

### Indirect
El atacante envenena datos que el LLM procesara (documentos, logs, paginas web).

### GhostJacking
Ver modulo 02-GhostJacking.

## Payloads



## Mitigacion

- Sanitizar inputs antes de pasarlos al LLM
- Validar outputs antes de ejecutar acciones
- Principio de minimo privilegio para agentes
- Human-in-the-loop para acciones sensibles
