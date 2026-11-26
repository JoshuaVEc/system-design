"""Ejercicio 2: el cupo semanal de reservas, con TDD.

ReservaU limita cuantas reservas puede tener cada estudiante por semana,
para que nadie acapare las canchas. La regla:

- Cada estudiante puede tener como maximo 3 reservas activas por semana.
  La semana va de lunes a domingo (semana_de, abajo, ya lo resuelve).
- Las reservas de semanas distintas no se suman.
- Cancelar una reserva libera su lugar en el cupo.
- Los equipos oficiales registrados tienen un cupo de 6.
- Registrar una reserva cuando el cupo esta agotado lanza
  ValueError("cupo semanal agotado"), y no la registra.

La clase se llama CupoSemanal y tiene, al final, estos metodos:

- puede_reservar(estudiante, fecha): True si le queda cupo esa semana.
- registrar(id_reserva, estudiante, fecha)
- cancelar(id_reserva)
- registrar_equipo_oficial(estudiante)

La lista de pruebas esta en test_cupos_ejercicio2.py. La primera ya esta
escrita. Corre las pruebas con:

    pytest test_cupos_ejercicio2.py

Cuando termines la lista, y no antes, corre las pruebas de aceptacion:

    pytest test_aceptacion_cupos.py
"""

from datetime import date



def semana_de(fecha):
    """La semana de una fecha "AAAA-MM-DD", como (anio, numero de semana).
    Dos fechas de la misma semana (de lunes a domingo) dan lo mismo."""
    anio, semana, _ = date.fromisoformat(fecha).isocalendar()
    return (anio, semana)

CUPOS_ESTUDIANTES =3
CUPOS_EQUIPO_OFICIAL =6
class CupoSemanal():
    def __init__(self):
        self._cupos={}
        self.reservas={}
        self.equipoOficial={}

    def _inicializar(self, estudiante,fecha):
        semana = semana_de(fecha)
        if estudiante not in  self._cupos:
            self._cupos[estudiante] ={}
        if estudiante not in self.equipoOficial:
             if semana not in self._cupos[estudiante]:
                 self._cupos[estudiante][semana] = CUPOS_ESTUDIANTES
        else:
            if semana not in self._cupos[estudiante]:
                self._cupos[estudiante][semana]=CUPOS_EQUIPO_OFICIAL

    def puede_reservar(self,estudiante,fecha):
        self._inicializar(estudiante,fecha)
        if self._cupos[estudiante][semana_de(fecha)]>0:
            return True
        return False
    


    def registrar(self,id_reserva,estudiante,fecha):
        if self.puede_reservar(estudiante,fecha):
            self.reservas[id_reserva] = [estudiante,fecha]
            self._cupos[estudiante][semana_de(fecha)] -= 1
        else:
            raise ValueError("cupo semanal agotado")
        
    def cancelar(self,id_reserva):
        if id_reserva not in self.reservas:
            raise ValueError("reserva desconocida")
        estudiante,fecha =self.reservas.pop(id_reserva)
        self._cupos[estudiante][semana_de(fecha)]+=1
        

    def registrar_equipo_oficial(self,estudiante):
        self.equipoOficial[estudiante]={}
