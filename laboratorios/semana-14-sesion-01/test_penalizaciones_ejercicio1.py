"""Pruebas del Ejercicio 1. Empieza vacio: cada prueba se escribe antes
del codigo que la hace pasar, una a la vez, en el orden de la lista de
penalizaciones_ejercicio1.py.
"""

from penalizaciones_ejercicio1 import HistorialDePenalizaciones, puntos_por_cancelar


def test_cancelar_con_mas_de_un_dia_no_penaliza():
    assert puntos_por_cancelar(2000)==0

def test_cancelar_el_mismo_dia():
    assert puntos_por_cancelar(1200)==1

def test_cancelar_con_menos_de_2_horas():
    assert puntos_por_cancelar(80)==2

def test_cancelacion_casos_frontera():

    assert puntos_por_cancelar(1440)==0
    assert puntos_por_cancelar(1)==2

def test_estudiante_con_tres_puntos_bloqueado():
    historial = HistorialDePenalizaciones()
    historial.cancelar('Ana',600)
    assert historial.esta_bloqueada('Ana')==False

    historial.cancelar('Ana',10)
    assert historial.esta_bloqueada('Ana')==True

def test_estudiante_nuevo_ver_bloqueado():
    historial =HistorialDePenalizaciones()
    assert historial.esta_bloqueada('Pedro') == False

#pruebas que debemos seguir creando para confirmr la calidad del comportamiento de la funcionalidad 