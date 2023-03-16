import pulsar,_pulsar  
from pulsar.schema import *
import uuid
import time
import logging
import traceback
import datetime

from aeroalpes.modulos.pedidos.infraestructura.schema.v1.eventos import EventoOrdenCreada
from aeroalpes.modulos.pedidos.infraestructura.schema.v1.comandos import ComandoCrearOrden


from aeroalpes.modulos.pedidos.infraestructura.proyecciones import ProyeccionOrdenesLista, ProyeccionOrdenesTotales
from aeroalpes.seedwork.infraestructura.proyecciones import ejecutar_proyeccion
from aeroalpes.seedwork.infraestructura import utils

def suscribirse_a_eventos(app=None):
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-orden', consumer_type=_pulsar.ConsumerType.Shared,subscription_name='aeroalpes-sub-eventos', schema=AvroSchema(EventoOrdenCreada))

        while True:
            mensaje = consumidor.receive()
            datos = mensaje.value().data
            print(f'Evento recibido: {datos}')
            ejecutar_proyeccion(ProyeccionOrdenesTotales(datos.fecha_creacion, ProyeccionOrdenesTotales.ADD), app=app)
            ejecutar_proyeccion(ProyeccionOrdenesLista(datos.id_orden, datos.id_cliente, datos.estado, datos.fecha_creacion, datos.fecha_creacion), app=app)
            consumidor.acknowledge(mensaje)     
        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()

def suscribirse_a_comandos(app=None):
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('comandos-orden', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='aeroalpes-sub-comandos', schema=AvroSchema(ComandoCrearOrden))

        while True:
            mensaje = consumidor.receive()
            print(f'Comando recibido: {mensaje.value().data}')

            consumidor.acknowledge(mensaje)     
            
        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()