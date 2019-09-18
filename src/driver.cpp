#include "../include/image.h"

int readImage(char[], ImageType&);

int main(int argc, char *argv[]) {
    int M, N, Q;

    char* filePath = "../data_input/peppers.pgm";

    ImageType image(N, M, Q);

    readImage(filePath, image);


    return 0;
}