# Proyecto: Algoritmo de Prim , encontrar el árbol de expansión mínima de un grafo ponderado

import networkx as nx
import matplotlib.pyplot as plt


# Aplica el algoritmo de Prim
def prim(G, nodo_inicio):

    # Lista donde se guardan las aristas seleccionadas
    arbol_minimo = []

    # Aquí se acumula el peso total del árbol
    peso_total = 0

    # Conjunto de nodos que ya forman parte del árbol
    visitados = set()

    # Se agrega el nodo inicial al conjunto de visitados
    visitados.add(nodo_inicio)

    # Mientras no se hayan visitado todos los nodos
    while len(visitados) < G.number_of_nodes():

        # Aquí se guarda la mejor arista encontrada en cada paso
        mejor_arista = None

        # Aquí se guarda el menor peso encontrado
        menor_peso = float("inf")

        # Se revisan todas las aristas que salen de los nodos visitados
        for u in visitados:

            # Se revisan los vecinos del nodo u
            for v in G.neighbors(u):

                # Solo nos interesan vecinos que todavía no estén en el árbol
                if v not in visitados:

                    # Se obtiene el peso de la arista
                    peso = G[u][v]["weight"]

                    # Si el peso es menor al mejor encontrado, se actualiza
                    if peso < menor_peso:
                        menor_peso = peso
                        mejor_arista = (u, v, peso)

        # Si no se encontró arista, el grafo no es conexo
        if mejor_arista is None:
            raise ValueError("El grafo no es conexo. No se puede aplicar Prim.")

        # Se obtiene la mejor arista
        u, v, peso = mejor_arista

        # Se agrega la arista al árbol mínimo
        arbol_minimo.append((u, v, peso))

        # Se suma el peso
        peso_total += peso

        # Se marca el nuevo nodo como visitado
        visitados.add(v)

    return arbol_minimo, peso_total


# Permite al usuario ingresar el grafo por consola
def ingresar_grafo():

    # Se crea un grafo vacío
    G = nx.Graph()

    # Esta lista guarda las aristas para mostrarlas en el resumen
    aristas_ingresadas = []

    print("Ingresa las aristas del grafo.")
    print("Formato: nodo1 nodo2 peso")
    print("Ejemplo: A B 4")
    print("Escribe 'fin' para terminar.\n")

    while True:

        # Se pide una arista al usuario
        entrada = input("Arista: ")

        # Si el usuario escribe fin, termina la captura
        if entrada.lower() == "fin":
            break

        # Se separa la entrada por espacios
        partes = entrada.split()

        # Cada arista debe tener tres datos
        if len(partes) != 3:
            print("Entrada inválida. Usa el formato: nodo1 nodo2 peso")
            continue

        # Se toman los dos nodos
        nodo1 = partes[0]
        nodo2 = partes[1]

        try:
            # Se convierte el peso a número decimal
            peso = float(partes[2])

        except ValueError:
            print("El peso debe ser un número.")
            continue

        # Se agrega la arista al grafo
        G.add_edge(nodo1, nodo2, weight=peso)

        # Se guarda la arista ingresada para el resumen
        aristas_ingresadas.append((nodo1, nodo2, peso))

    return G, aristas_ingresadas


# Pide al usuario el nodo inicial para Prim
def pedir_nodo_inicio(G):

    print("\nNodos disponibles:")
    print(list(G.nodes()))

    nodo_inicio = input("Ingresa el nodo inicial para Prim: ")

    # Se verifica que el nodo exista en el grafo
    if nodo_inicio not in G.nodes():
        raise ValueError("El nodo inicial no existe en el grafo.")

    return nodo_inicio


# Muestra el resultado en consola
def mostrar_resultado(arbol_minimo, peso_total, nodo_inicio):

    print(f"\nNodo inicial: {nodo_inicio}")
    print("\nAristas seleccionadas por Prim:\n")

    for u, v, peso in arbol_minimo:
        print(f"{u} - {v}   peso: {peso}")

    print(f"\nPeso total del árbol de expansión mínima: {peso_total}")


# Construye el texto que aparecerá en la figura
def construir_resumen(aristas_ingresadas, arbol_minimo, peso_total, nodo_inicio):

    texto = "Aristas ingresadas:\n\n"

    for u, v, peso in aristas_ingresadas:
        texto += f"Arista: {u} {v} {peso}\n"

    texto += f"\nNodo inicial: {nodo_inicio}\n"

    texto += "\nAristas seleccionadas por Prim:\n\n"

    for u, v, peso in arbol_minimo:
        texto += f"{u} - {v}   peso: {peso}\n"

    texto += f"\nPeso total: {peso_total}"

    return texto


# Dibuja el grafo y el resumen en la misma figura
def dibujar_grafo_con_resumen(G, arbol_minimo, resumen):

    # Se calculan posiciones para los nodos
    pos = nx.spring_layout(G, seed=42)

    # Se guardan solo las aristas seleccionadas por Prim
    aristas_arbol = []

    for u, v, peso in arbol_minimo:
        aristas_arbol.append((u, v))

    # Se obtienen los pesos de las aristas
    etiquetas_pesos = nx.get_edge_attributes(G, "weight")

    # Se crea una figura con dos secciones
    fig, (ax1, ax2) = plt.subplots(
        1,
        2,
        figsize=(14, 7),
        gridspec_kw={"width_ratios": [2, 1]}
    )

    # Se dibujan los nodos
    nx.draw_networkx_nodes(
        G,
        pos,
        ax=ax1,
        node_size=800,
        node_color="#8ecae6"
    )

    # Se dibujan todas las aristas del grafo original
    nx.draw_networkx_edges(
        G,
        pos,
        ax=ax1,
        edge_color="lightgray",
        width=2
    )

    # Se resaltan las aristas del árbol mínimo
    nx.draw_networkx_edges(
        G,
        pos,
        ax=ax1,
        edgelist=aristas_arbol,
        edge_color="#023047",
        width=4
    )

    # Se dibujan las etiquetas de los nodos
    nx.draw_networkx_labels(
        G,
        pos,
        ax=ax1,
        font_size=11,
        font_weight="bold"
    )

    # Se dibujan los pesos de las aristas
    nx.draw_networkx_edge_labels(
        G,
        pos,
        ax=ax1,
        edge_labels=etiquetas_pesos,
        font_size=10
    )

    # Título del grafo
    ax1.set_title("Algoritmo de Prim\nÁrbol de expansión mínima")
    ax1.axis("off")

    # Se oculta el eje del resumen
    ax2.axis("off")

    # Título del resumen
    ax2.set_title("Resumen", fontsize=12)

    # Se coloca el texto del resumen
    ax2.text(
        0.0,
        1.0,
        resumen,
        transform=ax2.transAxes,
        fontsize=9,
        va="top",
        ha="left",
        family="monospace",
        wrap=True
    )

    plt.tight_layout()
    plt.show()


# Programa principal
if __name__ == "__main__":

    try:
        # El usuario ingresa el grafo
        G, aristas_ingresadas = ingresar_grafo()

        # Se verifica que se hayan ingresado aristas
        if G.number_of_edges() == 0:
            print("No se ingresaron aristas. No se puede aplicar Prim.")

        # Se verifica que el grafo sea conexo
        elif not nx.is_connected(G):
            print("El grafo no es conexo.")
            print("Prim necesita un grafo conexo para obtener un árbol de expansión mínima.")

        else:
            # Se pide el nodo inicial
            nodo_inicio = pedir_nodo_inicio(G)

            # Se aplica el algoritmo de Prim
            arbol_minimo, peso_total = prim(G, nodo_inicio)

            # Se muestra el resultado en consola
            mostrar_resultado(arbol_minimo, peso_total, nodo_inicio)

            # Se construye el resumen para la imagen
            resumen = construir_resumen(
                aristas_ingresadas,
                arbol_minimo,
                peso_total,
                nodo_inicio
            )

            # Se dibuja el grafo con su resumen
            dibujar_grafo_con_resumen(G, arbol_minimo, resumen)

    except ValueError as e:
        print(f"Error: {e}")