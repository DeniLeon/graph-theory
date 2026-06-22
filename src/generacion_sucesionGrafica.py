# Proyecto 2: Generar un grafo dada una sucesión gráfica
import tkinter as tk
from tkinter import messagebox

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Esta función verifica si la sucesión ingresada es gráfica
def es_sucesion_grafica(sucesion):

    return nx.is_graphical(sucesion, method="hh")


# Esta función genera el grafo usando Havel-Hakimi
def generar_grafo_sucesion(sucesion):

    # Primero se revisa si la sucesión sí es gráfica
    if not es_sucesion_grafica(sucesion):
        raise ValueError("La sucesión ingresada no es gráfica.")

    # Si la sucesión es válida, NetworkX genera el grafo
    G = nx.havel_hakimi_graph(sucesion)

    return G


# Esta función convierte el texto de entrada en una lista de enteros
def convertir_sucesion(texto):

    # Se eliminan espacios al inicio y al final
    texto = texto.strip()

    # Si el usuario no escribe nada, se marca error
    if texto == "":
        raise ValueError("Debes ingresar una sucesión de grados.")

    # Se separa el texto usando comas
    partes = texto.split(",")

    sucesion = []

    # Se convierte cada parte a número entero
    for parte in partes:
        numero = int(parte.strip())

        # Los grados no pueden ser negativos
        if numero < 0:
            raise ValueError("Los grados no pueden ser negativos.")

        sucesion.append(numero)

    return sucesion


# Esta función genera un resumen breve del grafo
def obtener_informacion(G, sucesion):

    n = G.number_of_nodes()
    m = G.number_of_edges()

    grados = dict(G.degree())
    grados_ordenados = sorted(grados.values(), reverse=True)

    suma_grados = sum(sucesion)

    if n > 0:
        grado_promedio = suma_grados / n
    else:
        grado_promedio = 0

    if n > 0:
        componentes = nx.number_connected_components(G)
    else:
        componentes = 0

    texto = (
        f"Sucesión ingresada: {sucesion}\n"
        f"Sucesión obtenida: {grados_ordenados}\n\n"
        f"Número de nodos |V|: {n}\n"
        f"Número de aristas |E|: {m}\n"
        f"Suma de grados: {suma_grados}\n"
        f"Grado promedio: {grado_promedio:.2f}\n"
        f"Componentes conexas: {componentes}\n"
    )

    return texto


# Clase principal de la interfaz
class AppSucesionGrafica:

    def __init__(self, root):

        self.root = root
        self.root.title("Generador de grafos por sucesión gráfica")
        self.root.geometry("1050x720")
        self.root.minsize(900, 600)

        # Aquí se guarda el grafo generado
        self.G = None

        # Se crea la interfaz
        self.crear_interfaz()

    def crear_interfaz(self):

        # Título de la ventana
        titulo = tk.Label(
            self.root,
            text="Generar un grafo dada una sucesión gráfica",
            font=("Arial", 16, "bold")
        )
        titulo.pack(pady=10)

        # Marco para los datos de entrada
        marco_entrada = tk.LabelFrame(
            self.root,
            text="Datos de entrada",
            padx=10,
            pady=10
        )
        marco_entrada.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        # Etiqueta de la sucesión
        tk.Label(
            marco_entrada,
            text="Sucesión de grados:",
            font=("Arial", 11)
        ).grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Entrada donde el usuario escribe la sucesión
        self.entry_sucesion = tk.Entry(marco_entrada, width=45)
        self.entry_sucesion.insert(0, "3, 3, 2, 2, 2")
        self.entry_sucesion.grid(row=0, column=1, padx=5, pady=5)

        # Botón para generar el grafo
        boton_generar = tk.Button(
            marco_entrada,
            text="Generar grafo",
            width=16,
            command=self.generar_grafo
        )
        boton_generar.grid(row=0, column=2, padx=10, pady=5)

        # Botón para limpiar la interfaz
        boton_limpiar = tk.Button(
            marco_entrada,
            text="Limpiar",
            width=12,
            command=self.limpiar
        )
        boton_limpiar.grid(row=0, column=3, padx=5, pady=5)

        # Texto pequeño de ayuda
        ayuda = tk.Label(
            marco_entrada,
            text="Escribe los grados separados por comas .Ejemplo : 3, 3, 2, 2, 2",
            font=("Arial", 9)
        )
        ayuda.grid(row=1, column=0, columnspan=4, padx=5, pady=3, sticky="w")

        # Marco principal para gráfica e información
        marco_central = tk.Frame(self.root)
        marco_central.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Marco donde se dibuja el grafo
        marco_grafica = tk.LabelFrame(
            marco_central,
            text="Grafo generado",
            padx=5,
            pady=5
        )
        marco_grafica.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Figura de matplotlib
        self.fig, self.ax = plt.subplots(figsize=(7, 5))

        # Se coloca la figura dentro de tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=marco_grafica)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        # Estado inicial del área de dibujo
        self.ax.set_title("Grafo generado")
        self.ax.axis("off")
        self.canvas.draw()

        # Marco para información breve
        marco_info = tk.LabelFrame(
            self.root,
            text="Información del grafo",
            padx=10,
            pady=8
        )
        marco_info.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=8)

        # Cuadro de texto para mostrar información
        self.texto_info = tk.Text(
            marco_info,
            height=6,
            font=("Arial", 10)
        )
        self.texto_info.pack(fill=tk.X)

        # Mensaje inicial
        self.texto_info.insert(
            tk.END,
            "Ingresa una sucesión gráfica y presiona 'Generar grafo'."
        )

    def generar_grafo(self):

        try:
            # Se toma el texto escrito por el usuario
            texto = self.entry_sucesion.get()

            # Se convierte el texto en una lista de enteros
            sucesion = convertir_sucesion(texto)

            # Se genera el grafo
            self.G = generar_grafo_sucesion(sucesion)

            # Se dibuja el grafo
            self.dibujar_grafo(self.G, sucesion)

            # Se muestra información breve
            informacion = obtener_informacion(self.G, sucesion)
            self.actualizar_info(informacion)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error\n{e}")

    def dibujar_grafo(self, G, sucesion):

        # Se limpia el dibujo anterior
        self.ax.clear()

        n = G.number_of_nodes()

        # Se calculan posiciones para los nodos
        pos = nx.spring_layout(G, seed=42, k=1.1, iterations=100)

        # Se ajusta el tamaño para que grafos grandes no se vean tan saturados
        if n <= 10:
            node_size = 650
            font_size = 10
            edge_width = 1.2
        elif n <= 25:
            node_size = 420
            font_size = 8
            edge_width = 1.0
        elif n <= 60:
            node_size = 230
            font_size = 6
            edge_width = 0.8
        else:
            node_size = 110
            font_size = 4
            edge_width = 0.6

        # Se dibuja el grafo
        nx.draw(
            G,
            pos,
            ax=self.ax,
            with_labels=True,
            node_size=node_size,
            node_color="#8ecae6",
            edge_color="gray",
            font_size=font_size,
            width=edge_width
        )

        # Se coloca un título con datos principales
        self.ax.set_title(
            f"Grafo generado \n"
            f"|V| = {G.number_of_nodes()}, |E| = {G.number_of_edges()}",
            fontsize=11
        )

        self.ax.axis("off")
        self.canvas.draw()

    def actualizar_info(self, texto):

        # Se borra la información anterior
        self.texto_info.delete("1.0", tk.END)

        # Se escribe la nueva información
        self.texto_info.insert(tk.END, texto)

    def limpiar(self):

        # Se borra el grafo guardado
        self.G = None

        # Se limpia la gráfica
        self.ax.clear()
        self.ax.set_title("Grafo generado")
        self.ax.axis("off")
        self.canvas.draw()

        # Se limpia la información
        self.texto_info.delete("1.0", tk.END)
        self.texto_info.insert(
            tk.END,
            "Ingresa una sucesión gráfica y selecciona 'Generar grafo'."
        )

# Programa principal
if __name__ == "__main__":

    root = tk.Tk()
    app = AppSucesionGrafica(root)
    root.mainloop()