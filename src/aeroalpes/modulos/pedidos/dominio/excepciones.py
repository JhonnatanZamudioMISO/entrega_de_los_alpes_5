""" Excepciones del dominio de Pedidos

En este archivo usted encontrará los Excepciones relacionadas
al dominio de Pedidos

"""

from aeroalpes.seedwork.dominio.excepciones import ExcepcionFabrica

class TipoObjetoNoExisteEnDominioPedidosExcepcion(ExcepcionFabrica):
    def __init__(self, mensaje='No existe una fábrica para el tipo solicitado en el módulo de Pedidos'):
        self.__mensaje = mensaje
    def __str__(self):
        return str(self.__mensaje)