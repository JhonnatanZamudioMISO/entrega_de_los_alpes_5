from aeroalpes.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from aeroalpes.seedwork.aplicacion.queries import ejecutar_query as query
from aeroalpes.modulos.pedidos.infraestructura.repositorios import RepositorioOrdenes
from aeroalpes.modulos.pedidos.dominio.entidades import Orden
from dataclasses import dataclass
from .base import OrdenQueryBaseHandler
from aeroalpes.modulos.pedidos.aplicacion.mapeadores import MapeadorOrden
import uuid

@dataclass
class ObtenerOrden(Query):
    id: str

class ObtenerOrdenHandler(OrdenQueryBaseHandler):

    def handle(self, query: ObtenerOrden) -> QueryResultado:
        vista = self.fabrica_vista.crear_objeto(Orden)
        Orden =  self.fabrica_pedidos.crear_objeto(vista.obtener_por(id=query.id)[0], MapeadorOrden())
        return QueryResultado(resultado=Orden)

@query.register(ObtenerOrden)
def ejecutar_query_obtener_Orden(query: ObtenerOrden):
    handler = ObtenerOrdenHandler()
    return handler.handle(query)