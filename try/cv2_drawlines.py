import cv2
import numpy as np

# Handle the display
cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Image', 640, 480)
cv2.moveWindow('Image', 800, 0)

# Open the image
path = 'try.jpg'
img = cv2.imread(path)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Get the features
desc = cv2.goodFeaturesToTrack(img, 5, 0.01, 20)
kps = [cv2.KeyPoint(x=f[0][0], y=f[0][1], _size=20) for f in desc]
img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
desc = np.int0(desc)
for pts in desc:
    u,v = pts.ravel()
    cv2.circle(img, (u,v), 100, (0,255,0))

points = []
for pts in desc:
    points.append(pts)

print(points)

points = np.array([points], dtype = np.int32)

print(points)

cv2.imshow('Image', img)
cv2.waitKey()
