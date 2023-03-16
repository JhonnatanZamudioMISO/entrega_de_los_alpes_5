from abc import ABC
from aeroalpes.seedwork.dominio.repositorios import Repositorio

class RepositorioOrdenes(Repositorio, ABC):
    ...

class RepositorioEventosOrdenes(Repositorio, ABC):
    ...

class RepositorioProveedores(Repositorio, ABC):
    ...