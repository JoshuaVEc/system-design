"""Ejercicio 3: decidir, lectura por lectura, si va a la primaria o a la
replica.

Corre las pruebas con:

    pytest test_servicio_replicado_ejercicio3.py

No cambies los nombres de la clase ni de los metodos, y lee siempre a
traves de self.base.leer_de_primaria() o self.base.leer_de_replica():
los tests cuentan en que nodo hiciste cada lectura.
"""

from datos_reservas import ReservaRegistrada


def _obtener_campo(reserva, campo):
    
    if hasattr(reserva, campo):
        return getattr(reserva, campo)
    return None

def _obtener_id(reserva):
   
    if hasattr(reserva, "id"): return reserva.id
    if hasattr(reserva, "id_reserva"): return reserva.id_reserva
    if isinstance(reserva, tuple) and len(reserva) > 0: return reserva[0]
    return None


class ServicioDeReservasReplicado:
    def __init__(self, base):
        self.base = base
        self.siguiente_id = 1
        
        self.ultima_reserva_estudiante = {}

    def cancha_disponible(self, campus, cancha, fecha, hora):
       
        reservas = self.base.leer_de_primaria()
        for r in reservas:
            if (_obtener_campo(r, "campus") == campus and
                _obtener_campo(r, "cancha") == cancha and
                _obtener_campo(r, "fecha") == fecha and
                _obtener_campo(r, "hora") == hora):
                return False
        return True

    def reservar(self, id_estudiante, campus, cancha, fecha, hora):
        if not self.cancha_disponible(campus, cancha, fecha, hora):
            return None
        
        id_asignado = self.siguiente_id
        reserva = ReservaRegistrada(id_asignado, id_estudiante, campus, cancha, fecha, hora)
        self.siguiente_id += 1
        self.base.escribir(reserva)
        
        
        self.ultima_reserva_estudiante[id_estudiante] = id_asignado
        return reserva

    def mis_reservas(self, id_estudiante):
        
        if id_estudiante not in self.ultima_reserva_estudiante:
            reservas = self.base.leer_de_replica()
            return [
                r for r in reservas
                if _obtener_campo(r, "id_estudiante") == id_estudiante
            ]

        
        reservas_replica = self.base.leer_de_replica()
        id_esperado = self.ultima_reserva_estudiante[id_estudiante]

        ids_en_replica = {_obtener_id(r) for r in reservas_replica}

        if id_esperado in ids_en_replica:
           
            return [
                r for r in reservas_replica
                if _obtener_campo(r, "id_estudiante") == id_estudiante
            ]

       
        reservas_primaria = self.base.leer_de_primaria()
        return [
            r for r in reservas_primaria
            if _obtener_campo(r, "id_estudiante") == id_estudiante
        ]

    def ocupacion_del_campus(self, campus):
        
        reservas = self.base.leer_de_replica()
        total = 0
        for r in reservas:
            if _obtener_campo(r, "campus") == campus:
                total += 1
        return total