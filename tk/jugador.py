class Jugador:
    def __init__(self, jugador, fecha, hora, puntaje, rowid=None):
        self.__jugador = jugador
        self.__fecha = fecha
        self.__hora = hora
        self.__puntaje = puntaje
        self.rowid = rowid

    def getJugador(self):
        return self.__jugador

    def getFecha(self):
        return self.__fecha

    def getHora(self):
        return self.__hora

    def getPuntaje(self):
        return self.__puntaje

    def toJSON(self):
        return {
            '__class__': self.__class__.__name__,
            '__atributos__': {
                'jugador': self.__jugador,
                'fecha': self.__fecha,
                'hora': self.__hora,
                'puntaje': self.__puntaje,
                'rowid': self.rowid
            }
        }

    def __gt__(self, other):
        return self.__puntaje >= other.__puntaje