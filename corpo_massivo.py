from typing import Union
import numpy as np


class Corpo:
    def __init__(self,
                 massa: Union[float, int],
                 cor: Union[list, np.array],
                 raio: Union[float, int],
                 posicao_inicial: Union[list, np.array],
                 velocidade_inicial: Union[list, np.array]):

        self.massa = massa
        self.raio = raio
        self.cor = cor
        self.rastro = []

        self.posicao_inicial = posicao_inicial
        self.velocidade_inicial = velocidade_inicial
