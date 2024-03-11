import cv2 as cv
import time
import pigpio

img = cv.imread("/home/zero/Desktop/codes/tests/test")
cv.imshow("Display window", img)

k = cv.waitKey(0)

print(cv.__version__)