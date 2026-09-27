# Laboratorio 7

## Problema 1: eliminación de producciones épsilon

Programa en Python que carga gramáticas desde archivos de texto, valida sus producciones y elimina las producciones épsilon (`ε`). Durante la ejecución muestra los símbolos anulables, las combinaciones consideradas y la gramática resultante.

## Archivos

| Archivo | Función |
| --- | --- |
| `main.py` | Lee los archivos, muestra y valida las gramáticas y ejecuta la eliminación de épsilon. |
| `tokenizar.py` | Reconoce terminales, no terminales, flechas, OR y épsilon. |
| `validar_gramatica.py` | Verifica la estructura de cada producción. |
| `eliminar_epsilon.py` | Encuentra anulables y genera las variantes sin producciones épsilon. |
| `gramatica1.txt` | Primera gramática de entrada. |
| `gramatica2.txt` | Segunda gramática de entrada. |

## Ejecución
1. Descargar o clonar el repositorio.
2. Colocar los archivos de gramáticas en la misma carpeta que `main.py`.
3. Abrir una terminal en esa carpeta y ejecutar:

```bash
python main.py
```

Los archivos que se procesan se indican al final de `main.py`:

```python
gramaticas = cargararchivo(["gramatica1.txt", "gramatica2.txt"])
```

Para cargar otros archivos, modificar esa lista. Cada archivo representa una gramática independiente y la primera cabeza de producción se toma como símbolo inicial.

## Formato de las gramáticas

Cada línea no vacía contiene una cabeza, una flecha y una o varias alternativas separadas por `|`.

```text
S -> 0A0 | 1B1 | BB
A -> C
B -> S | A
C -> S | ε
```

- Las letras individuales `A-Z` representan no terminales.
- Las letras individuales `a-z` y los dígitos representan terminales.
- Se aceptan las flechas `->` y `→`.
- Se aceptan `ε` y `ϵ`, que se normalizan a `ε`.
- Se ignoran espacios y líneas vacías.
- Épsilon debe ocupar una alternativa completa.
- Los símbolos adicionales admitidos por el tokenizador, como `+`, se interpretan como terminales literales, no como operadores de expresiones regulares.
- Si una cabeza aparece en varias líneas, sus alternativas se agrupan y se evitan duplicados.

Los archivos deben guardarse con codificación UTF-8.


## Validación

Se adapta la estructura de tokenización y validación por tipos de tokens empleada en el proyecto y labs anteriores. La validación se realiza mediante código, sin una expresión regular de reconocimiento global.

Para cada línea se verifica que:
1. Exista exactamente una flecha.
2. A la izquierda haya un único símbolo en mayúscula.
3. A la derecha exista un cuerpo de producción.
4. Cada `|` tenga alternativas no vacías a ambos lados.
5. Épsilon no esté acompañado por otros símbolos dentro de su alternativa.
6. Los símbolos sean reconocidos por el tokenizador.

Ante una producción incorrecta indica el archivo, la línea y el motivo, detiene la carga y no ejecuta la eliminación de épsilon.


## Alcance

Esta versión elimina todas las producciones épsilon. Si el símbolo inicial era anulable, el resultado conserva las cadenas no vacías del lenguaje original, pero deja de generar la cadena vacía. el programa lo informa.

No se implementa eliminación de producciones unitarias, eliminación de símbolos inútiles ni conversión a Forma Normal de Chomsky.

## Video de demostración




