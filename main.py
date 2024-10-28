import numpy as np
from fastapi import FastAPI, File, UploadFile
from SawMethod import Saw
from pydantic import BaseModel

app = FastAPI()

class SawModel(BaseModel):
    cantidad_Criterios: int
    cantidad_Alternativas: int
    datos: list
    alternativas: list
    criterios: list
    costos: list
    pesos: list

@app.post("/saw")
async def saw(modelo: SawModel):
    saw = Saw(int(modelo.cantidad_Criterios), int(modelo.cantidad_Alternativas), np.array(modelo.datos),
              np.array(modelo.alternativas), np.array(modelo.criterios), np.array(modelo.costos),
              np.array(modelo.pesos))
    valor = saw.calcular()
    return valor, "message: " + "Mejor alternativa: " + valor.idxmax()["Ranking"] + " con un valor de: " + str(
        valor.max()["Ranking"])

@app.post("/saw-file")
async def upload(file: UploadFile = File(...)):
    contents = await file.read()
    datos_Procesados = procesarDatos(contents.decode())
    saw = Saw(int(datos_Procesados["cantidad_Criterios"]), int(datos_Procesados["cantidad_Alternativas"]),
              np.array(datos_Procesados["datos"]), np.array(datos_Procesados["alternativas"]),
              np.array(datos_Procesados["criterios"]), np.array(datos_Procesados["costos"]),
              np.array(datos_Procesados["pesos"]))
    valor = saw.calcular()
    return valor, "message: " + "Mejor alternativa: " + valor.idxmax()["Ranking"] + " con un valor de: " + str(
        valor.max()["Ranking"])


def procesarDatos(texto):
    datos = {}
    lines = texto.strip().split("\n")
    for linea in lines:
        key, value = linea.split(": ")
        if key == "datos":
            datos[key] = eval(value)
        elif key in ["alternativas", "criterios", "costos", "pesos"]:
            datos[key] = eval(value)
        else:
            datos[key] = int(value)
    return datos
