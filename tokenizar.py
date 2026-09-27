# Tipos de token
NONE = "INICIO"
TERMINAL = "TERMINAL"
NOTERMINAL = "NO_TERMINAL"
FLECHA = "FLECHA"
INFIJO = "OPERADOR_OR"
TIPO_EPSILON = "EPSILON"

EPSILON = "ε"

# Símbolos adicionales que permitiremos como terminales.
TERMINALES_ESPECIALES = {"+", "-", "*", "?", ".", "(", ")", "[", "]", "{", "}"}


def clasificar(token):
    if token == "→":
        return FLECHA

    if token == "|":
        return INFIJO

    if token == EPSILON:
        return TIPO_EPSILON

    # Un símbolo escapado representa un terminal literal.
    # Por ejemplo: \| representa el carácter |, no el OR.
    if token.startswith("\\") and len(token) == 2:
        return TERMINAL

    if len(token) == 1:
        if "A" <= token <= "Z":
            return NOTERMINAL

        if "a" <= token <= "z" or "0" <= token <= "9":
            return TERMINAL

        if token in TERMINALES_ESPECIALES:
            return TERMINAL

    raise ValueError(f"Símbolo no reconocido: {token!r}")


def tokenizar(expr):
    tokens = []
    i = 0

    while i < len(expr):
        c = expr[i]

        # Ignorar espacios.
        if c.isspace():
            i += 1
            continue

        # Caracter escapado: se conserva como un solo token.
        if c == "\\":
            if i + 1 >= len(expr):
                raise ValueError(
                    f"Escape incompleto en la posición {i + 1}."
                )

            tokens.append(expr[i:i + 2])
            i += 2
            continue

        # Reconocer -> antes de procesar el '-' individual.
        if expr.startswith("->", i):
            tokens.append("→")
            i += 2
            continue

        # Normalizar las dos formas de escribir épsilon.
        if c in {"ε", "ϵ"}:
            tokens.append(EPSILON)
            i += 1
            continue

        # Verificar que sea un símbolo reconocido.
        try:
            clasificar(c)
        except ValueError:
            raise ValueError(
                f"Símbolo no reconocido {c!r} "
                f"en la posición {i + 1}."
            ) from None

        tokens.append(c)
        i += 1

    return tokens