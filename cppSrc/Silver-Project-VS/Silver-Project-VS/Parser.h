#pragma once
#include "Lexer.h"
#include "Token.h"
#include "ErrorHandle.h"
class Parser {
public:
	Parser(Lexer& lex) noexcept : m_lex{lex} {}
	void parse() noexcept;
	Token get() noexcept { return m_lex.next(); }
	void parseLink() noexcept;
private:
	Lexer& m_lex;
	Token current;

};

