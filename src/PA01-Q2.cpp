#include <iostream>
#include <fstream>
#include <stdlib.h>
#include <string>
#include <cstring>
#include <sstream>
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

  std::stringstream ss;
  ss << quantNum;
  std::string s = ss.str();
   
    

    strcat(writefilePath, s.c_str());
    strcat(writefilePath, ".pgm");

    std::cout << writefilePath << std::endl;    
    writeImage(writefilePath, oldImage);

};
