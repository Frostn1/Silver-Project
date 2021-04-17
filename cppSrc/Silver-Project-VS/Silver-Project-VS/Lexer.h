#pragma once
#include "Token.h"
#include "Utils.h"
class Lexer {
public:
    Lexer(const char* beg) noexcept : m_beg{ beg } {}

    Token next() noexcept;
    
private:
    Token identifier() noexcept;
    Token number() noexcept;
    Token slash_or_comment() noexcept;
    Token atom(Token::Kind) noexcept;

    char peek() const noexcept { return *m_beg; }
    char get() noexcept { return *m_beg++; }

    const char* m_beg = nullptr;
};

