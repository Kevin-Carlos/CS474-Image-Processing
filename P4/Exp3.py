from PIL import Image
import numpy as np
import cmath
import math
import matplotlib.pyplot as plt
from FFT import *



def Experiment3():

  # Load the image
  image = Image.open("./data_input/lenna.pgm")
  pixels = list(image.getdata())
  width, height = image.size
  newImage = Image.new("L", (width, height))
  pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]


  # # N = height x width
  N = (newImage.size[0] + newImage.size[1]) // 4
  print(N, width, height)
  isign = -1

  newPixels = pixels

  pixels = normalizeImage(pixels, height, width, N)
          
  # Iterate over all the rows and store it into test2D
  pixels = ApplyFFTRow(pixels, width, N, isign)
          
  # Iterate over all the columns and store it into pixels
  pixels = ApplyFFTCol(pixels, height, N, isign)

  # pixels = np.fft.fftshift(np.fft.fft2(pixels))

  minVal = 1000000000000000000000000000
  maxVal = -101010100000000000000000000

  pixels = blurImage(pixels, height, width, 1, 0.1, 0.1)

  # pixels = np.fft.ifftshift(pixels)
  # pixels = np.real(np.fft.ifft2(pixels))
  
  # newImage = LinearScaleValues(newImage, maxVal, minVal, pixels, height, width)
  # newImage = LogScaleValues(newImage, maxVal, minVal, pixels, height, width)

  ################################## Do the reverse ##################################   
  # Iterate over all the columns and store it into pixels
  pixels = ApplyFFTCol(pixels, height, N, 1)

  # Iterate over all the rows and store it into test2D
  pixels = ApplyFFTRow(pixels, width, N, 1)

  # # pixels = changeAmplitudeSpatial(pixels, height, width, N, 1)
  newImage = LinearScaleValues(newImage, maxVal, minVal, pixels, height, width)

  newImage.save("./data_output/motion_blurred_lenna.png")
  # newImage1.save("./data_output/GaussianRadius.png")


def blurImage(array, height, width, T, a, b):

  for i in range(width):
    for j in range(height):
      # distanceToCenter = math.sqrt((i - (width//2))**2 + (j - (height//2))**2)

      # if(i == 0 and j == 0):
      #   H = 1
      #   print(H)
      #   print(array[i][j])
      # else:
      #   H = (T / (cmath.pi*(i*a + j*b))) * cmath.sin( cmath.pi * (i*a + j*b)) * cmath.e**( -(cmath.sqrt(-1)) * cmath.pi * (i*a + j*b))
      try:
        H = ( T / ( cmath.pi*( ( (i - (width//2)) *a) + ( (j - (height//2))*b) ) ) ) * cmath.sin( cmath.pi * ( ( (i - (width//2)) *a) + ( (j - (height//2))*b) ) ) * cmath.e**( -(cmath.sqrt(-1)) * cmath.pi * ( ( (i - (width//2)) *a) + ( (j - (height//2))*b) ))
      except:
        H = 1

      # H = cmath.e**( -0.0025* (( (i)**2 +  (j)**2)**(5/6)))

      Hr = np.real(H)
      # G = box_muller(0.0, 1.0)
      # if(j % 2 or i % 2):
      array[i][j] = array[i][j] * Hr
      array[i][j] = array[i][j] / Hr


  return array


def box_muller(m, s):
  y2 = x1 = x2 = 0.0
  use_last = 0

  if use_last:
    y1 = y2
    use_last = 0
  else:
    while True:
      x1 = 2.0 * np.random.random_sample() - 1.0
      x2 = 2.0 * np.random.random_sample() - 1.0
      w = x1 * x1 + x2 * x2

      if (w <= 1.0):
        break
    w = math.sqrt( (-2.0 * math.log( w )) / w )
    y1 = x1 * w
    y2 = x2 * w
    use_last = 1

  return (m + y1 * s)














Experiment3()