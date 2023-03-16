import pulsar
from pulsar.schema import *

from aeroalpes.modulos.pedidos.infraestructura.schema.v1.eventos import EventoOrdenCreada, OrdenCreadaPayload
from aeroalpes.modulos.pedidos.infraestructura.schema.v1.comandos import ComandoCrearOrden, ComandoCrearOrdenPayload
from aeroalpes.seedwork.infraestructura import utils

from aeroalpes.modulos.pedidos.infraestructura.mapeadores import MapeadorEventosOrden

class Despachador:
    def __init__(self):
        self.mapper = MapeadorEventosOrden()

    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=AvroSchema(EventoOrdenCreada))
        publicador.send(mensaje)
        cliente.close()

    def publicar_evento(self, evento, topico):
        evento = self.mapper.entidad_a_dto(evento)
        self._publicar_mensaje(evento, topico, AvroSchema(evento.__class__))

    def publicar_comando(self, comando, topico):
        payload = ComandoCrearOrdenPayload(
            id_usuario=str(comando.id_usuario)
            # agregar itinerarios
        )
        comando_integracion = ComandoCrearOrden(data=payload)
        self._publicar_mensaje(comando_integracion, topico, AvroSchema(ComandoCrearOrden))
