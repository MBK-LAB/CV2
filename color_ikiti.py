import numpy as np
import cv2
import matplotlib.pyplot as plt

path = '/home/pi/gazou/test_bird.jpg'

def mask_blue(path):
	img = cv2.imread(path)
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	
	blue_min = np.array([100, 170, 200], np.uint8)
	blue_max = np.array([120, 180, 255], np.uint8)
	
	blue_region = cv2.inRange(hsv, blue_min, blue_max)
	white = np.full(img.shape, 255, dtype=img.dtype)
	background = cv2.bitwise_and(white, white, mask=blue_region)
	
	inv_mask = cv2.bitwise_not(blue_region)
	extracted = cv2.bitwise_and(img, img, mask=inv_mask)
	
	masked =cv2.add(extracted, background)
	
	return masked

image = cv2.imread(path)
print(image[105, 192]) #img[Y軸, X軸]
img = mask_blue(path)
print(img[105, 192])
#print(grayed.shape)
cv2.imshow("blue", img)
cv2.waitKey(0)
cv2.imwrite('/home/pi/gazou/test_bird_blue.jpg', img)
cv2.waitKey(1)
cv2.destroyAllWindows()
cv2.waitKey(1)
