"""Pruebas del Ejercicio 2. La primera ya esta escrita. Escribe las demas
una a la vez, en este orden, y antes de cada una haz pasar la anterior:

1. Un estudiante sin reservas puede reservar.
2. Con 2 reservas en la semana, todavia puede.
3. Con 3 reservas en la semana, ya no puede.
4. Las reservas de otra semana no cuentan (2026-11-16 y 2026-11-23 son
   lunes de semanas distintas; 2026-11-22 es el domingo de la semana del 16).
5. Cancelar una reserva libera su lugar.
6. Un equipo oficial puede tener 6 reservas en la semana, pero no 7.
7. Registrar la cuarta reserva lanza ValueError (usa pytest.raises), y
   despues de intentarlo el estudiante sigue con 3.

Anota en la bitacora del README, por cada prueba: con que mensaje fallo,
que cambiaste para que pase, y que refactorizaste.
"""

import pytest

from cupos_ejercicio2 import CupoSemanal, semana_de


def test_sin_reservas_puede_reservar():
    cupo = CupoSemanal()
    assert cupo.puede_reservar("ana", "2026-11-16")== True

def test_con_2_reservas_en_la_semana_se_puedo_reservar():
    cupo =CupoSemanal()
    cupo.registrar(100,"juan","2026-11-16")
    cupo.registrar(102,"juan","2026-11-17")
    assert cupo.puede_reservar("juan","2020-11-18")

def test_con_3_reservas_en_la_semana_no_puede_reservar():
    
    cupo =CupoSemanal()
    cupo.registrar(100,"jose","2026-11-23")
    cupo.registrar(102,"jose", "2026-11-24")
    cupo.registrar(103,"jose","2026-11-25")
    assert cupo.puede_reservar("jose", "2026-11-26")==False
def test_reservas_semanas_diferentes_no_cuentan():
    cupo =CupoSemanal()
    cupo.registrar(100,"julian","2026-11-16")
    cupo.registrar(100,"julian","2026-11-23")
    assert cupo._cupos["julian"][semana_de("2026-11-16")]==2
    assert cupo._cupos["julian"][semana_de("2026-11-23")]==2

def test_cancelar_reserva_libera_lugar_y_cupo():
    cupo =CupoSemanal()
    cupo.registrar(100,"jose","2026-11-23")
    cupo.cancelar(100)
    assert cupo._cupos["jose"][semana_de("2026-11-23")] ==3

def test_equipo_oficial_puede_reservas_6_no_7():
    cupo =CupoSemanal()
    cupo.registrar_equipo_oficial("juan")
    cupo.registrar(1000,"juan","2026-11-23")
    cupo.registrar(1001,"juan","2026-11-24")
    cupo.registrar(1002,"juan","2026-11-25")
    assert cupo.puede_reservar("juan","2026-11-26") == True
    cupo.registrar(1003,"juan","2026-11-26")
    cupo.registrar(1004,"juan","2026-11-27")
    cupo.registrar(1005,"juan","2026-11-28")
    assert cupo.puede_reservar("juan","2026-11-28")==False

def test_cuarta_reserva_lanza_ValueError_estudiante_sigue_con_3():
   cupo =CupoSemanal()    
   cupo.registrar(1000,"juan","2026-11-23")
   cupo.registrar(1002,"juan","2026-11-24")
   cupo.registrar(1003,"juan","2026-11-25")
   

   with pytest.raises(ValueError):
       cupo.registrar(1004,"juan","2026-11-26")
   assert cupo._cupos["juan"][semana_de("2026-11-23")] == 0
