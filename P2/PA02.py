from PIL import Image
import numpy as np

def grab_mask(mask_size):
    maskImage = Image.open("./data_input/Pattern.pgm")
    # im.save("./data_output/Pattern.pgm")

    pixels = list(maskImage.getdata())
    width, height = maskImage.size
    pixels = [pixels[i * width: (i+1) * width] for i in range(height)]

    # grab the neighborhood for mask
    mask = []
    for i in range(height): #rows
        for j in range(width): #columns

                if (pixels[i][j] != 0):
                    # Found first nonoccurence of black, grab mask
                    # grab neighborhood
                    mask = grab_neighborhood(mask_size, i, j, pixels)
                    break
        else:
            continue
        break

    average = mask_size*mask_size
    for i in range(mask_size):
        for j in range(mask_size):
            mask[i][j] = mask[i][j] / average

    for items in mask:
        print(items)

    # Correlation(mask, mask_size)

#grab neighborhood of pixels and create a new array of sizexsize
def grab_neighborhood(size, row, col, pixels): 
    # print(row, col)

    #Create new mask array of sizexsize
    newMask = np.empty((size, size))

    tempRow = row
    tempCol = col

    #iterate over a sizexsize array at current row and column
    for i in range(size): 
        for j in range(size): 
            print(tempRow, tempCol)
        

            # Left boundary
            # if (row < size)
            # Top boundary
            # if (col < size)
            # Right boundary
           
            # Bottom boundary

            
            # boundaryCol = height - currentcolumn;
            # boundaryRow = width - currentrow;
            # if(boundarycol < size)
            # for(row = 0; row < boundaryRow; row++)
            #     for(col = 0; < boundaryCol; row++)

                # boundaryRow = width - i
                # boundaryCol = height - j
                
                # if (boundaryRow < size):
                #     #if current row is 60/60 then set the mask size 
                #     size = boundaryRow
                # elif (boundaryCol < size):
                #     #if current col is 60/60 then set the mask size 
                #     size = boundaryCol
                
            
               



            # start at the current row and column
            newMask[i][j] = pixels[tempRow][tempCol]

            tempCol += 1
        tempRow += 1
        tempCol = col

   
    return newMask

# def grabMaskWPadding():

# def grabSummationedVal(mask, srcImgPixels, mask_size):
            
    
# def Correlation(mask, mask_size):
#     image = Image.open("./data_input/Image.pgm")
#     srcImgPixels = list(image.getdata())
#     width, height = image.size
#     srcImgPixels = [srcImgPixels[i * width: (i+1) * width] for i in range(height)]

#     newMask = np.empty((mask_size, mask_size))

#     for rows in range(height):
#         for cols in range(width):
#             newMask = grab_neighborhood(mask_size, rows, cols, srcImgPixels)

#             break
#         else:
#             continue
#         break

#     for items in newMask:
#         print(items)



grab_mask(3)