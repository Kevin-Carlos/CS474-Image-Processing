from PIL import Image
import numpy as np
import math
import matplotlib.pyplot as plt


def Experiment3():

  # Load the image
  image = Image.open("./data_input/lenna.pgm")
  pixels = list(image.getdata())
  width, height = image.size
  newImage = Image.new("L", (width, height))
  pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]


  # Center the pixels


Experiment3()