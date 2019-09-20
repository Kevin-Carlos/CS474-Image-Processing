#include <iostream>
#include <fstream>
#include <stdlib.h>
#include <string.h>
#include "../include/image.h"

int writeImage(const char[], ImageType&);


void Quantize(int N, int M, int& val, int quantNum, ImageType oldImage) 
{

  char writefilePath[50] = "./data_output/peppers";
  quantNum = 256/quantNum;
  std::cout << quantNum << endl;
  
  for(int i=0; i<N; i++)
    for(int j=0; j<M; j++) 
    {
      oldImage.getPixelVal(i, j, val);
      val /= quantNum; 
      oldImage.setPixelVal(i, j, val);
    }


    char quantumNumber[5] = {(char)quantNum};
    strcat(writefilePath, quantumNumber);
    strcat(writefilePath, ".pgm");
    writeImage(writefilePath, oldImage);

};
