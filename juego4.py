import tkinter as tk
import random
import time
import pygame  # Librería para la música

# Lógica del juego
class Rompecabezas:
    def __init__(self, tamaño=4, columnas=5):
        self.tamaño = tamaño
        self.columnas = columnas
        self.tablero = self.generar_tablero()
        self.movimientos = 0
        self.seleccionado = None  # Para almacenar el botón seleccionado

    def generar_tablero(self):
        # Generar una lista de números del 1 al 20
        números = list(range(1, 21))  # Del 1 al 20
        random.shuffle(números)  # Desordenar los números
        tablero = [números[i:i + self.columnas] for i in range(0, len(números), self.columnas)]
        return tablero

    def mover(self, fila, col):
        # Si no se ha seleccionado un cuadro, lo seleccionamos
        if self.seleccionado is None:
            self.seleccionado = (fila, col)
        else:
            fila_sel, col_sel = self.seleccionado
            # Verificar si el movimiento es válido
            if abs(fila_sel - fila) + abs(col_sel - col) == 1:
                # Intercambiar las posiciones de los cuadros
                self.tablero[fila_sel][col_sel], self.tablero[fila][col] = self.tablero[fila][col], self.tablero[fila_sel][col_sel]
                self.movimientos += 1
            # Reiniciar la selección después de un movimiento
            self.seleccionado = None

    def esta_resuelto(self):
        # Verificar si el tablero está resuelto
        objetivo = list(range(1, 21))  # Los números del 1 al 20
        actual = [num for fila in self.tablero for num in fila]
        return actual == objetivo


# Interfaz gráfica con Tkinter
class InterfazJuego:
    def __init__(self, root, tamaño=4, columnas=5):
        self.root = root
        self.root.title("Rompecabezas de Números")
        self.root.config(bg="#E0BBE4")  # Fondo lila claro
        self.juego = None  # El juego se iniciará después de pasar la portada
        self.botones = {}
        self.tamaño = tamaño
        self.columnas = columnas
        self.botones_direcciones = {}

        # Iniciar la música
        pygame.mixer.init()
        pygame.mixer.music.load("eff.ms.mp3")  # Cargar el archivo de música
        pygame.mixer.music.play(-1)  # Reproducir la música en loop

        # Pantalla de portada
        self.mostrar_portada()

    def mostrar_portada(self):
        # Crear la pantalla de bienvenida
        self.portada_label = tk.Label(self.root, text="¡Bienvenido al Rompecabezas de Números!", font=("Arial", 20), bg="#E0BBE4")
        self.portada_label.grid(row=0, column=0, columnspan=self.columnas)

        # Crear el botón de "Siguiente"
        self.boton_siguiente = tk.Button(self.root, text="Siguiente", font=("Arial", 14), command=self.iniciar_juego, bg="#F39C12", width=12)
        self.boton_siguiente.grid(row=1, column=0, columnspan=self.columnas)

    def iniciar_juego(self):
        # Eliminar la pantalla de bienvenida
        self.portada_label.grid_forget()
        self.boton_siguiente.grid_forget()

        # Iniciar el juego
        self.juego = Rompecabezas(self.tamaño, self.columnas)
        self.crear_tablero()

        # Etiqueta de puntaje
        self.puntaje_label = tk.Label(self.root, text="Movimientos: 0", font=("Arial", 14), bg="#E0BBE4")
        self.puntaje_label.grid(row=self.tamaño, column=0, columnspan=self.columnas)

        # Botón de reinicio
        self.boton_reinicio = tk.Button(self.root, text="Reiniciar", font=("Arial", 14), command=self.reiniciar_juego, bg="#F39C12", width=12)
        self.boton_reinicio.grid(row=self.tamaño + 1, column=0, columnspan=self.columnas)

    def crear_tablero(self):
        # Crear botones para cada número
        for i in range(self.tamaño):
            for j in range(self.columnas):
                num = self.juego.tablero[i][j]
                btn = tk.Button(self.root, text=str(num), width=6, height=3,
                                bg="#E0BBE4", font=("Arial", 14),
                                command=lambda i=i, j=j: self.mover(i, j))
                btn.grid(row=i, column=j, padx=2, pady=2)
                self.botones[(i, j)] = btn

    def mover(self, fila, col):
        # Mover el número al adyacente si el movimiento es válido
        self.juego.mover(fila, col)
        self.actualizar_tablero()
        self.actualizar_puntaje()

        # Mostrar los botones de dirección después de seleccionar un cuadro
        self.mostrar_direcciones(fila, col)

    def mostrar_direcciones(self, fila, col):
        # Mostrar botones para mover el cuadro hacia arriba, abajo, izquierda o derecha
        for btn in self.botones_direcciones.values():
            btn.grid_forget()  # Ocultar los botones previos

        self.botones_direcciones.clear()

        direcciones = [
            ("Arriba", -1, 0), 
            ("Abajo", 1, 0), 
            ("Izquierda", 0, -1), 
            ("Derecha", 0, 1)
        ]

        for direccion, i, j in direcciones:
            nueva_fila = fila + i
            nueva_col = col + j
            if 0 <= nueva_fila < self.tamaño and 0 <= nueva_col < self.columnas:
                # Crear botones para cada dirección válida
                btn = tk.Button(self.root, text=direccion, width=10, height=2,
                                font=("Arial", 12), bg="#F39C12", 
                                command=lambda fila=fila, col=col, i=i, j=j: self.mover_direccion(fila, col, i, j))
                btn.grid(row=self.tamaño + 2, column=0, columnspan=self.columnas)
                self.botones_direcciones[direccion] = btn

    def mover_direccion(self, fila, col, i, j):
        # Mover el número en la dirección especificada
        nueva_fila = fila + i
        nueva_col = col + j
        self.juego.mover(nueva_fila, nueva_col)
        self.actualizar_tablero()
        self.actualizar_puntaje()

    def actualizar_tablero(self):
        # Actualizar los botones de acuerdo con el estado actual del tablero
        for i in range(self.tamaño):
            for j in range(self.columnas):
                num = self.juego.tablero[i][j]
                btn = self.botones[(i, j)]
                btn.config(text=str(num))  # Mantener el color lila

    def actualizar_puntaje(self):
        # Actualizar el puntaje
        self.puntaje_label.config(text=f"Movimientos: {self.juego.movimientos}")

    def mostrar_mensaje(self, mensaje):
        # Mostrar mensaje cuando el juego se resuelve
        mensaje_label = tk.Label(self.root, text=mensaje, font=("Arial", 16), bg="#E0BBE4")
        mensaje_label.grid(row=self.tamaño + 3, column=0, columnspan=self.columnas)
        # Deshabilitar todos los botones
        for btn in self.botones.values():
            btn.config(state="disabled")

    def mostrar_confeti(self):
        # Crear confeti con efectos visuales
        colores = ["#FF6347", "#FFD700", "#32CD32", "#1E90FF", "#8A2BE2"]
        for _ in range(50):
            x = random.randint(0, self.root.winfo_width())
            y = random.randint(0, self.root.winfo_height())
            color = random.choice(colores)
            confeti = tk.Label(self.root, text="*", font=("Arial", random.randint(10, 30)), fg=color)
            confeti.place(x=x, y=y)
            self.root.after(random.randint(100, 500), confeti.destroy)

    def reiniciar_juego(self):
        # Reiniciar el juego
        self.juego = Rompecabezas(self.tamaño, self.columnas)
        self.botones.clear()
        self.botones_direcciones.clear()
        for widget in self.root.winfo_children():
            widget.grid_forget()
        self.crear_tablero()
        self.puntaje_label.config(text="Movimientos: 0")
        self.boton_reinicio.grid(row=self.tamaño + 1, column=0, columnspan=self.columnas)

# Crear la ventana principal
root = tk.Tk()

# Inicializar la interfaz del juego
interfaz = InterfazJuego(root)

# Ejecutar la aplicación
root.mainloop()
