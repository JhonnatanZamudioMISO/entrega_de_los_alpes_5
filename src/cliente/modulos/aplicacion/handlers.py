

from cliente.modulos.pedidos.dominio.eventos.ordenes import OrdenCreada
from cliente.seedwork.aplicacion.handlers import Handler

class HandlerOrdenDominio(Handler):

    @staticmethod
    def handle_orden_creada(evento):
        print('================ ORDEN CREADA ===========')
        

    