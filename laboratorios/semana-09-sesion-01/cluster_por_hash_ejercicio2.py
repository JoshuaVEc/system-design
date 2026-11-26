"""Ejercicio 2: sharding por hash del estudiante, consulta dirigida y
scatter-gather.

Corre las pruebas con:

    pytest test_cluster_por_hash_ejercicio2.py

No cambies los nombres de la clase ni de los metodos: los tests
dependen de que existan exactamente asi.
"""

from datos_reservas import hash_estable


class ClusterPorHash:
    def __init__(self, cantidad_de_shards):
        self.cantidad_de_shards = cantidad_de_shards
        self.shards = []
        for _ in range(cantidad_de_shards):
            self.shards.append([])

    def shard_de(self, id_estudiante):
        # Hash estable del id_estudiante modulo la cantidad de shards
        return hash_estable(id_estudiante) % self.cantidad_de_shards

    def insertar(self, reserva):
        
        id_est = reserva.get("id_estudiante") if isinstance(reserva, dict) else reserva.id_estudiante
        shard_id = self.shard_de(id_est)
        self.shards[shard_id].append(reserva)

    def tamanos(self):
        
        return [len(shard) for shard in self.shards]

    def reservas_de_estudiante(self, id_estudiante):
        
        shard_id = self.shard_de(id_estudiante)
        encontradas = []
        for r in self.shards[shard_id]:
            r_id = r.get("id_estudiante") if isinstance(r, dict) else r.id_estudiante
            if r_id == id_estudiante:
                encontradas.append(r)
        return (encontradas, 1)
    


    def reservas_de_cancha(self, campus, cancha, fecha):
        
        encontradas = []
        for shard in self.shards:
            for r in shard:
                r_campus = r.get("campus") if isinstance(r, dict) else r.campus
                r_cancha = r.get("cancha") if isinstance(r, dict) else r.cancha
                r_fecha = r.get("fecha") if isinstance(r, dict) else r.fecha

                if r_campus == campus and r_cancha == cancha and r_fecha == fecha:
                    encontradas.append(r)

        return (encontradas, self.cantidad_de_shards)


def fraccion_que_cambia_de_shard(claves, shards_antes, shards_despues):
    
    if not claves:
        return 0.0

    cambiadas = 0
    for clave in claves:
        shard_antes = hash_estable(clave) % shards_antes
        shard_despues = hash_estable(clave) % shards_despues
        if shard_antes != shard_despues:
            cambiadas += 1

    return cambiadas / len(claves)