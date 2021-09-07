import numpy as np
import cv2

# Setup the window
cv2.namedWindow('img', cv2.WINDOW_NORMAL)
cv2.resizeWindow('img', 640, 480)
cv2.moveWindow('img', 3000, 0)

img = cv2.imread('try.jpg')
points = [[(100,200), (300,400), (500,600)], [(700,800), (900, 1000)]]# Firstly declare as a list
for elements in points:
    for elements in elements:
        cv2.circle(img, tuple(elements), 10, (0,255,0), -1)

for elements in points:
    points = np.array([elements], dtype = np.int32)
    #print(points)
    cv2.polylines(img, points, False, (255,0,0), thickness = 2)
cv2.imshow('img', img)
cv2.waitKey()