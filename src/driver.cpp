#include "ReadImage.cpp"

int main() {

    int M, N, Q;

    ImageType image(N, M, Q);

    if (readImage("../data_input/peppers.pgm", image)) {
        cout << "Success.\n";
    }

    return 0;
}