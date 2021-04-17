#pragma once
#include <iostream>
#include <string>



class Token {
public:
    enum class Kind {
        Number,
        Identifier,
        LeftParen,
        RightParen,
        LeftSquare,
        RightSquare,
        LeftCurly,
        RightCurly,
        LessThan,
        GreaterThan,
        Equal,
        Plus,
        Minus,
        Asterisk,
        Slash,
        Hash,
        Dot,
        Comma,
        Colon,
        Semicolon,
        SingleQuote,
        DoubleQuote,
        Comment,
        Pipe,
        End,
        Unexpected,
        At,
        
    };
    Token(Kind kind) noexcept : m_kind{ kind } {}

    Token(Kind kind, const char* beg, std::size_t len) noexcept
        : m_kind{ kind }, m_lexeme(beg, len) {}

    Token(Kind kind, const char* beg, const char* end) noexcept
        : m_kind{ kind }, m_lexeme(beg, std::distance(beg, end)) {}

    Kind kind() const noexcept { return m_kind; }

    void kind(Kind kind) noexcept { m_kind = kind; }

    bool is(Kind kind) const noexcept { return m_kind == kind; }

    bool is_not(Kind kind) const noexcept { return m_kind != kind; }

    bool is_one_of(Kind k1, Kind k2) const noexcept { return is(k1) || is(k2); }

    template <typename... Ts>
    bool is_one_of(Kind k1, Kind k2, Ts... ks) const noexcept {
        return is(k1) || is_one_of(k2, ks...);
    }

    std::string_view lexeme() const noexcept { return m_lexeme; }

    void lexeme(std::string_view lexeme) noexcept {
        m_lexeme = std::move(lexeme);
    }

private:
    Kind             m_kind{};
    std::string_view m_lexeme{};
};