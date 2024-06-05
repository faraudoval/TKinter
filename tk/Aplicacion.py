from tkinter import *
from tkinter import ttk
import random
from datetime import datetime
from manej_jugadores import ManejJugadores
from jugador import Jugador

class Aplicacion():
    def __init__(self, nombre_jugador, gestor):
        self.ventana = Tk()
        self.ventana.geometry('500x300')
        self.ventana.configure(bg='light blue')
        self.ventana.title('JugateYa - Simon')

        self.etiq = ttk.Label(self.ventana, text="Puntaje:")
        self.etiq.grid(row=0, column=1, columnspan=1, pady=10)

        self.nombre_label = ttk.Label(self.ventana, text=f"Jugador: {nombre_jugador}")
        self.nombre_label.grid(row=0, column=0, columnspan=1, pady=10, padx=10)
        
        #datos de jugador  y puntaje
        self.nombre_jugador = nombre_jugador
        self.gestor = gestor
        self.puntaje = 0
        self.puntaje_label = ttk.Label(self.ventana, text=f" {self.puntaje}")
        self.puntaje_label.grid(row=0, column=1, columnspan=2, pady=10, padx=10)
        # Etiqueta para el reloj
        self.tiempo = StringVar()
        self.tiempo.set("00:00")
        self.reloj = ttk.Label(self.ventana, textvariable=self.tiempo)
        self.reloj.grid(row=0, column=2, columnspan=2, pady=10, padx=10)
        #Etiquetas de fecha y hora
        ahora = datetime.now()
        self.fecha = ahora.strftime("%Y-%m-%d")
        self.hora = ahora.strftime("%H:%M:%S")

        self.fecha_label = ttk.Label(self.ventana, text=f"Fecha: {self.fecha}")
        self.fecha_label.grid(row=1, column=0, columnspan=1, pady=5)

        self.hora_label = ttk.Label(self.ventana, text=f"Hora: {self.hora}")
        self.hora_label.grid(row=2, column=0, columnspan=1, pady=5)

        self.tiempo_iniciado = False
        self.segundos = 0

    #botones canvas
        self.buttons = {
            "green": self.crear_boton(1, 1, "#00ff00"),
            "red": self.crear_boton(1, 2, "#ff0000"),
            "yellow": self.crear_boton(2, 1, "#ffff00"),
            "blue": self.crear_boton(2, 2, "#0000ff")
        }
    #boton salir
        self.boton_salir = Button(self.ventana, text='Salir', command=self.salir)
        self.boton_salir.grid(row=3, column=1, columnspan=1, pady=10)
    #listas
        self.secuencia = []
        self.secuencia_usuario = []

        self.ventana.mainloop()

    def crear_boton(self, row, col, color):
        canvas = Canvas(self.ventana, width=100, height=100, bg=color, relief='raised')
        canvas.grid(row=row, column=col, padx=5, pady=5)
        canvas.bind("<Button-1>", self.click)
        return canvas

    def activar_boton(self, canvas):
        original_color = canvas['bg']
        canvas.config(bg=self.cambiar_color(original_color))
        self.ventana.after(500, lambda: canvas.config(bg=original_color))

    def click(self, event):
        if not self.tiempo_iniciado:
            self.iniciar_juego(event)
            return

        canvas = event.widget
        color = canvas['bg']
        if color == "#00ff00":
            color = "green"
        elif color == "#ff0000":
            color = "red"
        elif color == "#ffff00":
            color = "yellow"
        elif color == "#0000ff":
            color = "blue"
        
        self.secuencia_usuario.append(color)
        self.activar_boton(canvas)
        self.chequear()

    def enable_buttons(self):
        for button in self.buttons.values():
            button.bind("<Button-1>", self.click)

    def disable_buttons(self):
        for button in self.buttons.values():
            button.unbind("<Button-1>")

    def cambiar_color(self, color):
        color_map = {
            "#00ff00": "#00cc00",
            "#ff0000": "#cc0000",
            "#ffff00": "#cccc00",
            "#0000ff": "#0000cc"
        }
        return color_map.get(color, color)

    def iniciar_juego(self, event):
        self.iniciar_reloj()
        self.secuencia = []
        self.secuencia_usuario = []
        self.puntaje = 0
        self.actualizaPuntaje()
        self.agregar_secuencia()

    def agregar_secuencia(self):
        self.disable_buttons()
        color = random.choice(list(self.buttons.keys()))
        self.secuencia.append(color)
        for i, color in enumerate(self.secuencia):
            self.ventana.after(1000 * (i + 1), lambda c=color: self.activar_boton(self.buttons[c]))
        self.ventana.after(1000 * (len(self.secuencia) + 1), self.enable_buttons)

    def chequear(self):
        if self.secuencia_usuario == self.secuencia:
            self.puntaje += 1
            self.actualizaPuntaje()
            self.secuencia_usuario = []
            self.agregar_secuencia()
        elif len(self.secuencia_usuario)==len(self.secuencia) and self.secuencia_usuario!=self.secuencia:
            print("Juego terminado, tu puntaje es: {}".format(self.puntaje))
            print(self.secuencia)
            print(self.secuencia_usuario)
            self.salir()

    def actualizaPuntaje(self):
        self.puntaje_label.config(text=f" {self.puntaje}")

    def iniciar_reloj(self):
        self.tiempo_iniciado = True
        self.actualizar_reloj()

    def actualizar_reloj(self):
        if self.tiempo_iniciado:
            self.segundos += 1
            minutos = self.segundos // 60
            segundos = self.segundos % 60
            self.tiempo.set(f"{minutos:02}:{segundos:02}")
            self.ventana.after(1000, self.actualizar_reloj)


    def salir(self):
        jugador = Jugador(self.nombre_jugador, self.fecha, self.hora, self.puntaje)
        self.gestor.agregar(jugador)
        self.ventana.destroy()
        Terminado(self.puntaje)

class Datos:
    def __init__(self, gestor):
        self.ventana = Tk()
        self.ventana.geometry('400x120')
        self.ventana.configure(bg='grey')
        self.ventana.title('JugateYa - Simon')

        self.gestor = gestor

        self.etiq = ttk.Label(self.ventana, text="Datos del jugador:")
        self.etiq1 = ttk.Label(self.ventana, text="Jugador:")

        self.jugador = StringVar()
        self.jugador.set('')
        self.ctext1 = ttk.Entry(self.ventana, textvariable=self.jugador, width=30)
        
        self.boton1 = ttk.Button(self.ventana, text="Iniciar Juego", padding=(5, 5), command=self.iniciar_juego)

        self.etiq.place(x=20, y=20)
        self.etiq1.place(x=30, y=40)
        self.ctext1.place(x=150, y=42)
        self.boton1.place(x=170, y=70)

    def iniciar_juego(self):
        nombre_jugador = self.jugador.get()
        self.ventana.destroy()
        Aplicacion(nombre_jugador, self.gestor)
class Terminado:
    def __init__(self, puntaje):
        self.ventana = Tk()
        self.ventana.geometry('400x120')
        self.ventana.configure(bg='orange')
        self.ventana.title('JugateYa - Simon')
        self.puntaje_label = ttk.Label(self.ventana, text=f"Juego terminado, tu puntaje es: {puntaje}")
        self.puntaje_label.place(x=70, y=40)
            
        #boton salir
        self.boton_salir = Button(self.ventana, text='Salir', command=self.salir)
        self.boton_salir.place(x=170, y=70)
        
    def salir(self):
        self.ventana.destroy()
def testAPP():
    gestor = ManejJugadores()
    datos = Datos(gestor)
    datos.ventana.mainloop()

if __name__ == '__main__':
    testAPP()