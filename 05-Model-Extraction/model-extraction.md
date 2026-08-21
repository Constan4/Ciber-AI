# Model Extraction y Data Leakage

OWASP LLM02 | LLM07

## System Prompt Extraction

Extraer el system prompt confidencial del modelo.



## Training Data Extraction

El modelo puede memorizar datos de entrenamiento sensibles.



## Model Cloning

Robar el comportamiento del modelo via muchas consultas.



## Defensa

- No incluir secretos en el system prompt
- Rate limiting para prevenir extraccion sistematica
- Output filtering para datos sensibles
- Monitorizar patrones de consultas sospechosas
