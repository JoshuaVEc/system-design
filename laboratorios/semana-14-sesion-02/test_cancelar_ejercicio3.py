"""Ejercicio 3: las pruebas de cancelar. Sin pruebas de partida: las
escribes tu, decidiendo de que tipo es cada una.

    pytest test_cancelar_ejercicio3.py --durations=0
"""

import pytest

from api import ApiDeReservas
from dominio import semana_de
from entorno_e2e import NavegadorSimulado
from repositorio import RepositorioEnMemoria, RepositorioSQLite
from servicio import ServicioDeReservas


def test_unitario_cancelar_borra_solo_la_indicada_y_suma_puntos():
    repo = RepositorioEnMemoria()
    servicio = ServicioDeReservas(repo)
    servicio.reservar("r1", "ana", "2026-11-16")
    servicio.reservar("r2", "ana", "2026-11-17")
    servicio.cancelar("r1", 600)
    assert repo.buscar("r1") is None
    assert repo.buscar("r2") == ("ana", "2026-11-17")
    assert repo.contar_en_semana("ana", semana_de("2026-11-16")) == 1
    assert repo.puntos_de("ana") == 1


def test_unitario_cancelar_inexistente_lanza_error():
    servicio = ServicioDeReservas(RepositorioEnMemoria())
    with pytest.raises(ValueError, match="reserva desconocida"):
        servicio.cancelar("no-existe", 1500)


def test_integracion_sqlite_cancelar_una_reserva_mantiene_las_otras_del_mismo_estudiante():
    repo = RepositorioSQLite(":memory:")
    servicio = ServicioDeReservas(repo)
    servicio.reservar("r1", "ana", "2026-11-16")
    servicio.reservar("r2", "ana", "2026-11-17")
    servicio.reservar("r3", "beto", "2026-11-18")
    servicio.cancelar("r1", 2000)
    assert repo.buscar("r1") is None
    assert repo.buscar("r2") == ("ana", "2026-11-17")
    assert repo.buscar("r3") == ("beto", "2026-11-18")
    assert repo.contar_en_semana("ana", semana_de("2026-11-16")) == 1
    assert repo.puntos_de("ana") == 0
    repo.cerrar()


def test_integracion_api_cancelar_tarde_con_sqlite():
    repo = RepositorioSQLite(":memory:")
    api = ApiDeReservas(ServicioDeReservas(repo))
    api.manejar({"metodo": "POST", "ruta": "/reservas",
                 "cuerpo": {"id": "r1", "estudiante": "ana", "fecha": "2026-11-16"}})
    api.manejar({"metodo": "POST", "ruta": "/reservas",
                 "cuerpo": {"id": "r2", "estudiante": "ana", "fecha": "2026-11-17"}})
    respuesta = api.manejar({"metodo": "DELETE", "ruta": "/reservas/r1",
                             "cuerpo": {"minutos_de_anticipacion": 30}})
    assert respuesta == {"estado": 200, "cuerpo": {}}
    assert repo.buscar("r2") == ("ana", "2026-11-17")
    assert repo.puntos_de("ana") == 2
    repo.cerrar()


def test_e2e_cancelar_una_de_tres_conserva_el_cupo_usado_de_las_otras_dos():
    navegador = NavegadorSimulado()
    navegador.iniciar_sesion("ana")
    navegador.reservar("r1", "2026-11-16")
    navegador.reservar("r2", "2026-11-17")
    navegador.reservar("r3", "2026-11-18")
    assert navegador.cancelar("r1", 3000)["estado"] == 200
    assert navegador.reservar("r4", "2026-11-19")["estado"] == 201
    assert navegador.reservar("r5", "2026-11-20")["estado"] == 409
