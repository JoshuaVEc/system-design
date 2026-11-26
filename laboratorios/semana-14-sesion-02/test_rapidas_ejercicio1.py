"""Ejercicio 1: la misma cobertura, en la base de la piramide. Empieza
vacio: se escribe en vivo.

Por cada prueba de punta a punta de test_suite_heredada.py que se pueda
bajar de nivel, una prueba unitaria del servicio (con RepositorioEnMemoria)
o una de integracion (con RepositorioSQLite o con la API), y una sola
prueba de punta a punta que recorra el camino completo.

    pytest test_rapidas_ejercicio1.py --durations=0
"""

import pytest

from api import ApiDeReservas
from dominio import puntos_por_cancelar, semana_de
from entorno_e2e import NavegadorSimulado
from repositorio import RepositorioEnMemoria, RepositorioSQLite
from servicio import ServicioDeReservas


@pytest.fixture
def servicio():
    return ServicioDeReservas(repositorio = RepositorioEnMemoria())

def test_la_cuarta_reserva_se_rechaza(servicio):
    servicio.reservar("r1",'pedro',"2026-11-25")
    servicio.reservar("r2",'pedro',"2026-11-27")
    servicio.reservar("r3",'pedro',"2026-11-28")
    assert servicio.motivo_de_rechazo('pedro','2026-11-29') == "cupo semanal agotado"
    with pytest.raises(ValueError, match = "cupo semanal agotado"):
        servicio.reservar('r4','pedro','2026-11-29')


def test_la_semana_va_de_lunes_a_domingo():
    assert semana_de("2026-11-16") == semana_de("2026-11-22")
    assert semana_de("2026-11-22") != semana_de("2026-11-23")


def test_los_tramos_de_puntos():
    assert puntos_por_cancelar(1440) == 0
    assert puntos_por_cancelar(120) == 1
    assert puntos_por_cancelar(119) == 2


def test_servicio_otra_semana_tiene_cupo_y_es_por_estudiante(servicio):
    servicio.reservar("r1", "ana", "2026-11-20")
    servicio.reservar("r2", "ana", "2026-11-21")
    servicio.reservar("r3", "ana", "2026-11-22")
    servicio.reservar("r4", "ana", "2026-11-23")
    servicio.reservar("r5", "beto", "2026-11-22")


def test_servicio_cancelar_a_tiempo_libera_cupo_sin_puntos():
    repo = RepositorioEnMemoria()
    srv = ServicioDeReservas(repo)
    srv.reservar("r1", "ana", "2026-11-16")
    srv.reservar("r2", "ana", "2026-11-17")
    srv.reservar("r3", "ana", "2026-11-18")
    srv.cancelar("r3", 3000)
    assert repo.puntos_de("ana") == 0
    srv.reservar("r4", "ana", "2026-11-19")


def test_servicio_tres_puntos_bloquean_y_cancelar_desconocida_falla():
    repo = RepositorioEnMemoria()
    srv = ServicioDeReservas(repo)
    srv.reservar("r1", "ana", "2026-11-17")
    srv.cancelar("r1", 30)
    srv.reservar("r2", "ana", "2026-11-18")
    srv.cancelar("r2", 600)
    assert repo.puntos_de("ana") == 3
    with pytest.raises(ValueError, match="estudiante bloqueado"):
        srv.reservar("r3", "ana", "2026-11-19")
    with pytest.raises(ValueError, match="reserva desconocida"):
        srv.cancelar("no-existe", 3000)


def test_integracion_api_con_sqlite():
    repo = RepositorioSQLite(":memory:")
    api = ApiDeReservas(ServicioDeReservas(repo))
    assert api.manejar({"metodo": "POST", "ruta": "/reservas",
                        "cuerpo": {"id": "r1", "estudiante": "ana", "fecha": "2026-11-17"}}) == {
        "estado": 201, "cuerpo": {"id": "r1"},
    }
    assert api.manejar({"metodo": "DELETE", "ruta": "/reservas/r1",
                        "cuerpo": {"minutos_de_anticipacion": 30}})["estado"] == 200
    assert api.manejar({"metodo": "DELETE", "ruta": "/reservas/no-existe",
                        "cuerpo": {"minutos_de_anticipacion": 3000}})["estado"] == 404
    assert api.manejar({"metodo": "GET", "ruta": "/estudiantes/ana/puntos"}) == {
        "estado": 200, "cuerpo": {"puntos": 2},
    }
    repo.cerrar()


def test_e2e_flujo_completo():
    navegador = NavegadorSimulado()
    navegador.iniciar_sesion("ana")
    assert navegador.reservar("r1", "2026-11-17")["estado"] == 201
    assert navegador.cancelar("r1", 30)["estado"] == 200
    assert navegador.ver_puntos() == 2
