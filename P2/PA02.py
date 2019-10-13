from PIL import Image
import numpy as np

def Correlation(mask_size, mask):
    image = Image.open("./data_input/Image.pgm")
    # im.save("./data_output/Pattern.pgm")

    width = mask_size[0]
    height = mask_size[1]

    # normalizedMask = Normalize(width, height, mask)
    normalizedMask = list(mask.getdata())
    normalizedMask = [normalizedMask[i * width: (i+1) * width] for i in range(height)]

    newImage = MapCorrelation(mask, image, normalizedMask)
    normalizedMask = Normalize(width, height, newImage)

    normalizedMask.save("./data_output/Correlation.pgm")
    

def Normalize(width, height, normalized):

    correlatedMap = Image.new("L", (normalized.shape[0], normalized.shape[1]))
    

    # pixels = list(mask.getdata())
    # pixels = [pixels[i * width: (i+1) * width] for i in range(height)]
    

    maxVal = -15415660
    minVal = 15464500000
   
    for i in range(height):
        for j in range(width):
            if(maxVal < normalized[i][j]):
                maxVal = normalized[i][j]
            if(minVal > normalized[i][j]):
                minVal = normalized[i][j]

                
    print("maxVal: ", maxVal, "minVal: ", minVal)

    for rows in range(height):
        for cols in range(width):
            try:
                value = int(((normalized[rows][cols] - minVal)//(maxVal - minVal)) * 255)
            # print(value)
            except:
                value = 0
            correlatedMap.putpixel((rows,cols), value)
            
    return correlatedMap

def MapCorrelation(mask, image, normalizedMask):
    # Initiffize pixel values
    imagePixels = list(image.getdata())
    imagePixels = [imagePixels[i * image.size[0]: (i+1) * image.size[0]] for i in range(image.size[1])]

    newImage = np.empty([image.size[0], image.size[1]])
    
    # Allocate a new image type of same size
    correlatedMap = Image.new("L", (image.size[0], image.size[1]))

    # This loop is for the image itself, going from 0 to whatever the end is
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            
            # This goes into a funciton to do the summation/apply the mask for the i, j pixel position
            value = int(ApplyMask(i, j, mask, image, normalizedMask, imagePixels))



            # print(value)

            try:
                # correlatedMap.putpixel((i,j), value)
                newImage[i][j] = value
            except:
                pass
            
    return newImage
    # print(correlatedPixels)


    
    
def ApplyMask(i, j, mask, image, maskPixels, imagePixels):
    summation = 0
    Hinc = 0

    # This loop loops from -K/2 to K/2 on the mask and calculates the corresponding coordinate to map it to, so 0,0 on the image is -41, -27 for the pattern
    for row in range(-(mask.size[0] // 2), mask.size[0] // 2):
        Winc = 0
        for col in range(-(mask.size[1] // 2), mask.size[1] // 2):

            
            imageCoordH = i - (mask.size[1] // 2) + Hinc #Height or Row
            imageCoordW = j - (mask.size[0] // 2) + Winc #Width or Col
           

            checkRight = image.size[0] - (imageCoordW + mask.size[0])
            checkBottom = image.size[1] - (imageCoordH + mask.size[1])

           
            # print("image Width: ", image.size[0], "image Height: ",image.size[1])
            # print("Row: ", imageCoordH, "Col: ", imageCoordW, "Dist to right: ", checkRight, "Dist to Bottom: ", checkBottom)
            # print("IMG Row: ", imageCoordH, "IMG Col: ", imageCoordW, "Mask Row: ", row, "Mask Col: ", col)
            # print("IMG Row: ", imageCoordH, "IMG Col: ", imageCoordW, "Mask Row: ", row, "Mask Col: ", col, "mask Pixel: ", maskPixels[row][col], "img Pixel: ", imagePixels[imageCoordH][imageCoordW])
            # Make sure the coord is within bounds otherwise just call it 0
            if(imageCoordW > 0 and imageCoordH > 0 and checkBottom > 0 and checkRight > 0):
                # print("O:", imagePixels[imageCoordW][imageCoordH], "M:", maskPixels[row][col])
                summation = summation + (maskPixels[row][col] * imagePixels[imageCoordH][imageCoordW])
                # print("try")
            else:
                # print("except")
                summation = summation + 0
            
            Winc += 1
        Hinc += 1

    # print(summation)
    return summation 

maskImage = Image.open("./data_input/Pattern.pgm")
Correlation(maskImage.size, maskImage)