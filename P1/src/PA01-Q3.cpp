#include <iostream>
#include <fstream>
#include <stdlib.h>
#include <math.h>
#include "../include/image.h"

int readImageHeader(const char[], int&, int&, int&, bool&);
int readImage(const char[], ImageType&);
int writeImage(const char[], ImageType&);
void initArray(int*);
void createHistogram(ImageType, int*);
void equalizeHistogram(ImageType, int *);

void Question3() {
    // Variables
    int N, M, Q;
    bool type;
    const int SIZE = 256;

    int histogramArray[SIZE]; // Array for histogram

    const char* boatFilePath = "./data_input/f_16.pgm"; //Change end to change image

    // Initialization
    readImageHeader(boatFilePath, N, M, Q, type);
    ImageType boatImage(N, M, Q);
    readImage(boatFilePath, boatImage);

    initArray(histogramArray);
    createHistogram(boatImage, histogramArray);

    equalizeHistogram(boatImage, histogramArray);

}

// Initializes number of occurences to 0
void initArray(int* histogram) {
    for (int index = 0; index < 256; index++) {
        histogram[index] = 0;
    }
}

void createHistogram(ImageType srcImage, int* histogram) {
    // Variables
    int N,
        M,
        Q,
        value;

    // Initialization
    srcImage.getImageInfo(N, M, Q);

    for (int row = 0; row < N; row++) {
        for (int col = 0; col < M; col++) {
            srcImage.getPixelVal(row, col, value);
            histogram[value] += 1;
        }
    }

    // Debug
    // for (int index = 0; index < 256; index++) {
    //     cout << histogram[index] << "\n";
    // }
}

void equalizeHistogram(ImageType srcImage, int* histogram) {
    // Variables
    const char* outputPath = "./data_output/equalized_f_16.pgm"; //Change for correct output name

    int N,
        M,
        Q;

    const int SIZE = 256;
    int equalizedArray[SIZE];
    int numOperatedOn = 0;
    int totalNumPixels;
    float equalizedValue = 0.0f;

    // Get image information
    srcImage.getImageInfo(N, M, Q);

    totalNumPixels = N * M;

    // Equalize and map values to equalizedArray
    for (int index = 0; index < SIZE; index++) {
        numOperatedOn += histogram[index];

        equalizedValue = (float)numOperatedOn / (float)totalNumPixels;
        equalizedValue *= Q;
        equalizedValue = round(equalizedValue);

        // Map values
        equalizedArray[index] = equalizedValue;
    }

    // Create the equalized image
    int L = N,
        O = M,
        P = Q;
    int srcValue,
        newValue;

    // Initalize
    ImageType equalizedImage(L, O, P);

    for (int row = 0; row < N; row++) {
        for (int col = 0; col < M; col++) {
            srcImage.getPixelVal(row, col, srcValue);

            // Look at that value/index
            newValue = equalizedArray[srcValue];

            // Store in new image
            equalizedImage.setPixelVal(row, col, newValue);
        }
    }

    writeImage(outputPath, equalizedImage);

}