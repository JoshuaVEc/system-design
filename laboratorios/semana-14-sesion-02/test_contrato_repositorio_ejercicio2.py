"""Ejercicio 2: las pruebas de contrato del repositorio.

El servicio se prueba rapido con RepositorioEnMemoria, un doble de prueba.
Eso solo vale si el doble se comporta igual que RepositorioSQLite. Estas
pruebas corren dos veces cada una, una con cada repositorio (la fixture
`repositorio` tiene dos parametros): si una pasa con uno y falla con el
otro, el doble miente.

    pytest test_contrato_repositorio_ejercicio2.py -v
"""

import sqlite3

import pytest

from dominio import semana_de
from repositorio import RepositorioEnMemoria, RepositorioSQLite


@pytest.fixture(params=["memoria", "sqlite"])
def repositorio(request, tmp_path):
    if request.param == "memoria":
        repo = RepositorioEnMemoria()
    else:
        repo = RepositorioSQLite(str(tmp_path / "reservau.db"))
    yield repo
    repo.cerrar()


def test_guardar_y_buscar(repositorio):
    repositorio.guardar("r1", "ana", "2026-11-17")
    assert repositorio.buscar("r1") == ("ana", "2026-11-17")


def test_buscar_inexistente_devuelve_none(repositorio):
    assert repositorio.buscar("no-existe") is None


def test_contar_en_semana_filtra_por_estudiante_y_semana(repositorio):
    repositorio.guardar("r1", "ana", "2026-11-16")
    repositorio.guardar("r2", "ana", "2026-11-22")
    repositorio.guardar("r3", "ana", "2026-11-23")
    repositorio.guardar("r4", "beto", "2026-11-16")
    assert repositorio.contar_en_semana("ana", semana_de("2026-11-16")) == 2
    assert repositorio.contar_en_semana("ana", semana_de("2026-11-23")) == 1
    assert repositorio.contar_en_semana("beto", semana_de("2026-11-16")) == 1


def test_guardar_id_repetido_lanza_integrity_error(repositorio):
    repositorio.guardar("r1", "ana", "2026-11-17")
    with pytest.raises(sqlite3.IntegrityError):
        repositorio.guardar("r1", "beto", "2026-11-18")


def test_puntos_de_suma_puntos_por_estudiante(repositorio):
    assert repositorio.puntos_de("ana") == 0
    repositorio.sumar_puntos("ana", 1)
    repositorio.sumar_puntos("ana", 2)
    repositorio.sumar_puntos("beto", 1)
    assert repositorio.puntos_de("ana") == 3
    assert repositorio.puntos_de("beto") == 1
