#include <iostream>
#include <fstream>
#include <stdlib.h>
#include <string>
#include <cstring>
#include <sstream>
#include "../include/image.h"


int readImageHeader(const char[], int&, int&, int&, bool&);
int readImage(const char[], ImageType&);
void Quantize(int N, int M, int& val, int quantNum, ImageType oldImage, char writePath[]);
int writeImage(const char[], ImageType&);

//Will output the Quantized image of lena and peppers
void Quantize(int N, int M, int& val, int quantNum, ImageType oldImage, char writePath[]) 
{
  //QuantNum is the number/ratio to scale the rest of the pixels to and also output the corresponding one.
 
  char temporary[50] = ""; 
  
  oldImage.setImageInfo(N, M, quantNum); //Update the image so the quantum level matches Q
  std::stringstream ss;
  ss << quantNum; //copy the quantNum as a string from int
  
  strcpy(temporary, writePath); //take the file to write to and copy it into temporary
  quantNum = 256/quantNum; //will set the quantNum = #pixels/ratio
                           //example: for the first question i) 128, it will be 256/128 = 2           
                           
  

  for(int i=0; i<N; i++)
    for(int j=0; j<M; j++) 
    {
      oldImage.getPixelVal(i, j, val);
      val /= quantNum;                  //pixel range is now between 128 - 0.
      oldImage.setPixelVal(i, j, val);
    }

  
  std::string s = ss.str();
  strcat(temporary, s.c_str());
  strcat(temporary, "_Quantized.pgm");
  
  writeImage(temporary, oldImage);

};

void Question2()
{
  int N, M, Q; //pepper values
  int Y, X, Z; //lenna values
  bool type;
  int pval; //pepper
  int lval; //lenna

  const char* PepperfilePath = "./data_input/peppers.pgm";
  const char* LennafilePath = "./data_input/lenna_1.pgm";

  readImageHeader(PepperfilePath, N, M, Q, type); //
  readImageHeader(LennafilePath, Y, X, Z, type); //

  ImageType Pepperimage(N, M, Q);
  ImageType Lennaimage(Y, X, Z);

  readImage(PepperfilePath, Pepperimage);
  readImage(LennafilePath, Lennaimage);
    
  char writePepperPath[50] = "./data_output/peppers";
  char writeLennaPath[50] = "./data_output/lenna";
 


  //Will write out the 128, 32, 8, and 2 Quantizations for lenna_1.pgm and pepper.pgm
  for(int k = 0; k < 4; k++)
  {
    switch(k)
    {
      case (0):
        Quantize(N, M, pval, 128, Pepperimage, writePepperPath);
        Quantize(Y, X, lval, 128, Lennaimage, writeLennaPath);
        break;
      case (1):
        Quantize(N, M, pval, 32, Pepperimage, writePepperPath); 
        Quantize(Y, X, lval, 32, Lennaimage, writeLennaPath);
        break;
      case (2):
        Quantize(N, M, pval, 8, Pepperimage, writePepperPath);
        Quantize(Y, X, lval, 8, Lennaimage, writeLennaPath);
        break;
      case (3):
        Quantize(N, M, pval, 2, Pepperimage, writePepperPath);
        Quantize(Y, X, lval, 2, Lennaimage, writeLennaPath);
        break;   
    }
  }
 


}
