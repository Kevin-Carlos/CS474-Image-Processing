#include "../include/image.h"

int readImageHeader(const char[], int&, int&, int&, bool&);
int readImage(const char[], ImageType&);
int writeImage(char[], ImageType&);

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


    return 0;
}
