from dataclasses import dataclass, field
from aeroalpes.seedwork.dominio.fabricas import Fabrica
from aeroalpes.seedwork.dominio.repositorios import Repositorio
from aeroalpes.seedwork.infraestructura.vistas import Vista
from aeroalpes.modulos.pedidos.infraestructura.vistas import VistaOrden
from aeroalpes.modulos.pedidos.dominio.entidades import Orden
from aeroalpes.modulos.pedidos.dominio.repositorios import RepositorioProveedores, RepositorioOrdenes, RepositorioEventosOrdenes
from .repositorios import RepositorioOrdenesSQLAlchemy, RepositorioProveedoresSQLAlchemy, RepositorioEventosOrdenesQLAlchemy
from .excepciones import ExcepcionFabrica

@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if obj == RepositorioOrdenes:
            return RepositorioOrdenesSQLAlchemy()
        elif obj == RepositorioProveedores:
            return RepositorioProveedoresSQLAlchemy()
        elif obj == RepositorioEventosOrdenes:
            return RepositorioEventosOrdenesQLAlchemy()
        else:
            raise ExcepcionFabrica(f'No existe fábrica para el objeto {obj}')

@dataclass
class FabricaVista(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Vista:
        if obj == Orden:
            return VistaOrden()
        else:
            raise ExcepcionFabrica(f'No existe fábrica para el objeto {obj}')