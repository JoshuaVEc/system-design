"""Pruebas del Ejercicio 3: las escriben ustedes, en pareja, una a la vez."""

import pytest

from recurrentes_ejercicio3 import AgendaDeCancha


def test_calendario_se_crea_y_reutiliza_por_fecha():
    agenda = AgendaDeCancha("cancha-1")
    cal_a = agenda.calendario("2026-11-10")
    cal_b = agenda.calendario("2026-11-10")
    cal_otro = agenda.calendario("2026-11-17")
    assert cal_a is cal_b
    assert cal_a is not cal_otro
    assert cal_a.cancha == "cancha-1"
    assert cal_a.fecha == "2026-11-10"


def test_reservar_varias_semanas_libres():
    agenda = AgendaDeCancha("cancha-1")
    resultado = agenda.reservar_cada_semana("entreno", "futbol-arq", "2026-11-10", 18, 19, 3)
    assert resultado == [
        ("2026-11-10", "reservada"),
        ("2026-11-17", "reservada"),
        ("2026-11-24", "reservada"),
    ]
    assert agenda.calendario("2026-11-10").reservas()[0][0] == "entreno-1"
    assert agenda.calendario("2026-11-17").reservas()[0][0] == "entreno-2"
    assert agenda.calendario("2026-11-24").reservas()[0][0] == "entreno-3"


def test_salta_semana_ocupada_y_continua_con_las_demas():
    agenda = AgendaDeCancha("cancha-1")
    agenda.calendario("2026-11-17").reservar("otra", "ana", 18, 19)
    resultado = agenda.reservar_cada_semana("entreno", "beto", "2026-11-10", 18, 19, 3)
    assert resultado == [
        ("2026-11-10", "reservada"),
        ("2026-11-17", "ocupada"),
        ("2026-11-24", "reservada"),
    ]
    assert [r[0] for r in agenda.calendario("2026-11-17").reservas()] == ["otra"]


def test_reporta_limite_si_supera_maximo_de_horas_diarias():
    agenda = AgendaDeCancha("cancha-1")
    agenda.calendario("2026-11-17").reservar("previa", "beto", 8, 10)
    resultado = agenda.reservar_cada_semana("entreno", "beto", "2026-11-10", 18, 19, 3)
    assert resultado == [
        ("2026-11-10", "reservada"),
        ("2026-11-17", "limite"),
        ("2026-11-24", "reservada"),
    ]


def test_ocupada_tiene_prioridad_sobre_limite():
    agenda = AgendaDeCancha("cancha-1")
    agenda.calendario("2026-11-10").reservar("previa", "beto", 18, 20)
    resultado = agenda.reservar_cada_semana("entreno", "beto", "2026-11-10", 18, 19, 1)
    assert resultado == [("2026-11-10", "ocupada")]


def test_semanas_fuera_de_rango_lanza_sin_reservar_nada():
    agenda = AgendaDeCancha("cancha-1")
    with pytest.raises(ValueError):
        agenda.reservar_cada_semana("entreno", "ana", "2026-11-10", 18, 19, 0)
    with pytest.raises(ValueError):
        agenda.reservar_cada_semana("entreno", "ana", "2026-11-10", 18, 19, 13)
    assert agenda.calendario("2026-11-10").reservas() == []


def test_franja_invalida_lanza_sin_reservar_nada():
    agenda = AgendaDeCancha("cancha-1")
    with pytest.raises(ValueError, match="franja invalida"):
        agenda.reservar_cada_semana("entreno", "ana", "2026-11-10", 20, 22, 2)
    assert agenda.calendario("2026-11-10").reservas() == []
