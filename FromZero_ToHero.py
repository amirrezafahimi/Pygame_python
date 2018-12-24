import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np
import math

translationSpeed = 5
scaleSpeed = 1.1
rotationSpeed = 0.1 * math.pi

p1 = [0, 0, 1]
p2 = [20, 0, 1]
p3 = [20, 20, 1]
p4 = [0, 20, 1]
vertices = [p1, p2, p3, p4]


def translate(vertices, m, n):
    trans = np.matrix([[1, 0, 0], [0, 1, 0], [m, n, 1]])

    for index, point in enumerate(vertices):
        vertices[index] = (np.matrix([point]) * trans).tolist()[0]
    print(trans)


def scale(vertices, s):
    scale = np.matrix([[s, 0, 0], [0, s, 0], [0, 0, 1]])
    for index, point in enumerate(vertices):
        vertices[index] = (np.matrix([point]) * scale).tolist()[0]
    print(scale)


def rotate(vertices, theta):
    rotate = np.matrix([[math.cos(theta), math.sin(theta), 0], [-math.sin(theta), math.cos(theta), 0], [0, 0, 1]])
    for index, point in enumerate(vertices):
        vertices[index] = (np.matrix([point]) * rotate).tolist()[0]
    print(rotate)


def local_scale(vertices, s):
    m1 = np.matrix([[1, 0, 0], [0, 1, 0], [-vertices[0][0], -vertices[0][1], 1]])
    m2 = np.matrix([[s, 0, 0], [0, s, 0], [0, 0, 1]])
    m3 = np.matrix([[1, 0, 0], [0, 1, 0], [vertices[0][0], vertices[0][1], 1]])
    final_matrix = m1 * m2 * m3
    for index, point in enumerate(vertices):
        vertices[index] = (np.matrix([point]) * final_matrix).tolist()[0]
    print(f'{m1}, {m2}, {m3}')


def local_rotate(vertices, s):
    m1 = np.matrix([[1, 0, 0], [0, 1, 0], [-vertices[0][0], -vertices[0][1], 1]])
    m2 = rotate = np.matrix([[math.cos(s), math.sin(s), 0], [-math.sin(s), math.cos(s), 0], [0, 0, 1]])
    m3 = np.matrix([[1, 0, 0], [0, 1, 0], [vertices[0][0], vertices[0][1], 1]])
    final_matrix = m1 * m2 * m3
    for index, point in enumerate(vertices):
        vertices[index] = (np.matrix([point]) * final_matrix).tolist()[0]
    print(f'{m1}, {m2}, {m3}')


def init():
    pygame.init()
    display = (800, 800)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    # setting up display '2d orthogonal' coord system
    gluOrtho2D(-100, 100, -100, 100)
    # setting clear color i.e. background color
    glClearColor(0.3, 0.5, 1.0, 1.0)


def event_handler():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

            if event.key == pygame.K_UP:
                translate(vertices, 0, translationSpeed)
            if event.key == pygame.K_DOWN:
                translate(vertices, 0, -translationSpeed)
            if event.key == pygame.K_RIGHT:
                translate(vertices, translationSpeed, 0)
            if event.key == pygame.K_LEFT:
                translate(vertices, -translationSpeed, 0)

            if event.key == pygame.K_w:
                scale(vertices, scaleSpeed)
            if event.key == pygame.K_s:
                scale(vertices, 1.0 / scaleSpeed)

            if event.key == pygame.K_a:
                rotate(vertices, rotationSpeed)
            if event.key == pygame.K_d:
                rotate(vertices, -rotationSpeed)

            if event.key == pygame.K_k:
                local_scale(vertices, 1.0 / scaleSpeed)
            if event.key == pygame.K_i:
                local_scale(vertices, scaleSpeed)
            if event.key == pygame.K_l:
                local_rotate(vertices, -rotationSpeed)
            if event.key == pygame.K_j:
                local_rotate(vertices, rotationSpeed)


def draw_grid():
    glColor3fv([1.0, 0.0, 0.0])
    glLineWidth(1.0)
    glBegin(GL_LINES)
    glVertex2fv([0, -100])
    glVertex2fv([0, 100])
    glVertex2fv([-100, 0])
    glVertex2fv([100, 0])
    glEnd()


def draw_box(vertices):
    glColor3fv([0.0, 1.0, 1.0])
    glPolygonMode(GL_FRONT, GL_LINE)
    glLineWidth(3.0)
    glBegin(GL_QUADS)
    glVertex2fv(vertices[0][:2])
    glVertex2fv(vertices[1][:2])
    glVertex2fv(vertices[2][:2])
    glVertex2fv(vertices[3][:2])
    glEnd()


# this one draw's stuff to the screen.
def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    draw_grid()
    draw_box(vertices)


def main():
    # pygame initialization

    print('\n\n')
    print('you\'re rotating transforming abound the origin(0,0)')
    print('press arrow keys for translation')
    print('press w, s keys for scaling')
    print('press a, d keys for rotation')
    print('press k, i keys for scaling locally')
    print('press l, j keys for rotating locally')
    print('press escape key to quit')
    init()

    # this is the main 'game' loop
    while True:
        # poll events here
        event_handler()

        # render here
        render()

        # swap buffers (don't worry about this)
        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == '__main__':
    main()
