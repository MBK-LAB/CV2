import numpy as np
import cv2
import matplotlib.pyplot as plt

def to_grauscale(path):
	img = cv2.imread(path)
	grayed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	return grayed

def to_matplotlib_format(img):
	return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


path = '/home/pi/gazou/test_bird.jpg'
img = to_grauscale(path)

#print(grayed.shape)
cv2.imshow("gray", img)
cv2.waitKey(0)
cv2.imwrite('/home/pi/gazou/test_bird_gray.jpg', img)
cv2.waitKey(1)
cv2.destroyAllWindows()
cv2.waitKey(1)


plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
plt.show()
