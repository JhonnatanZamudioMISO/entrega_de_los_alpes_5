from aeroalpes.modulos.pedidos.dominio.eventos.ordenes import OrdenCreada, OrdenCancelada, OrdenAprobada, OrdenPagada
from aeroalpes.seedwork.aplicacion.handlers import Handler
from aeroalpes.modulos.pedidos.infraestructura.despachadores import Despachador

class HandlerOrdenIntegracion(Handler):

    @staticmethod
    def handle_orden_creada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-orden')

    @staticmethod
    def handle_orden_cancelada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-orden')

    @staticmethod
    def handle_orden_aprobada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-orden')

    @staticmethod
    def handle_orden_pagada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-orden')


    