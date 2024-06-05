import json
from jugador import Jugador

class ManejJugadores:
    indice = 0

    def __init__(self, archivo='pysimonpuntajes.json'):
        self.__jugadores = []
        self.archivo = archivo
        self.cargar_datos()

    def cargar_datos(self):
        try:
            with open(self.archivo, 'r') as file:
                datos = json.load(file)
                for jugador_data in datos.get('jugadores', []):
                    atributos = jugador_data['__atributos__']
                    jugador = Jugador(**atributos)
                    self.__jugadores.append(jugador)
                    rowid = atributos.get('rowid', None)
                    if rowid is not None and rowid >= ManejJugadores.indice:
                        ManejJugadores.indice = rowid + 1
        except FileNotFoundError:
            self.__jugadores = []

    def agregar(self, jugador):
        jugador.rowid = ManejJugadores.indice
        ManejJugadores.indice += 1
        self.__jugadores.append(jugador)
        self.guardarEnArchivo()

    def getLista(self):
        return self.__jugadores

    def deleteJugador(self, jugador):
        indice = self.obtenerIndiceJugador(jugador)
        self.__jugadores.pop(indice)
        self.guardarEnArchivo()

    def obtenerIndiceJugador(self, jugador):
        for i, j in enumerate(self.__jugadores):
            if j.rowid == jugador.rowid:
                return i
        return -1

    def toJSON(self):
        return {
            '__class__': self.__class__.__name__,
            'jugadores': [jugador.toJSON() for jugador in self.__jugadores]
        }

    def guardarEnArchivo(self):
        with open(self.archivo, 'w') as file:
            json.dump(self.toJSON(), file, indent=4)