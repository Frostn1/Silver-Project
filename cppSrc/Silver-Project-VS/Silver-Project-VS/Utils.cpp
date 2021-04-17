#include "Utils.h"

bool is_space(char c) noexcept {
    switch (c) {
    case ' ':
    case '\t':
    case '\r':
    case '\n':
        return true;
    default:
        return false;
    }
}

bool is_digit(char c) noexcept {
    switch (c) {
    case '0':
    case '1':
    case '2':
    case '3':
    case '4':
    case '5':
    case '6':
    case '7':
    case '8':
    case '9':
        return true;
    default:
        return false;
    }
}

bool is_identifier_char(char c) noexcept {
    switch (c) {
    case 'a':
    case 'b':
    case 'c':
    case 'd':
    case 'e':
    case 'f':
    case 'g':
    case 'h':
    case 'i':
    case 'j':
    case 'k':
    case 'l':
    case 'm':
    case 'n':
    case 'o':
    case 'p':
    case 'q':
    case 'r':
    case 's':
    case 't':
    case 'u':
    case 'v':
    case 'w':
    case 'x':
    case 'y':
    case 'z':
    case 'A':
    case 'B':
    case 'C':
    case 'D':
    case 'E':
    case 'F':
    case 'G':
    case 'H':
    case 'I':
    case 'J':
    case 'K':
    case 'L':
    case 'M':
    case 'N':
    case 'O':
    case 'P':
    case 'Q':
    case 'R':
    case 'S':
    case 'T':
    case 'U':
    case 'V':
    case 'W':
    case 'X':
    case 'Y':
    case 'Z':
    case '0':
    case '1':
    case '2':
    case '3':
    case '4':
    case '5':
    case '6':
    case '7':
    case '8':
    case '9':
    case '_':
        return true;
    default:
        return false;
    }
}

void col(unsigned short color) {
    HANDLE hcon = GetStdHandle(STD_OUTPUT_HANDLE);
    SetConsoleTextAttribute(hcon, color);
}

void printHelp() {
    col(YELLOW);
    std::cout << "Usage";
    col(GRAY);
    std::cout << " : ";
    col(WHITE);
    std::cout << ".\\Silver.exe <options> [file]\n\n";
    col(GRAY);
    std::cout << "Options:\n-h --help for usage and help\n-l --lex only return the lexemes of the file\n";
    exit(0);
}

std::ostream& operator<<(std::ostream& os, const Token::Kind& kind) {
    static const char* const names[]{
        "Number",      "Identifier",  "LeftParen",  "RightParen", "LeftSquare",
        "RightSquare", "LeftCurly",   "RightCurly", "LessThan",   "GreaterThan",
        "Equal",       "Plus",        "Minus",      "Asterisk",   "Slash",
        "Hash",        "Dot",         "Comma",      "Colon",      "Semicolon",
        "SingleQuote", "DoubleQuote", "Comment",    "Pipe",       "End",
        "Unexpected",  "At",
    };
    return os << names[static_cast<int>(kind)];
}