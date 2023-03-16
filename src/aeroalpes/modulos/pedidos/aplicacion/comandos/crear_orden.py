from aeroalpes.seedwork.aplicacion.comandos import Comando
from aeroalpes.modulos.pedidos.aplicacion.dto import ItinerarioDTO, OrdenDTO
from .base import CrearOrdenBaseHandler
from dataclasses import dataclass, field
from aeroalpes.seedwork.aplicacion.comandos import ejecutar_commando as comando

from aeroalpes.modulos.pedidos.dominio.entidades import Orden
from aeroalpes.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from aeroalpes.modulos.pedidos.aplicacion.mapeadores import MapeadorOrden
from aeroalpes.modulos.pedidos.infraestructura.repositorios import RepositorioOrdenes, RepositorioEventosOrdenes

@dataclass
class CrearOrden(Comando):
    fecha_creacion: str
    fecha_actualizacion: str
    id: str
    itinerarios: list[ItinerarioDTO]


class CrearOrdenHandler(CrearOrdenBaseHandler):
    
    def handle(self, comando: CrearOrden):
        Orden_dto = OrdenDTO(
                fecha_actualizacion=comando.fecha_actualizacion
            ,   fecha_creacion=comando.fecha_creacion
            ,   id=comando.id
            ,   itinerarios=comando.itinerarios)
        Orden: Orden = self.fabrica_pedidos.crear_objeto(Orden_dto, MapeadorOrden())
        Orden.crear_Orden(Orden)
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioOrdenes)
        repositorio_eventos = self.fabrica_repositorio.crear_objeto(RepositorioEventosOrdenes)
        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, Orden, repositorio_eventos_func=repositorio_eventos.agregar)
        UnidadTrabajoPuerto.commit()


@comando.register(CrearOrden)
def ejecutar_comando_crear_Orden(comando: CrearOrden):
    handler = CrearOrdenHandler()
    handler.handle(comando)
    