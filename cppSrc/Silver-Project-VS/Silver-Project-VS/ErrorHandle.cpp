#include "ErrorHandle.h"
void throwError(std::string message) {
    col(RED);
    std::cout << "error";
    col(GRAY);
    std::cout << " : ";
    col(WHITE);
    std::cout << message << std::endl;
    col(GRAY);
    exit(0);
}