import numpy as np
import cv2
import matplotlib.pyplot as plt

path = '/home/pi/gazou/test_bird.jpg'

img = cv2.imread(path)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

pixelValue = hsv[190, 105]
print ('pixelValue = ' + str(pixelValue))
