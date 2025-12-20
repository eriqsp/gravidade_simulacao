import pygame
from pygame.locals import DOUBLEBUF, OPENGL, QUIT
from OpenGL.GL import *
from OpenGL.GLU import *
from corpo_massivo import Corpo
from fisica import *


def init_opengl(largura, altura):
    # inicia ambiente
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 1.0)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(45, largura / altura, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

    # habilita luz
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)

    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    glLightfv(GL_LIGHT0, GL_POSITION, (5.0, 5.0, 5.0, 1.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.8, 0.8, 0.8, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))

    # transparencia
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


def objeto_inicio(slices=20, stacks=20):
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    return quadric, slices, stacks


def cria_esfera(quadric, raio, slices, stacks, angulo, posicao, cor):
    glPushMatrix()
    glTranslatef(*posicao)
    glRotatef(angulo, 0, 1, 0)
    glColor3f(*cor)
    gluSphere(quadric, raio, slices, stacks)
    glPopMatrix()


def desenha_rastro(pontos):
    if len(pontos) < 2:
        return

    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)

    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_LINE_STRIP)
    for p in pontos:
        glVertex3f(p[0], p[1], p[2])
    glEnd()

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)


def main():
    pygame.init()
    largura, altura = 1600, 1200
    pygame.display.set_mode((largura, altura), DOUBLEBUF | OPENGL)

    massa = 1
    raio = 0.2
    distancia = 25.0

    objetos = [
        Corpo(massa * 300, np.array([1.0, 1.0, 0.0]), raio * 6, [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]),  # Sol
        Corpo(massa, np.array([0.2, 0.4, 0.8]), raio, [distancia, 0.0, 0.0], [0.0, 1.1, 0.0]),  # Terra
        Corpo(massa * 0.1, np.array([0.8, 0.3, 0.2]), raio * 0.5, [distancia * 1.5, 0.0, 0.0], [0.0, -1.1, 0.0]),  # Marte
        Corpo(massa * 10, np.array([0.8, 0.6, 0.4]), raio * 2.5, [distancia * 3, 0.0, 0.0], [0.0, 1.1, 0.0]),  # Jupiter
    ]

    massas = [objeto.massa for objeto in objetos]
    g = 1.0

    posicoes = np.array([objeto.posicao_inicial for objeto in objetos])
    velocidades = np.array([objeto.velocidade_inicial for objeto in objetos])
    aceleracoes = aceleracao(posicoes, massas, g)

    init_opengl(largura, altura)

    quadric, slices, stacks = objeto_inicio()
    clock = pygame.time.Clock()
    angulo = 0

    # parametros para zoom e mudanca de fov
    zoom = 1.0
    camera_distance = 50
    rot_x, rot_y = 20, -30
    mouse_down = False

    rodando = True
    while rodando:
        for event in pygame.event.get():
            if event.type == QUIT:
                rodando = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    zoom += 0.1
                if event.button == 5:
                    zoom -= 0.1
                if zoom < 0.1:
                    zoom = 0.1

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    camera_distance -= 0.5

                if event.button == 5:
                    camera_distance += 0.5

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_down = True

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_down = False

            if event.type == pygame.MOUSEMOTION and mouse_down:
                dx, dy = event.rel
                rot_y += dx * 0.5
                rot_x += dy * 0.5

            camera_distance = max(3, min(camera_distance, 50))

        angulo += 60 * clock.get_time() / 1000
        dt = 0.01

        # reinicia matriz a cada iteracao
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # camera
        glTranslatef(0, 0, -camera_distance)
        glRotatef(rot_x, 1, 0, 0)
        glRotatef(rot_y, 0, 1, 0)

        posicoes, aceleracoes = atualiza_movimento(posicoes, velocidades, aceleracoes, massas, g, dt)

        for i, objeto in enumerate(objetos):
            if i > 0:
                objeto.rastro.append(tuple(posicoes[i]))

        for i, objeto in enumerate(objetos):
            if i > 0:
                desenha_rastro(objeto.rastro)

        for i, objeto in enumerate(objetos):
            cria_esfera(quadric, objeto.raio, slices, stacks, angulo, posicoes[i], objeto.cor)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
