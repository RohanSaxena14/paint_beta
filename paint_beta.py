def draw_circles(circles):
    r_max = 0
    for (x, y, r) in circles[0, :]:
        if r >= r_max:
            x_max, y_max, r_max = x, y, r
    cv2.circle(frame, (x_max, y_max), r_max, (0, 255, 0), 5)
    cv2.imshow("frame", frame)
    draw_line(x_max, y_max)

def draw_line(x_max, y_max):
    coordinates.append((x_max, y_max))
    if len(coordinates) >= 2:
        cv2.line(img, coordinates[-2], coordinates[-1], (0, 255, 0), 8)
    return

def rub_line(x_max, y_max):
    coordinates_rub.append((x_max, y_max))
    if len(coordinates_rub) >= 2:
        cv2.line(img, coordinates_rub[-2], coordinates_rub[-1], (0, 0, 0), 40)
    return
def nothing(event):
    pass
def PolyArea(x,y):
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

import cv2
import numpy as np

cap = cv2.VideoCapture(0)
coordinates = []
coordinates_rub = []
_, frame = cap.read()
img = np.zeros_like(frame)

while cap.isOpened():
    _, frame = cap.read()
    #frame = cv2.imread("shapes.png")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 7)

    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 100)

    if circles is not None:
        draw_circles(circles)

    frame = cv2.bitwise_or(frame, img)
    _, thresh = cv2.threshold(gray, 40, 255, 1)
    contours, _ = cv2.findContours(thresh, 1, 2)

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        if len(approx) == 4 :
            x, y = 0, 0
            points_x, points_y = [], []
            for i in range(4):
                points_x.append(x)
                points_y.append(y)
                x += approx[i][0][0]
                y += approx[i][0][1]
            x, y = int(x/4), int(y/4)
            area = PolyArea(points_x, points_y)
            if area > 8000:
                rub_line(x, y)
                cv2.drawContours(frame, [approx], -1, [0, 0, 255], 5)

    cv2.imshow("frame", frame)
    cv2.imshow("image", img)

    if cv2.waitKey(1) == ord("q"):
        break

cv2.destroyAllWindows()