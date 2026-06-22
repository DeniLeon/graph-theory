# PROYECTO: GENERAR GRAFOS r-REGULARES DE ORDEN n
# Un grafo r-regular de orden n es un grafo que tiene: n nodos y todos los nodos con el mismo grado r

import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# FUNCIÓN PARA VALIDAR LOS PARÁMETROS
def validar_parametros(n, r):

    # El número de nodos debe ser positivo.
    # No se genera un grafo con 0 nodos.
    if n <= 0:
        raise ValueError("El número de nodos n debe ser mayor que 0.")

    # El grado r no puede ser negativo.
    # El grado de un nodo representa cuántas aristas llegan a él.
    if r < 0:
        raise ValueError("El grado r no puede ser negativo.")

    # En un grafo simple, r debe ser menor que n.
    # Si hay n nodos, cada nodo como máximo puede conectarse con n-1 nodos.
    if r >= n:
        raise ValueError("En un grafo simple, r debe ser menor que n.")

    # El producto n*r debe ser par.
    # Esto se debe a que la suma de grados de un grafo siempre es par.
    if (n * r) % 2 != 0:
        raise ValueError(
            "No existe un grafo r-regular con esos valores, "
            "porque n*r debe ser par."
        )


# FUNCIÓN PARA GENERAR EL GRAFO r-REGULAR
def generar_grafo_r_regular(n, r):

    # Primero se validan los parámetros.
    validar_parametros(n, r)

    # Se genera el grafo r-regular usando NetworkX.
    # d = grado de cada nodo
    # n = número de nodos
    G = nx.random_regular_graph(d=r, n=n)

    return G


# CLASE PRINCIPAL DE LA INTERFAZ
class AppGrafoRegular:

    def __init__(self, root):

        self.root = root

        self.root.title("Generador de grafos r-regulares")
        self.root.geometry("1000x700")
        self.root.minsize(850, 600)

        # Variable para guardar el grafo generado.
        self.G = None

        # Se crea la interfaz.
        self.crear_interfaz()

    def crear_interfaz(self):

        # Título principal.
        titulo = tk.Label(
            self.root,
            text="Generación de grafos r-regulares de orden n",
            font=("Arial", 16, "bold")
        )

        titulo.pack(pady=10)

        # Marco superior donde estarán los parámetros.
        marco_parametros = tk.LabelFrame(
            self.root,
            text="Parámetros del grafo",
            padx=10,
            pady=10
        )

        marco_parametros.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        # Etiqueta y entrada para n.
        tk.Label(
            marco_parametros,
            text="Orden n:",
            font=("Arial", 11)
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.entry_n = tk.Entry(marco_parametros, width=10)
        self.entry_n.insert(0, "8")
        self.entry_n.grid(row=0, column=1, padx=5, pady=5)

        # Etiqueta y entrada para r.
        tk.Label(
            marco_parametros,
            text="Grado r:",
            font=("Arial", 11)
        ).grid(
            row=0,
            column=2,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.entry_r = tk.Entry(marco_parametros, width=10)
        self.entry_r.insert(0, "3")
        self.entry_r.grid(row=0, column=3, padx=5, pady=5)

        # Botón para generar el grafo.
        boton_generar = tk.Button(
            marco_parametros,
            text="Generar grafo",
            width=18,
            command=self.generar_grafo
        )

        boton_generar.grid(row=0, column=4, padx=10, pady=5)

        # Botón para limpiar la gráfica.
        boton_limpiar = tk.Button(
            marco_parametros,
            text="Limpiar",
            width=12,
            command=self.limpiar
        )

        boton_limpiar.grid(row=0, column=5, padx=5, pady=5)

        # Marco central para la gráfica.
        marco_central = tk.Frame(self.root)
        marco_central.pack(
            side=tk.TOP,
            fill=tk.BOTH,
            expand=True,
            padx=10,
            pady=10
        )

        # Marco donde se muestra el grafo generado.
        marco_grafica = tk.LabelFrame(
            marco_central,
            text="Grafo generado",
            padx=5,
            pady=5
        )

        marco_grafica.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True,
            padx=5
        )

        # Se crea la figura de Matplotlib.
        self.fig, self.ax = plt.subplots(figsize=(7, 5))

        # Se inserta la figura dentro de la ventana de Tkinter.
        self.canvas = FigureCanvasTkAgg(self.fig, master=marco_grafica)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        # Estado inicial de la gráfica.
        self.ax.set_title("Grafo generado")
        self.ax.axis("off")
        self.canvas.draw()

    def generar_grafo(self):

        try:

            # Se leen los valores escritos por el usuario.
            n = int(self.entry_n.get())
            r = int(self.entry_r.get())

            # Se genera el grafo.
            self.G = generar_grafo_r_regular(n, r)

            # Se dibuja el grafo generado.
            self.dibujar_grafo(self.G, n, r)

        except ValueError as e:
            messagebox.showerror("Error en los parámetros", str(e))

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado:\n{e}")

    def dibujar_grafo(self, G, n, r):

        # Se limpia la gráfica anterior.
        self.ax.clear()

        # Se calculan las posiciones de los nodos.
        pos = nx.spring_layout(G, seed=42)

        # Se ajusta el tamaño de nodos y letras según el número de nodos.
        if n <= 15:
            node_size = 700
            font_size = 10
        elif n <= 40:
            node_size = 400
            font_size = 8
        else:
            node_size = 180
            font_size = 6

        # Se dibuja el grafo.
        nx.draw(
            G,
            pos,
            ax=self.ax,
            with_labels=True,
            node_size=node_size,
            node_color="#8ecae6",
            edge_color="gray",
            font_size=font_size,
            width=1.2
        )

        # Se agrega un título con la información principal.
        self.ax.set_title(
            f"Grafo {r}-regular de orden {n}\n"
            f"|V| = {G.number_of_nodes()}, |E| = {G.number_of_edges()}",
            fontsize=11
        )

        self.ax.axis("off")
        self.canvas.draw()

    def limpiar(self):

        # Se elimina el grafo guardado.
        self.G = None

        # Se limpia el área de dibujo.
        self.ax.clear()
        self.ax.set_title("Grafo generado")
        self.ax.axis("off")
        self.canvas.draw()


# PROGRAMA PRINCIPAL
if __name__ == "__main__":

    root = tk.Tk()
    app = AppGrafoRegular(root)
    root.mainloop()