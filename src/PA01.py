import cv2
import numpy as np

srcImg = cv2.imread('../data_input/peppers.pgm', 0)
cv2.imshow('image', srcImg)

waitKey(0)