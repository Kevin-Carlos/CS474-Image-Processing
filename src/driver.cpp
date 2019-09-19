#include <iostream>
#include <fstream>
#include <stdlib.h>
#include "../include/image.h"

int readImageHeader(const char[], int&, int&, int&, bool&);
int readImage(const char[], ImageType&);
int writeImage(const char[], ImageType&);

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
    
    //std::cout << "Enter threshold: ";
    //std::cin >> thresh;

 // threshold image 

 for(i=0; i<N; i++)
   for(j=0; j<M; j++) {
     image.getPixelVal(i, j, val);
     if(val < 50) 
       image.setPixelVal(i, j, 255);
     else
       image.setPixelVal(i, j, 0);
    }

   const char *writefilePath = "./data_input/peppers_test.pgm";

 // write image
 writeImage(writefilePath, image);

 return (1);


}
