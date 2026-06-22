# Proyecto: Algoritmo Kruskal inverso  encontrar el árbol de expansión mínima de un grafo ponderado

import networkx as nx
import matplotlib.pyplot as plt


# En esta función aplicamos el algoritmo de Kruskal inverso
def kruskal_inverso(G):

    # Se crea una copia del grafo original
    # En esta copia se irán eliminando aristas
    arbol_minimo = G.copy()

    # Se obtienen todas las aristas con sus pesos
    aristas = []

    for u, v, datos in G.edges(data=True):
        peso = datos["weight"]
        aristas.append((u, v, peso))

    # Se ordenan las aristas de mayor a menor peso
    aristas.sort(key=lambda x: x[2], reverse=True)

    # Se revisan las aristas empezando por las más pesadas
    for u, v, peso in aristas:

        # Se elimina temporalmente la arista
        arbol_minimo.remove_edge(u, v)

        # Si el grafo sigue conexo, la arista se elimina definitivamente
        if nx.is_connected(arbol_minimo):
            pass

        # Si el grafo se desconecta, se vuelve a agregar la arista
        else:
            arbol_minimo.add_edge(u, v, weight=peso)

    # Se obtiene la lista final de aristas seleccionadas
    aristas_finales = []

    for u, v, datos in arbol_minimo.edges(data=True):
        peso = datos["weight"]
        aristas_finales.append((u, v, peso))

    # Se calcula el peso total del árbol mínimo
    peso_total = 0

    for u, v, peso in aristas_finales:
        peso_total += peso

    return aristas_finales, peso_total


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


# Muestra el resultado en consola
def mostrar_resultado(aristas_finales, peso_total):

    print("\nAristas seleccionadas por Kruskal inverso:\n")

    for u, v, peso in aristas_finales:
        print(f"{u} - {v}   peso: {peso}")

    print(f"\nPeso total del árbol de expansión mínima: {peso_total}")


# Construye el texto que aparecerá en la figura
def construir_resumen(aristas_ingresadas, aristas_finales, peso_total):

    texto = "Aristas ingresadas:\n\n"

    for u, v, peso in aristas_ingresadas:
        texto += f"Arista: {u} {v} {peso}\n"

    texto += "\nAristas seleccionadas por Kruskal inverso:\n\n"

    for u, v, peso in aristas_finales:
        texto += f"{u} - {v}   peso: {peso}\n"

    texto += f"\nPeso total: {peso_total}"

    return texto


# Dibuja el grafo y el resumen en la misma figura
def dibujar_grafo_con_resumen(G, aristas_finales, resumen):

    # Se calculan posiciones para los nodos
    pos = nx.spring_layout(G, seed=42)

    # Se guardan solo las aristas que quedaron en el árbol mínimo
    aristas_arbol = []

    for u, v, peso in aristas_finales:
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

    # Se resaltan las aristas que quedaron en el árbol mínimo
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
    ax1.set_title("Algoritmo de Kruskal inverso\nÁrbol de expansión mínima")
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

    # El usuario ingresa el grafo
    G, aristas_ingresadas = ingresar_grafo()

    # Se verifica que se hayan ingresado aristas
    if G.number_of_edges() == 0:
        print("No se ingresaron aristas. No se puede aplicar Kruskal inverso.")

    # Se verifica que el grafo sea conexo
    elif not nx.is_connected(G):
        print("El grafo no es conexo.")
        print("Kruskal inverso necesita un grafo conexo para obtener un árbol de expansión mínima.")

    else:
        # Se aplica el algoritmo de Kruskal inverso
        aristas_finales, peso_total = kruskal_inverso(G)

        # Se muestra el resultado en consola
        mostrar_resultado(aristas_finales, peso_total)

        # Se construye el resumen para la imagen
        resumen = construir_resumen(
            aristas_ingresadas,
            aristas_finales,
            peso_total
        )

        # Se dibuja el grafo con su resumen
        dibujar_grafo_con_resumen(G, aristas_finales, resumen)