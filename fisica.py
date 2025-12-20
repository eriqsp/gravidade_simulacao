import numpy as np


def aceleracao(posicoes: np.array, massas: list, g: float):
    a = np.zeros_like(posicoes)
    n = len(posicoes)
    for i in range(n):
        for j in range(n):
            if i != j:
                r = posicoes[j] - posicoes[i]
                d = np.linalg.norm(r) + 0.0  # distancia entre os corpos + um pequeno drift
                a[i] += massas[j] * g * r / d ** 3
    return a


def atualiza_movimento(posicoes: np.array, velocidades: np.array, aceleracoes: np.array, massas: list, g: float, dt: float):
    posicoes += velocidades * dt + aceleracoes * 0.5 * dt ** 2

    aceleracoes_new = aceleracao(posicoes, massas, g)
    velocidades += dt * 0.5 * (aceleracoes + aceleracoes_new)
    return posicoes, aceleracoes_new
