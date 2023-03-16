from .entidades import Orden
from .reglas import MinimoUnItinerario, RutaValida
from .excepciones import TipoObjetoNoExisteEnDominioPedidosExcepcion
from aeroalpes.seedwork.dominio.repositorios import Mapeador, Repositorio
from aeroalpes.seedwork.dominio.fabricas import Fabrica
from aeroalpes.seedwork.dominio.entidades import Entidad
from aeroalpes.seedwork.dominio.eventos import EventoDominio
from dataclasses import dataclass

@dataclass
class _FabricaOrden(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad) or isinstance(obj, EventoDominio):
            return mapeador.entidad_a_dto(obj)
        else:
            orden: Orden = mapeador.dto_a_entidad(obj)

            self.validar_regla(MinimoUnItinerario(orden.itinerarios))
            [self.validar_regla(RutaValida(ruta)) for itin in orden.itinerarios for odo in itin.odos for segmento in odo.segmentos for ruta in segmento.legs]
            
            return orden

@dataclass
class FabricaPedidos(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == Orden.__class__:
            fabrica_orden = _FabricaOrden()
            return fabrica_orden.crear_objeto(obj, mapeador)
        else:
            raise TipoObjetoNoExisteEnDominioPedidosExcepcion()

