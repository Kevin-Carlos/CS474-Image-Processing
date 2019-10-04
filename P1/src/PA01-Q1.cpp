#include <iostream>
#include <fstream>
#include <stdlib.h>
#include "../include/image.h"

int readImageHeader(const char[], int&, int&, int&, bool&);
int readImage(const char[], ImageType&);
int writeImage(const char[], ImageType&);
void sampling(ImageType, ImageType&, const int);
void resizeTo256(ImageType, const int);

void Question1() {
  bool type2;
  const char* filePath = "./data_input/lenna_1.pgm"; // Change depending on input picture
  const char *writefilePath = "./data_output/lenna_8sample.pgm"; // Change this to match FACTOR

  int Z, X, Y; // for image sampling
  const int FACTOR = 8; // Change this to make new size

  readImageHeader(filePath, Z, X, Y, type2);
  ImageType samplingImage(Z, X, Y);
  samplingImage.getImageInfo(Z, X, Y);

  // Debugging
  // cout << "Row: " << Z << " Col: " << X << "\n";

  // Lenna
  int   L = Z / FACTOR,
        O = X / FACTOR,
        P = Y;

  // Because peppers is a 255 x 254 and need to jank it to work
  // int   L = ( (Z + 1) / FACTOR ) + .5,
  //       O = ( (X + 1) / FACTOR ),
  //       P = Y;

  ImageType resizedImg(L, O, P);

  readImage(filePath, samplingImage);

  sampling(samplingImage, resizedImg, FACTOR);
  resizeTo256(resizedImg, FACTOR);

  writeImage(writefilePath, resizedImg);
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
  int value;
  int actualRow = 0,
      actualCol = 0;

  //Initialization
  srcImg.getImageInfo(srcRows, srcCols, srcLvls);

  cout << " " << srcRows << " " << srcCols << "\n";

  for (int cols = 0; cols < srcCols; cols += FACTOR) {
    actualRow = 0;
    for (int rows = 0; rows < srcRows; rows += FACTOR) {
        srcImg.getPixelVal(rows, cols, value);

        // Debugging
        // cout << "ActRow: " << actualRow << " ActCol: " << actualCol << " Val: " << value << "\n";

        newImg.setPixelVal(actualRow, actualCol, value);

      actualRow++;
    }

    actualCol++;
  }
}

void resizeTo256(ImageType srcImg, const int FACTOR) {
  //Variables
  const char* resized256Path = "./data_output/lenna_8_256sample.pgm";

  int srcRow,
      srcCol,
      srcLvl;

  // Lenna
  int N = 256,
      M = 256,
      Q = 255;

  // Peppers
  // int N = 255,
  //     M = 254,
  //     Q = 255;

  int actualRow = 0, actualCol = 0;
  int value;

  // Initialization
  ImageType resizedImg(N, M, Q);
  srcImg.getImageInfo(srcRow, srcCol, srcLvl);

  for (int row = 0; row < srcRow; row++) {
    actualCol = 0;
    for (int col = 0; col < srcCol; col++) {
      srcImg.getPixelVal(row, col, value);
      for (int index = 1; index < FACTOR; index++) {
        resizedImg.setPixelVal(actualRow, actualCol, value);

        // Need to do boundary checking on these portions

        // Lenna
        if (actualRow + index < N - FACTOR && actualCol + index < M - FACTOR) {
          resizedImg.setPixelVal(actualRow + index, actualCol, value);
          resizedImg.setPixelVal(actualRow, actualCol + index, value);
          resizedImg.setPixelVal(actualRow + index, actualCol + index, value);
        }

        // Peppers
        // if (actualRow + index < N - FACTOR + 1 && actualCol + index < M - FACTOR + 1) {
        //   resizedImg.setPixelVal(actualRow + index, actualCol, value);
        //   resizedImg.setPixelVal(actualRow, actualCol + index, value);
        //   resizedImg.setPixelVal(actualRow + index, actualCol + index, value);
        // }
        cout << "Row: " << actualRow << " Col: " << actualCol << " \n";
      }
      actualCol += FACTOR;
    }
    actualRow += FACTOR;
  }

  writeImage(resized256Path, resizedImg);
}