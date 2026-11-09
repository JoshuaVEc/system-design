"""Ejercicio 3: decidir, lectura por lectura, si va a la primaria o a la
replica.

Corre las pruebas con:

    pytest test_servicio_replicado_ejercicio3.py

No cambies los nombres de la clase ni de los metodos, y lee siempre a
traves de self.base.leer_de_primaria() o self.base.leer_de_replica():
los tests cuentan en que nodo hiciste cada lectura.
"""

from datos_reservas import ReservaRegistrada


class ServicioDeReservasReplicado:
    def __init__(self, base):
        self.base = base
        self.siguiente_id = 1
        
        self.estudiantes_con_escritura = set()

    def cancha_disponible(self, campus, cancha, fecha, hora):
        
        reservas = self.base.leer_de_primaria()
        for r in reservas:
            r_campus = r.get("campus") if isinstance(r, dict) else r.campus
            r_cancha = r.get("cancha") if isinstance(r, dict) else r.cancha
            r_fecha = r.get("fecha") if isinstance(r, dict) else r.fecha
            r_hora = r.get("hora") if isinstance(r, dict) else r.hora

            if r_campus == campus and r_cancha == cancha and r_fecha == fecha and r_hora == hora:
                return False
        return True

    def reservar(self, id_estudiante, campus, cancha, fecha, hora):
        if not self.cancha_disponible(campus, cancha, fecha, hora):
            return None
        reserva = ReservaRegistrada(self.siguiente_id, id_estudiante, campus, cancha, fecha, hora)
        self.siguiente_id = self.siguiente_id + 1
        self.base.escribir(reserva)
        
        self.estudiantes_con_escritura.add(id_estudiante)
        return reserva

    def mis_reservas(self, id_estudiante):
       
        if id_estudiante in self.estudiantes_con_escritura:
            reservas = self.base.leer_de_primaria()
        else:
            reservas = self.base.leer_de_replica()

        encontradas = []
        for r in reservas:
            r_id = r.get("id_estudiante") if isinstance(r, dict) else r.id_estudiante
            if r_id == id_estudiante:
                encontradas.append(r)
        return encontradas

    def ocupacion_del_campus(self, campus):
       
        reservas = self.base.leer_de_replica()
        total = 0
        for r in reservas:
            r_campus = r.get("campus") if isinstance(r, dict) else r.campus
            if r_campus == campus:
                total += 1
        return total