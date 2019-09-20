#include <iostream>
#include <fstream>
#include <stdlib.h>
#include "../include/image.h"

int readImageHeader(const char[], int&, int&, int&, bool&);
int readImage(const char[], ImageType&);
int writeImage(const char[], ImageType&);
void sampling(ImageType, ImageType&, const int);
constexpr int sizeHelper(const int);

int main(int argc, char *argv[]) {
    //int M, N, Q;

//     int i, j;
//     int M, N, Q;
//     bool type;
  bool type2;
//     int val;
//     int thresh;
  const char* filePath = "./data_input/peppers.pgm";
  const char *writefilePath = "./data_output/peppers_2sample.pgm";

  int Z, X, Y; // for image sampling
  const int FACTOR = 2; // Change this to make new size
  int size = 256/FACTOR;
  int L = size, O = size - 1, P = size;
  readImageHeader(filePath, Z, X, Y, type2);
  ImageType samplingImage(Z, X, Y);
  ImageType resizedImg(L, O, P);

  readImage(filePath, samplingImage);

  sampling(samplingImage, resizedImg, FACTOR);
  writeImage(writefilePath, resizedImg);

//     readImageHeader(filePath, N, M, Q, type);

//     ImageType image(N, M, Q);

//     readImage(filePath, image);

//     //std::cout << "Enter threshold: ";
//     //std::cin >> thresh;

//  // threshold image

//  for(i=0; i<N; i++)
//    for(j=0; j<M; j++) {
//      image.getPixelVal(i, j, val);
//      if(val < 50)
//        image.setPixelVal(i, j, 255);
//      else
//        image.setPixelVal(i, j, 0);
//     }

//  // write image
//  writeImage(writefilePath, image);

 return (1);


}

/**
 *  Details: Take in an integer defining how much to sample the
 *            image, e.g. 2. Run through the pixel values and store
 *            every 2nd pixel value into a new array which will be the
 *            pixel values of the new image, or every 4th pixel, or 8th.
 * */
void sampling(ImageType srcImg, ImageType& newImg, const int FACTOR) {
  // Variables
  int srcRows,
      srcCols,
      srcLvls;

  // New image variables
  int newImgCol;
  int value;

  // test
  int row, col, lvl;

  // initialization
  srcImg.getImageInfo(srcRows, srcCols, srcLvls);
  newImg.getImageInfo(row, col, lvl);

  cout << srcRows << " " << srcCols << " " << srcLvls << " \n";
  cout << row << " " << col << " " << lvl << " \n";

  // Run thru the image
  for (int srcImgRow = 0; srcImgRow <= srcRows; srcImgRow++) {
    if (srcImgRow == 128)
      break;
    newImgCol = 0;
    for (int srcImgCol = 0; srcImgCol <= srcCols; srcImgCol++) {
      if (srcImgCol % FACTOR == 0) {
        cout << srcImgRow << " " << newImgCol << " " << value << " \n";
        srcImg.getPixelVal(srcImgRow, srcImgCol, value);
        cout << srcImgRow << " " << newImgCol << " " << value << " \n";
        newImg.setPixelVal(srcImgRow, newImgCol, value);

        newImgCol++;
      }
    }
  }

}