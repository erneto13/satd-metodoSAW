import numpy as np
import numpy
import pandas as pd

class Saw:
    def __init__(self, cantidad_Criterios, cantidad_Alternativas, datos, alternativas, criterios, costos: numpy.ndarray,
                 pesos):
        self.cantidad_Criterios = cantidad_Criterios
        self.cantidad_Alternativas = cantidad_Alternativas
        self.datos = datos
        self.alternativas = alternativas
        self.criterios = criterios
        self.costos = costos
        self.pesos = pesos

    def retTablaFormateada(self) -> pd.DataFrame:
        return pd.DataFrame(self.datos, columns=self.criterios, index=self.alternativas)

    def normalizar(self) -> numpy.ndarray:
        row_Size, col_Size = self.datos.shape
        tabla_Normalizada = np.zeros((row_Size, col_Size), dtype=float)
        for row in range(row_Size):
            for col in range(col_Size):
                if np.isin(self.criterios[col], self.costos):
                    tabla_Normalizada[row][col] = np.round(np.min(self.datos[:, col]) / self.datos[row][col], 2)
                else:
                    tabla_Normalizada[row][col] = self.datos[row][col] / np.max(self.datos[:, col])
        return tabla_Normalizada

    def ponderar(self, pesos: numpy.ndarray, tabla) -> numpy.ndarray:
        tabla_Ponderada = np.zeros(self.cantidad_Alternativas, dtype=float)
        for i in range(self.cantidad_Alternativas):
            tabla_Ponderada[i] = np.sum(pesos * tabla[i])
        return tabla_Ponderada

    def calcular(self):
        tabla_Normalizada = self.normalizar()
        tabla_Ponderada = self.ponderar(self.pesos, tabla_Normalizada)
        ranking_Tabla = pd.DataFrame(tabla_Ponderada, columns=["Ranking"], index=self.alternativas)
        return ranking_Tabla
