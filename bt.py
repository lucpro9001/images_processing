import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('./a.jpg')
print(img.shape)
blur = cv2.GaussianBlur(img, (177, 177), 100)
plt.subplot(121), plt.imshow(img), plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(img), plt.title('Blurred')
plt.xticks([]), plt.yticks([])
plt.show()