class Corpo:
    def __init__(self, massa, cor, raio, posicao_inicial, velocidade_inicial):
        self.massa = massa
        self.raio = raio
        self.cor = cor
        self.rastro = []

        self.posicao_inicial = posicao_inicial
        self.velocidade_inicial = velocidade_inicial
