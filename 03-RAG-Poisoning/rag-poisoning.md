# RAG Poisoning -- Envenenamiento de Sistemas RAG

OWASP LLM04 | LLM08

## Que es RAG

Retrieval-Augmented Generation: el LLM busca documentos relevantes
en una base de datos vectorial antes de responder.

## El ataque

Inyectar documentos maliciosos en la base de conocimiento.
Cuando el usuario hace una pregunta legitima, el RAG recupera
el documento malicioso y el LLM sigue las instrucciones inyectadas.

## Ejemplo



## Defensa

- Validar documentos antes de indexar en el vector store
- Eliminar HTML comments e instrucciones directas al LLM
- Detectar patrones sospechosos en documentos
- Auditar periodicamente los documentos indexados
