from fastapi import FastAPI
import asyncio
import time
import traceback
import uvicorn

from pydantic import BaseSettings
from typing import Any

from .eventos import EventoPago, PagoRevertido, ordenPagada
from .comandos import ComandoPagarorden, ComandoRevertirPago, RevertirPagoPayload, PagarordenPayload
from .consumidores import suscribirse_a_topico
from .despachadores import Despachador

from . import utils

class Config(BaseSettings):
    APP_VERSION: str = "1"

settings = Config()
app_configs: dict[str, Any] = {"title": "Pagos AeroAlpes"}

app = FastAPI(**app_configs)
tasks = list()

@app.on_event("startup")
async def app_startup():
    global tasks
    task1 = asyncio.ensure_future(suscribirse_a_topico("evento-pago", "sub-pagos", EventoPago))
    task2 = asyncio.ensure_future(suscribirse_a_topico("comando-pagar-orden", "sub-com-pagos-ordenar", ComandoPagarorden))
    task3 = asyncio.ensure_future(suscribirse_a_topico("comando-revertir-pago", "sub-com-pagos-revertir", ComandoRevertirPago))
    tasks.append(task1)
    tasks.append(task2)
    tasks.append(task3)

@app.on_event("shutdown")
def shutdown_event():
    global tasks
    for task in tasks:
        task.cancel()

@app.get("/prueba-orden-pagada", include_in_schema=False)
async def prueba_orden_pagada() -> dict[str, str]:
    payload = ordenPagada(
        id = "1232321321",
        id_correlacion = "389822434",
        orden_id = "6463454",
        monto = 23412.12,
        monto_vat = 234.0,
        fecha_creacion = utils.time_millis()
    )

    evento = EventoPago(
        time=utils.time_millis(),
        ingestion=utils.time_millis(),
        datacontenttype=ordenPagada.__name__,
        orden_pagada = payload
    )
    despachador = Despachador()
    despachador.publicar_mensaje(evento, "evento-pago")
    return {"status": "ok"}

@app.get("/prueba-pago-revertido", include_in_schema=False)
async def prueba_pago_revertido() -> dict[str, str]:
    payload = PagoRevertido(
        id = "1232321321",
        id_correlacion = "389822434",
        orden_id = "6463454",
        fecha_actualizacion = utils.time_millis()
    )

    evento = EventoPago(
        time=utils.time_millis(),
        ingestion=utils.time_millis(),
        datacontenttype=PagoRevertido.__name__,
        pago_revertido = payload
    )
    despachador = Despachador()
    despachador.publicar_mensaje(evento, "evento-pago")
    return {"status": "ok"}
    
@app.get("/prueba-pagar-orden", include_in_schema=False)
async def prueba_pagar_orden() -> dict[str, str]:
    payload = PagarordenPayload(
        id_correlacion = "389822434",
        orden_id = "6463454",
        monto = 23412.12,
        monto_vat = 234.0,
    )

    comando = ComandoPagarorden(
        time=utils.time_millis(),
        ingestion=utils.time_millis(),
        datacontenttype=ordenPagada.__name__,
        data = payload
    )
    despachador = Despachador()
    despachador.publicar_mensaje(comando, "comando-pagar-orden")
    return {"status": "ok"}

@app.get("/prueba-revertir-pago", include_in_schema=False)
async def prueba_revertir_pago() -> dict[str, str]:
    payload = RevertirPagoPayload(
        id = "1232321321",
        id_correlacion = "389822434",
        orden_id = "6463454",
    )

    comando = ComandoRevertirPago(
        time=utils.time_millis(),
        ingestion=utils.time_millis(),
        datacontenttype=RevertirPagoPayload.__name__,
        data = payload
    )
    despachador = Despachador()
    despachador.publicar_mensaje(comando, "comando-revertir-pago")
    return {"status": "ok"}