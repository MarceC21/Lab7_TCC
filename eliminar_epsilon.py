# Lógica para quitar producciones ε de una gramática


# Para generar los grupos de posiciones que vamos a quitar
def generar_combinaciones(posiciones, cuantos):
    resultado = []

    def construir(inicio, actual):
        # Ya seleccionamos la cantidad solicitada.
        if len(actual) == cuantos:
            resultado.append(tuple(actual))
            return

        for i in range(inicio, len(posiciones)):
            # Elegir esta posición.
            actual.append(posiciones[i])

            # Buscar la siguiente a partir de i + 1.
            construir(i + 1, actual)

            # Deshacer la elección para probar otra.
            actual.pop()

    construir(0, [])
    return resultado

# 
def texto_cuerpo(cuerpo):
    return "".join(cuerpo) if cuerpo else "ε"


# 1. Primero se encuentran los símbolos anulables, es decir, aquellos que pueden producir ε.
def encontrar_anulables(producciones):
    anulables = set()

    print("\nPASO 1: Encontrar símbolos anulables")

    # Anulables directos: tienen una alternativa vacía
    for cabeza, alternativas in producciones.items():
        if () in alternativas:
            anulables.add(cabeza)
            print(f"  {cabeza} es anulable porque {cabeza} → ε")

    # Anulables indirectos: tienen una alternativa formada únicamente por símbolos que ya son anulables
    cambios = True

    while cambios:
        cambios = False

        for cabeza, alternativas in producciones.items():
            if cabeza in anulables:
                continue

            for cuerpo in alternativas:
                if cuerpo and all(
                    simbolo in anulables for simbolo in cuerpo
                ):
                    anulables.add(cabeza)
                    cambios = True

                    print(
                        f"  {cabeza} es anulable porque "
                        f"{cabeza} → {texto_cuerpo(cuerpo)} "
                        "y todos los símbolos del cuerpo son anulables."
                    )
                    break

    print(
        "  Símbolos anulables:",
        ", ".join(sorted(anulables)) if anulables else "ninguno"
    )

    return anulables

#2. Luego se generan todas las variantes de las producciones, quitando los símbolos anulables 
def eliminar_epsilon(gramatica):
    producciones = gramatica["producciones"]
    anulables = encontrar_anulables(producciones)

    # Para no modificar la gramática original
    nuevas_producciones = {
        cabeza: [] for cabeza in producciones
    }

    print("\nPASO 2: Generar variantes y quitar producciones ε")

    for cabeza, alternativas in producciones.items():
        destino = nuevas_producciones[cabeza]

        for cuerpo in alternativas:
            if not cuerpo:
                print(f"\n  Se elimina {cabeza} → ε")
                continue

            print(f"\n  Revisando {cabeza} → {texto_cuerpo(cuerpo)}")

            # Identificar POSICIONES, porque un símbolo puede repetirse
            posiciones = [
                indice
                for indice, simbolo in enumerate(cuerpo)
                if simbolo in anulables
            ]

            cantidad = len(posiciones)

            print(
                f"  {cantidad} posiciones anulables: "
                f"2^{cantidad} = {2 ** cantidad} combinaciones."
            )

            # Desde no quitar nada hasta quitar todas las
            # posiciones anulables.
            for cuantos in range(cantidad + 1):
                for quitar in generar_combinaciones(posiciones, cuantos):
                    nuevo_cuerpo = tuple(
                        simbolo
                        for indice, simbolo in enumerate(cuerpo)
                        if indice not in quitar
                    )

                    if quitar:
                        detalle = ", ".join(
                            f"{cuerpo[indice]} en posición {indice + 1}"
                            for indice in quitar
                        )
                        accion = f"Quitar {detalle}"
                    else:
                        accion = "Conservar el cuerpo original"

                    resultado = (
                        f"{cabeza} → {texto_cuerpo(nuevo_cuerpo)}"
                    )

                    # No guardar ninguna producción vacía.
                    if not nuevo_cuerpo:
                        print(
                            f"    {accion}: {resultado} "
                            "(se descarta ε)"
                        )

                    elif nuevo_cuerpo in destino:
                        print(
                            f"    {accion}: {resultado} "
                            "(ya existe)"
                        )

                    else:
                        destino.append(nuevo_cuerpo)
                        print(
                            f"    {accion}: {resultado} "
                            "(se guarda)"
                        )

    if gramatica["inicial"] in anulables:
        print(
            "\nEl símbolo inicial era anulable. "
            "Al quitar todas las producciones ε, "
            "la gramática conserva las cadenas no vacías, "
            "pero deja de generar la cadena vacía."
        )

    return {
        "archivo": gramatica["archivo"],
        "inicial": gramatica["inicial"],
        "producciones": nuevas_producciones,
    }