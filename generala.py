from random import randint

class ErrorInput(Exception):
    pass

class TurnoError(Exception):
    pass

class TablaPuntosError(Exception):
    pass

def calcular_repetidos(dados):
    repetidos = [0] * 6
    for dado in dados:
        index = dado - 1
        repetidos[index] += 1
    return repetidos

def buscar_repetido(dados, repetidos, cantidad_repetidos, estricto=False):
    encontre = False
    for repetido in repetidos:
        if repetido >= cantidad_repetidos:
            encontre = True
    return encontre

def calcular_puntos(numero_lanzamiento, dados, juego):
    puntos = 0

    if juego == "escalera":
        dados.sort()
        if dados == [1, 2, 3, 4, 5] or dados == [2, 3, 4, 5, 6]:
            puntos = 20
            if numero_lanzamiento == 1:
                puntos += 5

    if juego == "generala":
        repetidos = calcular_repetidos(dados)
        if buscar_repetido(dados, repetidos, 5):
            puntos = 50

    elif juego == "generala_doble":
        repetidos = calcular_repetidos(dados)
        if buscar_repetido(dados, repetidos, 5):
            puntos = 100

    elif juego == "poker":
        repetidos = calcular_repetidos(dados)
        if buscar_repetido(dados, repetidos, 4):
            puntos = 40
            if numero_lanzamiento == 1:
                puntos += 5

    elif juego == "full":
        diferentes = []
        for x in dados:
            if x not in diferentes:
                diferentes.append(x)
            if len(diferentes) == 2:
                if (dados.count(diferentes[0]) == 3 and dados.count(diferentes[1]) == 2) or (dados.count(diferentes[0]) == 2 and dados.count(diferentes[1]) == 3):
                    puntos = 30
                    if numero_lanzamiento == 1:
                        puntos += 5
      
              
    else:   #"1","2","3","4","5","6"
        for dado in dados:
            if juego == str(dado):
                puntos += dado
    return puntos

class Jugador:
    pass

class Dados:
    def __init__(self, cantidad_dados):
        self._valores = [randint(1, 6) for _ in range(cantidad_dados)]

    @property
    def cantidad(self):
        return len(self._valores)

    @property
    def valores(self):
        return self._valores

class Turno:
    def __init__(self):
        self.numero_lanzamiento = 1
        self.dados_lanzados = Dados(5)
        self.dados_seguir = Dados(0)

    def guardar_dados(self, indices):
        for indice in indices:
            self.dados_seguir.valores.append(self.dados_lanzados.valores[indice])
        self.siguiente_turno()

    def siguiente_turno(self):
        if(self.numero_lanzamiento >= 3):
            raise TurnoError("\nLímite de lanzamientos alcanzado")

        self.numero_lanzamiento += 1
        self.dados_lanzados = Dados(5 - self.dados_seguir.cantidad)

    @property
    def dados_finales(self):
        return self.dados_lanzados.valores + self.dados_seguir.valores

class TablaPuntos:
    def __init__(self, cantidad_jugadores):
        self.cantidad_jugadores = cantidad_jugadores
        self._tabla = [  # lista
            {  # diccionario
                '1': None,
                '2': None,
                '3': None,
                '4': None,
                '5': None,
                '6': None,
                'escalera': None,
                'full': None,
                'poker': None,
                'generala': None,
                'generala_doble': None,
            }
            for _ in range(cantidad_jugadores)
        ]

    @property
    def estado_tabla(self):
        for jugada in self._tabla[-1].values():
            if jugada is None:
                return False
        return True # Significa que la tabla del ultimo jugador esta llena
    

    def jugadas_faltantes(self, jugador):
        faltan = []
        for jugada, value in self._tabla[jugador].items():
            if value is None:
                faltan.append(jugada)
        return faltan

    def anotar(self, jugador, jugada, numero_lanzamiento, dados):
        jugadas_validas = ['1','2','3','4','5','6','escalera','full','poker','generala','generala_doble',]

        if jugada not in jugadas_validas:
            raise ErrorInput("\nJugada no valida")

        if jugada == 'generala_doble' and self._tabla[jugador]['generala'] is None:
            self._tabla[jugador]['generala_doble'] = None
            raise TablaPuntosError("\nPara anotar generala_doble primer tenes que tener anotado generala")
        elif jugada == 'generala_doble' and self._tabla[jugador]['generala'] is not None:
            self._tabla[jugador][jugada] = calcular_puntos(numero_lanzamiento, dados, "generala_doble")



        elif self._tabla[jugador][jugada] is None:
            puntos = calcular_puntos(numero_lanzamiento, dados, jugada)
            self._tabla[jugador][jugada] = puntos
    
        else:
            raise TablaPuntosError('\nJugada ya anotada. No se puede anotar la misma jugada dos veces')

    def puntaje_final(self):
        puntaje = {}
        for jugador in range(self.cantidad_jugadores):
            puntos = 0
            for jugada in ['1','2','3','4','5','6','escalera','full','poker','generala','generala_doble',]:
                if self._tabla[jugador][jugada] is not None:
                    puntos += self._tabla[jugador][jugada]
            puntaje[jugador]=puntos
        return puntaje


    
class Generala:
    def __init__(self, cantidad_jugadores):
        self.cantidad_jugadores = cantidad_jugadores
        self.esta_jugado = True
        self.jugador_esta_jugando = True
        self.jugador_actual = 0
        self.turno_actual = Turno()
        self.tabla_puntos = TablaPuntos(cantidad_jugadores)
        self.puntos = 0

    def siguiente_jugador(self):
        self.jugador_actual += 1
        self.jugador_actual = self.jugador_actual % self.cantidad_jugadores
        self.turno_actual = Turno()
        self.jugador_esta_jugando = True

    def anotar(self, jugada):
        try:
            self.tabla_puntos.anotar(self.jugador_actual, jugada, self.turno_actual.numero_lanzamiento, self.turno_actual.dados_finales)
            if self.tabla_puntos.estado_tabla:
                self.esta_jugado = False
            else:
                self.siguiente_jugador()
            return "\nSe anoto la jugada '{}'\n".format(jugada)
        except TablaPuntosError as e:
            return str(e)


    def dados_finales(self, dados_seguir):
        if dados_seguir == "ANOTAR" :
            self.jugador_esta_jugando = False
        else:
            if dados_seguir == "":
                list_int_dados_seguir = []
            else:
                list_dados_seguir = dados_seguir.split(sep=',')
                list_int_dados_seguir = [int(dado) for dado in list_dados_seguir]
            self.turno_actual.guardar_dados(list_int_dados_seguir)
            if self.turno_actual.numero_lanzamiento == 3:
                self.jugador_esta_jugando = False
    
    def jugadas_faltantes(self):
      return self.tabla_puntos.jugadas_faltantes(self.jugador_actual)

    def mostrar_puntos(self):
        puntaje = self.tabla_puntos.puntaje_final()
        for jugador in range(self.cantidad_jugadores):
            print( "jugador {} : {} ptos. ".format(jugador, puntaje[jugador]) )

    def mostrar_ganador(self):
        puntaje = self.tabla_puntos.puntaje_final()
        ganador = max(puntaje, key=puntaje.get)
        return ganador


def main():

    while True:
        try:
            cantidad_jugadores = int(input('\nCantidad de jugadores: '))
            juego = Generala(cantidad_jugadores)
            print("\nComenzemos a jugar...\n")
            while juego.esta_jugado:
                while juego.jugador_esta_jugando:
                    print('\njugador actual: {} \n'.format(juego.jugador_actual))
                    print("En el lanzamiento nº {} tocaron los dados:".format(juego.turno_actual.numero_lanzamiento))
                    print(juego.turno_actual.dados_finales)
                    decision = input("\n¿Quiere finalizar el turno? (si/no): ")
                    if decision == "si":
                        dados_seguir = "ANOTAR"
                    else:
                        dados_seguir = input('\nIngrese índices de los dados con los que quiere seguir o presione enter para tirar todos los dados de vuelta: ')
                    juego.dados_finales(dados_seguir)
                print(juego.turno_actual.dados_finales)
                jugada = input('\n¿Qué jugada quiere anotar? {}: '.format(juego.jugadas_faltantes()))
                print(juego.anotar(jugada))
                # print("La tabla de puntos es: \n")
                # print(juego.tabla_puntos._tabla)
            
            print("\nTodos los jugadores completaron las jugadas. Los puntajes son: \n")
            juego.mostrar_puntos()
            print("\nEl ganador es el jugador {}".format(juego.mostrar_ganador()))
            exit()
    
        
        except ValueError:
            print("\nValor inválido. Ingrese un valor válido")
    
if __name__ == '__main__':
    main()

