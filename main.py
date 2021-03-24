import pygame as pg
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import *
from OpenGL.GLU import *
import cv2
import numpy as np
import PIL.Image as Image
from MeshRenderer import ChairMesh, shelfMesh
import sys

print(sys.argv)
cap = cv2.VideoCapture(1)
cascade = cv2.CascadeClassifier("fixed_files/face.xml")
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
position_y, position_x = {}, {}
for x in range(height):
    if x < height / 2:
        position_y[x] = 7 - (20 / height * x)
    else:
        position_y[x] = 7 - (20 / height * x)
for x in range(width):
    if x < width / 2:
        position_x[x] = 7 - (20 / width * x)
    else:
        position_x[x] = 7 - (20 / width * x)
detection = []
cubeVertices = [
    (1, 1, 1), (1, 1, -2), (1, -1, -2), (1, -1, 1), (-1, 1, 1), (-1, -1, -2), (-1, -1, 1), (-1, 1, -2)]
cubeEdges = [
    (0, 1), (0, 3), (0, 4), (1, 2), (1, 7), (2, 5), (2, 3), (3, 6), (4, 6), (4, 7), (5, 6), (5, 7)]
last_frame = ""
for x in [1 - x * 0.1 for x in range(1, 20)]:
    max_point = max(max(cubeEdges))
    cubeVertices.append([-1, x, 1])
    cubeVertices.append([-1, x, -2])
    cubeEdges.append((max_point + 1, (max_point + 2)))

for x in [1 - x * 0.1 for x in range(1, 20)]:
    max_point = max(max(cubeEdges))
    cubeVertices.append([1, x, 1])
    cubeVertices.append([1, x, -2])
    cubeEdges.append((max_point + 1, (max_point + 2)))

for x in [1 - x * 0.1 for x in range(1, 20)]:
    max_point = max(max(cubeEdges))
    cubeVertices.append([x, 1, 1])
    cubeVertices.append([x, 1, -2])
    cubeEdges.append((max_point + 1, (max_point + 2)))

for x in [1 - x * 0.1 for x in range(1, 20)]:
    max_point = max(max(cubeEdges))
    cubeVertices.append([x, -1, 1])
    cubeVertices.append([x, -1, -2])
    cubeEdges.append((max_point + 1, (max_point + 2)))

for z in [1 - x * 0.1 for x in range(1, 30)] + [-2 + x * 0.01 for x in range(1, 10)]:
    last_val = max(cubeEdges[-1] + cubeEdges[-2]) + 1
    cubeVertices.append([-1, 1, z])
    cubeVertices.append([-1, -1, z])
    cubeVertices.append([1, -1, z])
    cubeVertices.append([1, 1, z])
    cubeEdges.append((last_val, last_val + 1))
    cubeEdges.append((last_val + 2, last_val + 3))
    cubeEdges.append((last_val, last_val + 3))
    cubeEdges.append((last_val + 2, last_val + 1))


def mean(array):
    return sum(array) / len(array)


def load_image(filename):
    im = Image.open(filename)
    return im


def get_rotation():
    global last_frame
    _, img = cap.read()
    pos = [int(x.strip()) for x in open("log.txt", "r").readline().split(",")]
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    blank_image = np.ones((height, width, 3), np.uint8)
    blank_image.fill(255)

    def get_pos(dilated_image):
        contours, hierarchy = cv2.findContours(dilated_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if (cv2.contourArea(contour)) >= 500:
                return x, y, w, h, int(cv2.contourArea(contour))

    lower_blue = np.array(pos[:3])
    upper_blue = np.array(pos[3:])

    mask1 = cv2.inRange(hsv, lower_blue, upper_blue)
    kernel = np.ones((2, 2), np.uint8)
    dilated = cv2.dilate(mask1, kernel, iterations=6)

    try:
        x, y, w, h, area = get_pos(dilated)
        cv2.circle(blank_image, (int(x + w / 2), int(y + h / 2)), 5, (255, 255, 0), -1)
        detection.append([int(round((x + w / 2))), int(round((y + h / 2))), width, height])

    except Exception as e:
        pass
    cv2.imwrite("face.png", blank_image)


def get_rotation_by_face():
    global cascade, height, width
    _, frame = cap.read()
    faces = cascade.detectMultiScale(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 1.1, 5, minSize=(50, 50))
    blank_image = np.ones((height, width, 3), np.uint8)
    blank_image.fill(255)
    for (x, y, w, h) in faces:
        if len(detection) > 20:
            detection.append([int(round((x + w / 2))), int(round((y + h / 2))), w, h])
            cv2.rectangle(blank_image, (x, y), (x + w, y + h), (0, 255, 0), 3)
        else:
            detection.append([int(round((x + w / 2))), int(round((y + h / 2))), w, h])
            cv2.rectangle(blank_image, (x, y), (x + w, y + h), (0, 255, 0), 3)

        break

    cv2.imwrite("face.png", blank_image)


def display_pic():
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glEnable(GL_TEXTURE_2D)
    img = load_image("face.png")
    width, height = img.width, img.height
    textureData = img.tobytes("raw", "RGB", 0, -1)
    im = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, im)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, textureData)

    glEnable(GL_TEXTURE_2D)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(-1, -1, -2)
    glTexCoord2f(0, 1)
    glVertex3f(-1, 1, -2)
    glTexCoord2f(1, 1)
    glVertex3f(1, 1, -2)
    glTexCoord2f(1, 0)
    glVertex3f(1, -1, -2)
    glEnd()
    # glClearColor(133 / 255, 138 / 255, 255 / 255, 1)


def wireCube():
    glBegin(GL_LINES)
    for cubeEdge in cubeEdges:
        for cubeVertex in cubeEdge:
            glColor3fv((1, 1, 1))
            glVertex3fv(cubeVertices[cubeVertex])
    glEnd()


def draw_sphere(pos, sphere):
    glPushMatrix()
    glTranslated(pos[0], pos[1], pos[2])  # Move to the place
    glColor4f(0, 1, 1, 1)  # Put color
    gluSphere(sphere, 0.1, 30, 30)  # Draw sphere
    glPopMatrix()


def main():
    pg.init()
    x_rotation, y_rotation = 0, 0
    display = (1920, 1080)
    pg.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -2.3)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_BLEND)
    glEnable(GL_DEPTH_TEST)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    glEnable(GL_LINE_SMOOTH)
    glClearColor(133 / 255, 138 / 255, 255 / 255, 1)
    glClear(GL_COLOR_BUFFER_BIT)
    # glRotatef(0, 2, 0, 100)
    glClear(GL_COLOR_BUFFER_BIT)
    detection_method = get_rotation_by_face

    if len(sys.argv) > 1:
        if sys.argv[1] == "mask":
            detection_method = get_rotation
        else:
            detection_method = get_rotation_by_face

    def update_screen():
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        wireCube()
        ChairMesh(0)
        shelfMesh(0)
        display_pic()
        pg.display.flip()
        pg.time.wait(1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def reset(x_rotation, y_rotation):
        glRotatef(-x_rotation, 0, 1, 0)
        glRotatef(-y_rotation, 1, 0, 0)
        update_screen()
        detection.clear()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    reset(x_rotation, y_rotation)
                    x_rotation = 0
                    y_rotation = 0

        try:
            detection_method()
            if len(detection) > 2:
                x_cord, y_cord, _, _ = detection[-1]
                glRotatef(-y_rotation, 1, 0, 0)
                glRotatef(position_y[y_cord], 1, 0, 0)
                y_rotation = position_y[y_cord]
                glRotatef(-x_rotation, 0, 1, 0)
                glRotatef(position_x[x_cord], 0, 1, 0)
                x_rotation = position_x[x_cord]
                update_screen()
        except Exception as e:
            print(e)
            pass

        if len(detection) < 2:
            update_screen()


if __name__ == "__main__":
    main()
