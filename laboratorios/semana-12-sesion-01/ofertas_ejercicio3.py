"""Ejercicio 3: la lista de espera con plazo para aceptar.

Avisar a beto no alcanza: si beto no contesta, la franja queda libre y
dani, que tambien esperaba, nunca se entera. La universidad pide esto:

ListaDeEsperaConPlazo es un observador de CalendarioConEventos (Ejercicio
2) que se suscribe a "liberada" y a "ocupada". Se construye con
ListaDeEsperaConPlazo(calendario, notificador, reloj, minutos_para_aceptar=15),
donde reloj es un RelojSimulado (reloj.py). Cada franja tiene su propia
fila de espera, y a lo sumo una oferta activa a la vez.

- anotar(estudiante, inicio, fin): pone al estudiante al final de la fila
  de esa franja (del dia del calendario). Si ya esta en esa fila, o ya
  tiene la oferta activa de esa franja: ValueError("ya esta en la lista").
  Si la franja esta libre en este momento: ValueError("la franja esta
  libre"), porque puede reservarla directamente.

- Cuando una franja se libera y no tiene oferta activa, se le ofrece al
  primero de su fila: sale de la fila, recibe "Tienes 15 minutos para
  aceptar cancha-1 2026-11-10 18-19" (con los minutos del constructor), y
  la oferta vence minutos_para_aceptar minutos despues de ahora. Si al
  primero no le alcanza el limite de horas (horas_de del calendario mas la
  duracion de la franja pasaria de MAXIMO_HORAS_POR_ESTUDIANTE), sale de
  la fila, recibe "No puedes tomar cancha-1 2026-11-10 18-19: pasarias el
  limite de horas", y la oferta pasa al siguiente. Si la fila queda vacia,
  no hay oferta.

- aceptar(estudiante, inicio, fin, id_reserva): si el estudiante no tiene
  la oferta activa de esa franja: ValueError("no tienes una oferta"). Si
  la oferta ya vencio (el reloj paso del minuto de vencimiento):
  ValueError("oferta vencida"), y la oferta sigue ahi hasta que alguien
  revise las vencidas. Si no, la oferta se cierra y se reserva la franja
  a su nombre con ese id.

- revisar_vencidas(): cada oferta vencida se cierra, su estudiante recibe
  "Vencio tu oferta de cancha-1 2026-11-10 18-19", y la franja se le
  ofrece al siguiente de la fila, con las mismas reglas. En la app en
  produccion esto lo corre un proceso cada minuto.

- Si alguien reserva directamente una franja que tiene una oferta activa
  (o una que se solapa con ella), la oferta se cierra y su estudiante
  recibe "La franja cancha-1 2026-11-10 18-19 ya no esta disponible". La
  fila de esa franja no cambia.

Los mensajes se envian con notificador.enviar(estudiante, texto), con el
texto exacto de arriba. Esta vez no hay codigo de partida: escribes la
clase completa. Corre las pruebas con:

    pytest test_ofertas_ejercicio3.py
"""

from eventos_ejercicio2 import ObservadorDeReservas
from reservas import MAXIMO_HORAS_POR_ESTUDIANTE, FranjaHoraria


class ListaDeEsperaConPlazo(ObservadorDeReservas):
    def __init__(self, calendario, notificador, reloj, minutos_para_aceptar=15):
        self.calendario = calendario
        self.notificador = notificador
        self.reloj = reloj
        self.minutos_para_aceptar = minutos_para_aceptar
        self.filas = {}
        self.ofertas = {}

    def anotar(self, estudiante, inicio, fin):
        franja = FranjaHoraria(self.calendario.fecha, inicio, fin)
        en_fila = estudiante in self.filas.get(franja, [])
        tiene_oferta = franja in self.ofertas and self.ofertas[franja][0] == estudiante
        if en_fila or tiene_oferta:
            raise ValueError("ya esta en la lista")
        if self.calendario.esta_libre(inicio, fin):
            raise ValueError("la franja esta libre")
        self.filas.setdefault(franja, []).append(estudiante)

    def _ofrecer_al_siguiente(self, cancha, franja):
        cola = self.filas.get(franja, [])
        while cola:
            estudiante = cola.pop(0)
            if self.calendario.horas_de(estudiante) + franja.duracion() > MAXIMO_HORAS_POR_ESTUDIANTE:
                self.notificador.enviar(
                    estudiante,
                    f"No puedes tomar {cancha} {franja.fecha} {franja.inicio}-{franja.fin}: pasarias el limite de horas",
                )
                continue
            vence = self.reloj.ahora() + self.minutos_para_aceptar
            self.ofertas[franja] = (estudiante, vence)
            self.notificador.enviar(
                estudiante,
                f"Tienes {self.minutos_para_aceptar} minutos para aceptar {cancha} {franja.fecha} {franja.inicio}-{franja.fin}",
            )
            return

    def al_liberarse(self, cancha, franja):
        if franja not in self.ofertas:
            self._ofrecer_al_siguiente(cancha, franja)

    def al_ocuparse(self, cancha, franja):
        for franja_oferta, (estudiante, _) in list(self.ofertas.items()):
            if franja_oferta.se_solapa_con(franja):
                del self.ofertas[franja_oferta]
                self.notificador.enviar(
                    estudiante,
                    f"La franja {cancha} {franja_oferta.fecha} {franja_oferta.inicio}-{franja_oferta.fin} ya no esta disponible",
                )

    def aceptar(self, estudiante, inicio, fin, id_reserva):
        franja = FranjaHoraria(self.calendario.fecha, inicio, fin)
        oferta = self.ofertas.get(franja)
        if oferta is None or oferta[0] != estudiante:
            raise ValueError("no tienes una oferta")
        if self.reloj.ahora() > oferta[1]:
            raise ValueError("oferta vencida")
        del self.ofertas[franja]
        try:
            self.calendario.reservar(id_reserva, estudiante, inicio, fin)
        except Exception:
            self.ofertas[franja] = oferta
            raise

    def revisar_vencidas(self):
        ahora = self.reloj.ahora()
        vencidas = [(franja, est) for franja, (est, vence) in list(self.ofertas.items()) if ahora > vence]
        for franja, estudiante in vencidas:
            del self.ofertas[franja]
            self.notificador.enviar(
                estudiante,
                f"Vencio tu oferta de {self.calendario.cancha} {franja.fecha} {franja.inicio}-{franja.fin}",
            )
            self._ofrecer_al_siguiente(self.calendario.cancha, franja)
