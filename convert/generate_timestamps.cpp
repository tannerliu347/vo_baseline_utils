// Author: Tianyi Liu
// Extract timestamps from a TUM style trajectory file
// To compile:
// g++ -o generate_timestamps generate_timestamps.cpp

#include <iostream>
#include <fstream>
#include <string>

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cout << "Usage: ./generate_timestamps [trajectory_file] [output_file]" << std::endl;
        return 1;
    }
    std::ifstream inFile;
    inFile.open(argv[1]);
    if (!inFile.is_open()) {
        std::cerr << "Unable to open trajectory_file" << std::endl;
        return 1;
    }
    std::ofstream outFile;
    outFile.open(argv[2]);
    if (!outFile.is_open()) {
        std::cerr << "Unable to open output_file" << std::endl;
        return 1;
    }
    double timestamp;
    double tmp;
    outFile.precision(16);
    while (!inFile.eof()) {
        inFile >> timestamp;
        for (int i = 0; i < 7; i++) // only need the timestamps
            inFile >> tmp;
        outFile << timestamp << std::endl;
    }
    inFile.close();
    outFile.close();
    return 0;
}