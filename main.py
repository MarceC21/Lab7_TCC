from pathlib import Path

from tokenizar import tokenizar
from validar_gramatica import validar_expresion
from eliminar_epsilon import eliminar_epsilon


## Leer y validar una gramática desde un archivo.
def leer_gramatica(ruta):
    producciones = {}
    simbolo_inicial = None

    with ruta.open("r", encoding="utf-8-sig") as archivo:
        for numero_linea, linea in enumerate(archivo, start=1):
            expresion = linea.strip()

            # Ignorar líneas vacías.
            if not expresion:
                continue

            try:
                tokens = tokenizar(expresion)
            except ValueError as error:
                raise ValueError(
                    f"{ruta.name}, línea {numero_linea}: {error}\n"
                    f"  Producción: {expresion}"
                ) from None

            valida, error = validar_expresion(tokens)

            if not valida:
                raise ValueError(
                    f"{ruta.name}, línea {numero_linea}: {error}\n"
                    f"  Producción: {expresion}"
                )

            # La validación garantiza: cabeza, flecha, cuerpo.
            cabeza = tokens[0]

            if simbolo_inicial is None:
                simbolo_inicial = cabeza

            # Permitir que una cabeza aparezca en varias líneas.
            if cabeza not in producciones:
                producciones[cabeza] = []

            # Separar las alternativas del cuerpo.
            alternativa = []

            for token in tokens[2:]:
                if token == "|":
                    guardar_alternativa(
                        producciones[cabeza], alternativa
                    )
                    alternativa = []
                else:
                    alternativa.append(token)

            # Guardar la última alternativa.
            guardar_alternativa(producciones[cabeza], alternativa)

    if simbolo_inicial is None:
        raise ValueError(
            f"{ruta.name}: el archivo no contiene producciones."
        )

    return {
        "archivo": ruta.name,
        "inicial": simbolo_inicial,
        "producciones": producciones,
    }


def guardar_alternativa(destino, alternativa):
    # Representar épsilon como una tupla vacía.
    cuerpo = () if alternativa == ["ε"] else tuple(alternativa)

    # Evitar producciones duplicadas.
    if cuerpo not in destino:
        destino.append(cuerpo)


def mostrar_gramatica(gramatica):
    print(f"\nArchivo: {gramatica['archivo']}")
    print(f"Símbolo inicial: {gramatica['inicial']}")

    for cabeza, alternativas in gramatica["producciones"].items():
        cuerpos = [
            "".join(cuerpo) if cuerpo else "ε"
            for cuerpo in alternativas
        ]
        if cuerpos:
            print(f"{cabeza} → {' | '.join(cuerpos)}")
        else:
            print(f"{cabeza}: sin producciones")

# Procesa una lista de archivos y valida cada gramática
def procesararchivo(archivos):
    carpeta = Path(__file__).resolve().parent
    gramaticas = []

    for nombre in archivos:
        ruta = carpeta / nombre

        print(f"Archivo: {nombre}")

        try:
            # Mostrar el contenido antes de validarlo.
            contenido = ruta.read_text(encoding="utf-8-sig")

            print("Gramática:")
            print(contenido.strip() or "(Archivo vacío)")
            print()

            gramatica = leer_gramatica(ruta)

        except (OSError, UnicodeError) as error:
            print("No se pudo leer la gramática.")
            print(f"Motivo: {error}")
            print("Ejecución detenida.")
            return None

        except ValueError as error:
            print("GRAMÁTICA INVÁLIDA")
            print(f"Motivo: {error}")
            print("Ejecución detenida.")
            return None

        print("GRAMÁTICA VÁLIDA")
        print(f"Símbolo inicial: {gramatica['inicial']}")
        print()
        print()

        gramaticas.append(gramatica)

    print("\nTodas las gramáticas son válidas.")
    return gramaticas


gramaticas = procesararchivo(["gramatica1.txt", "gramatica2.txt"])

if gramaticas is not None:
    gramaticas_sin_epsilon = []

    for gramatica in gramaticas:
        print("\n" + "=" * 60)
        print(f"ELIMINAR ÉPSILON: {gramatica['archivo']}")
        print("=" * 60)

        resultado = eliminar_epsilon(gramatica)
        gramaticas_sin_epsilon.append(resultado)

        print("\nGRAMÁTICA SIN PRODUCCIONES ÉPSILON")
        mostrar_gramatica(resultado)