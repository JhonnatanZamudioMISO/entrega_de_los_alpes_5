from cliente.seedwork.aplicacion.comandos import Comando, ComandoHandler

import uuid

@dataclass
class ComandoAgregarOrdenUsuario(Comando):
    id_usuario: uuid.UUID
    id_orden: uuid.UUID

class AgregarOrdenUsuarioHandler(ComandoHandler):
    ...