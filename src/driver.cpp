#include <iostream>
#include <fstream>
#include <stdlib.h>
#include "../include/image.h"

int readImageHeader(const char[], int&, int&, int&, bool&);
int readImage(const char[], ImageType&);
void Quantize(int N, int M, int& val, int quantNum, ImageType oldImage);

int main(int argc, char *argv[]) {
    //int M, N, Q;

    int i, j;
    int M, N, Q;
    bool type;
    int val;
    int thresh;
    const char* filePath = "./data_input/peppers.pgm";

  readImageHeader(filePath, N, M, Q, type);

  ImageType image(N, M, Q);

  readImage(filePath, image);
    
  //const char *writefilePath;

  for(int k = 0; k < 4; k++)
  {
    switch(k)
    {
      case (0):
        Quantize(N, M, val, 128, image);
        break;
      case (1):
        Quantize(N, M, val, 32, image);
        break;
      case (2):
        Quantize(N, M, val, 8, image);
        break;
      case (3):
        Quantize(N, M, val, 2, image);
        break;   
    }
  }
 

 return (1);


}
