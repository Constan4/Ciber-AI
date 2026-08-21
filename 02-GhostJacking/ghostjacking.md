# GhostJacking -- Prompt Injection via Logs

OWASP LLM01 + LLM06 | Publicado en 2025

## El ataque



El WAF protege. Los logs traicionan.

## Demo del laboratorio



## Deteccion



## Mitigacion

Sanitizar logs antes de pasarlos al agente:
- Eliminar HTML comments
- Truncar campos de datos a longitud maxima
- Detectar patrones de injection
- Validar que el input viene de fuentes de confianza
