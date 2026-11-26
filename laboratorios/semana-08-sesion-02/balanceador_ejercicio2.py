"""Ejercicio 2: balanceador round robin con health check.

Corre las pruebas con:

    pytest test_balanceador_ejercicio2.py

No cambies los nombres de la clase ni de los metodos: los tests
dependen de que existan exactamente asi.
"""


class BalanceadorRoundRobin:
    def __init__(self, servidores):
        self.servidores = servidores
        self.siguiente = 0

    def enviar(self, duracion):
        
        cantidad = len(self.servidores)
        intento=self.siguiente
        for intento in range(cantidad):
            asignado =(self.siguiente + intento)% cantidad
            servidor =self.servidores[asignado]
            if servidor.puede_atender():
                servidor.atender(duracion)
                self.siguiente = (asignado + 1 )% cantidad
                return servidor.nombre
        return None

        
