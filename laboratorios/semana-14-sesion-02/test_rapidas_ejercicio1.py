"""Ejercicio 1: la misma cobertura, en la base de la piramide. Empieza
vacio: se escribe en vivo.

Por cada prueba de punta a punta de test_suite_heredada.py que se pueda
bajar de nivel, una prueba unitaria del servicio (con RepositorioEnMemoria)
o una de integracion (con RepositorioSQLite o con la API), y una sola
prueba de punta a punta que recorra el camino completo.

    pytest test_rapidas_ejercicio1.py --durations=0
"""


import pytest
from repositorio import RepositorioEnMemoria
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