from fixed_files.cup import *
from OpenGL.GL import *
from fixed_files.shelf import *


chair_verticies_vector3 = [tuple([((vertices[i] - min([x[i] for x in chair_verticies_vector3])) / (
                max([x[i] for x in chair_verticies_vector3]) - min([x[i] for x in chair_verticies_vector3]))) * (
                                  1 - (-1)) + (-1) for i in range(3)]) for vertices in chair_verticies_vector3]
colors = [(1, 1, 0)]


def ChairMesh(zaxis):

    glBegin(GL_QUADS)
    for face in chair_faces_vector4:
        x = 0
        for vertex in face:
            x += 1
            vertices = chair_verticies_vector3[vertex]
            vertices = [x/10 for x in vertices]
            vertices[2] *= 2
            vertices[1] += 0.11
            vertices[0] += 0.005
            glColor3fv((255/255,0,0))
            glVertex3fv(vertices)
    glEnd()

    glBegin(GL_LINES)
    for edge in chair_edges_vector2:
        for vertex in edge:
            vertices = chair_verticies_vector3[vertex]
            vertices = [x/10 for x in vertices]
            vertices[2] *= 2
            vertices[1] += 0.11
            vertices[0] += 0.005
            glVertex3fv(vertices)
    glEnd()


def shelfMesh(zaxis):

    colors = (
        (253, 245, 230),
        (244, 164, 96),
        (244, 164, 96),
        (205, 133, 63),
        (205, 133, 63),
        (160, 82, 45),
    )

    glBegin(GL_QUADS)
    for face, color in zip(shelf_faces_vector4, colors):
        for vertex in face:
            vertices = shelf_verticies_vector3[vertex]
            glColor3fv(tuple([x / 255 for x in color]))
            glVertex3fv(vertices)
    glEnd()

    glBegin(GL_LINES)
    for edge in shelf_edges_vector2:
        for vertex in edge:
            vertices = shelf_verticies_vector3[vertex]
            glVertex3fv(vertices)
    glEnd()
