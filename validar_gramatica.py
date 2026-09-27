# Lógica para validar la gramática

# Traemos las constantes y funciones de tokenizar.py para clasificar los tokens.
from tokenizar import (
    clasificar,
    NOTERMINAL,
    TERMINAL,
    FLECHA,
    INFIJO,
    TIPO_EPSILON,
)


def validar_expresion(tokens):
    if not tokens:
        return False, "La producción está vacía"

    # Clasificar los tokens
    try:
        tipos = [clasificar(token) for token in tokens]
    except ValueError as error:
        return False, str(error)

    # Debe existir exactamente una flecha
    if tipos.count(FLECHA) != 1:
        return False, "La producción debe contener exactamente una flecha"

    posicion_flecha = tipos.index(FLECHA)

    # Antes de la flecha debe haber exactamente una mayúscula
    if posicion_flecha != 1 or tipos[0] != NOTERMINAL:
        return False, (
            "A la izquierda de la flecha debe haber solo un símbolo en mayúscula"
        )

    # Debe existir un cuerpo después de la flecha
    if posicion_flecha == len(tokens) - 1:
        return False, (
            "Falta el cuerpo de la producción"
        )

    # Acumular los tipos de cada lado separada por '|'.
    alt = []

    for idx in range(posicion_flecha + 1, len(tokens)):
        tipo = tipos[idx]

        if tipo == INFIJO:
            # Rechaza un '|' inicial o dos '|' consecutivos.
            if not alt:
                return False, (
                    f"El '|' en la posición {idx + 1} "
                    "deberia tener algo a su izquierda"
                )

            alt = []

        elif tipo in (TERMINAL, NOTERMINAL, TIPO_EPSILON):
            # Épsilon debe aparecer solo
            if (
                tipo == TIPO_EPSILON and alt
            ) or TIPO_EPSILON in alt:
                return False, (
                    "ε debe aparecer solito"
                )

            alt.append(tipo)

        else:
            return False, (
                f"Símbolo inesperado {tokens[idx]!r} "
                f"en la posición {idx + 1}."
            )

    # Rechaza un '|' al final
    if not alt:
        return False, (
            "El último '|' deberia tener una aletrnativa a su derecha"
        )

    return True, None