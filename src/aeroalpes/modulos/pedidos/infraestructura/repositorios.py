from aeroalpes.config.db import db
from aeroalpes.modulos.pedidos.dominio.repositorios import RepositorioOrdenes, RepositorioProveedores, RepositorioEventosOrdenes
from aeroalpes.modulos.pedidos.dominio.objetos_valor import NombreAero, Odo, Leg, Segmento, Itinerario, CodigoIATA
from aeroalpes.modulos.pedidos.dominio.entidades import Proveedor, Aeropuerto, Orden
from aeroalpes.modulos.pedidos.dominio.fabricas import FabricaPedidos
from .dto import Orden as OrdenDTO
from .dto import EventosOrden
from .mapeadores import MapeadorOrden, MapadeadorEventosOrden
from uuid import UUID
from pulsar.schema import *

class RepositorioProveedoresSQLAlchemy(RepositorioProveedores):

    def obtener_por_id(self, id: UUID) -> Orden:
        # TODO
        raise NotImplementedError

    def obtener_todos(self) -> list[Orden]:
        origen=Aeropuerto(codigo="CPT", nombre="Cape Town International")
        destino=Aeropuerto(codigo="JFK", nombre="JFK International Airport")
        legs=[Leg(origen=origen, destino=destino)]
        segmentos = [Segmento(legs)]
        odos=[Odo(segmentos=segmentos)]

        proveedor = Proveedor(codigo=CodigoIATA(codigo="AV"), nombre=NombreAero(nombre= "Avianca"))
        proveedor.itinerarios = [Itinerario(odos=odos, proveedor=proveedor)]
        return [proveedor]

    def agregar(self, entity: Orden):
        # TODO
        raise NotImplementedError

    def actualizar(self, entity: Orden):
        # TODO
        raise NotImplementedError

    def eliminar(self, entity_id: UUID):
        # TODO
        raise NotImplementedError


class RepositorioOrdenesSQLAlchemy(RepositorioOrdenes):

    def __init__(self):
        self._fabrica_pedidos: FabricaPedidos = FabricaPedidos()

    @property
    def fabrica_pedidos(self):
        return self._fabrica_pedidos

    def obtener_por_id(self, id: UUID) -> Orden:
        Orden_dto = db.session.query(OrdenDTO).filter_by(id=str(id)).one()
        return self.fabrica_pedidos.crear_objeto(Orden_dto, MapeadorOrden())

    def obtener_todos(self) -> list[Orden]:
        # TODO
        raise NotImplementedError

    def agregar(self, Orden: Orden):
        Orden_dto = self.fabrica_pedidos.crear_objeto(Orden, MapeadorOrden())

        db.session.add(Orden_dto)

    def actualizar(self, Orden: Orden):
        # TODO
        raise NotImplementedError

    def eliminar(self, Orden_id: UUID):
        # TODO
        raise NotImplementedError

class RepositorioEventosOrdenesQLAlchemy(RepositorioEventosOrdenes):

    def __init__(self):
        self._fabrica_pedidos: FabricaPedidos = FabricaPedidos()

    @property
    def fabrica_pedidos(self):
        return self._fabrica_pedidos

    def obtener_por_id(self, id: UUID) -> Orden:
        Orden_dto = db.session.query(OrdenDTO).filter_by(id=str(id)).one()
        return self.fabrica_pedidos.crear_objeto(Orden_dto, MapadeadorEventosOrden())

    def obtener_todos(self) -> list[Orden]:
        raise NotImplementedError

    def agregar(self, evento):
        Orden_evento = self.fabrica_pedidos.crear_objeto(evento, MapadeadorEventosOrden())

        parser_payload = JsonSchema(Orden_evento.data.__class__)
        json_str = parser_payload.encode(Orden_evento.data)

        evento_dto = EventosOrden()
        evento_dto.id = str(evento.id)
        evento_dto.id_entidad = str(evento.id_orden)
        evento_dto.fecha_evento = evento.fecha_creacion
        evento_dto.version = str(Orden_evento.specversion)
        evento_dto.tipo_evento = evento.__class__.__name__
        evento_dto.formato_contenido = 'JSON'
        evento_dto.nombre_servicio = str(Orden_evento.service_name)
        evento_dto.contenido = json_str

        db.session.add(evento_dto)

    def actualizar(self, Orden: Orden):
        raise NotImplementedError

    def eliminar(self, Orden_id: UUID):
        raise NotImplementedError
