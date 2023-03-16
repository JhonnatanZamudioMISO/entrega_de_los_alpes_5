from aeroalpes.seedwork.aplicacion.queries import QueryHandler
from aeroalpes.modulos.pedidos.infraestructura.fabricas import FabricaVista
from aeroalpes.modulos.pedidos.dominio.fabricas import FabricaPedidos

class OrdenQueryBaseHandler(QueryHandler):
    def __init__(self):
        self._fabrica_vista: FabricaVista = FabricaVista()
        self._fabrica_pedidos: FabricaPedidos = FabricaPedidos()

    @property
    def fabrica_vista(self):
        return self._fabrica_vista
    
    @property
    def fabrica_pedidos(self):
        return self._fabrica_pedidos    