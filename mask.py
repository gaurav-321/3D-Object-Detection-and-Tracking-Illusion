import cv2
import numpy as np

cascade = cv2.CascadeClassifier("cars.xml")

cap = cv2.VideoCapture(1)

def nothing(x):
    pass


def get_pos(dilated_image):
    contours, hierarchy = cv2.findContours(dilated_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if (cv2.contourArea(contour)) >= 500:
            return x, y, w, h, int(cv2.contourArea(contour))


def onMouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"{x}-{y}--->x,y coordinated, {img[y, x]} rgbcolor")


pos = [int(x.strip()) for x in open("log.txt", "r").readline().split(",")]
cv2.namedWindow('image')
cv2.createTrackbar('l_R', 'image', pos[0], 255, nothing)
cv2.createTrackbar('l_G', 'image', pos[1], 255, nothing)
cv2.createTrackbar('l_B', 'image', pos[2], 255, nothing)
cv2.createTrackbar('h_R', 'image', pos[3], 255, nothing)
cv2.createTrackbar('h_G', 'image', pos[4], 255, nothing)
cv2.createTrackbar('h_B', 'image', pos[5], 255, nothing)
while cap.isOpened():
    _, img = cap.read()
    height, width, _ = img.shape
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    l_R = cv2.getTrackbarPos('l_R', 'image')
    l_G = cv2.getTrackbarPos('l_G', 'image')
    l_B = cv2.getTrackbarPos('l_B', 'image')
    h_R = cv2.getTrackbarPos('h_R', 'image')
    h_G = cv2.getTrackbarPos('h_G', 'image')
    h_B = cv2.getTrackbarPos('h_B', 'image')
    lower_blue = np.array([l_R, l_G, l_B])
    upper_blue = np.array([h_R, h_G, h_B])

    mask1 = cv2.inRange(hsv, lower_blue, upper_blue)
    kernel = np.ones((2, 2), np.uint8)
    dilated = cv2.dilate(mask1, kernel, iterations=4)

    try:
        x, y, w, h, area = get_pos(dilated)
        cv2.circle(img, (int(x + w / 2), int(y + h / 2)), 5, (255, 255, 255), -1)
        vertical_degree = int(round(y / 20))
        horizontal_degree = int(round(x / 20))
        if vertical_degree > 10:
            vertical_degree -= 20
        if horizontal_degree > 10:
            horizontal_degree -= 20
        print(horizontal_degree,vertical_degree)
    except Exception as e:
        pass

    for x in range(1, 20):
        cv2.line(img, (0, x * int(height / 20)), (width, x * int(height / 20)), (255, 255, 255), 1)
    for x in range(1, 20):
        cv2.line(img, (x * int(width / 20), 0), (x * int(width / 20), height), (255, 255, 255), 1)
    dilated = cv2.cvtColor(dilated, cv2.COLOR_GRAY2BGR)
    vis = np.concatenate((img, dilated), axis=1)
    cv2.imshow("main", vis)

    cv2.setMouseCallback('main', onMouse)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        with open("log.txt", "w") as w:
            w.write(str(f"{l_R},{l_G},{l_B},{h_R},{h_G},{h_B}"))
        break
