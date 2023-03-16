from aeroalpes.seedwork.aplicacion.comandos import ComandoHandler
from aeroalpes.modulos.pedidos.infraestructura.fabricas import FabricaRepositorio
from aeroalpes.modulos.pedidos.dominio.fabricas import FabricaPedidos

class CrearOrdenBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_pedidos: FabricaPedidos = FabricaPedidos()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_pedidos(self):
        return self._fabrica_pedidos    
    