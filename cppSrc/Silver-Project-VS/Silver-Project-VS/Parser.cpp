#include "Parser.h"

void Parser::parse() noexcept {
	
	while (not (current = get()).is_one_of(Token::Kind::End, Token::Kind::Unexpected)) {
		switch (current.kind()) {
		case Token::Kind::LeftParen :
			current = get();
			if(current.kind() == Token::Kind::Identifier && current.lexeme() == "link") parseLink();

		}
	}
}


void Parser::parseLink() noexcept {
	current = get();
	if (current.kind() != Token::Kind::Colon) throwError("missing .:. at link");
	current = get();
	if (current.kind() != Token::Kind::SingleQuote && current.kind() != Token::Kind::DoubleQuote) throwError("missing single quote | double quote");
	Token::Kind STARTER = current.kind();
	current = get();
	if (current.kind() != Token::Kind::Identifier) throwError("missing an identifier");
	std::string file = std::string(current.lexeme());
	current = get();
	if (current.kind() != Token::Kind::Dot) throwError("missing a dot in link");
	current = get();
	if (current.kind() != Token::Kind::Identifier && current.lexeme() != "pi") throwError("missing an identifier");
	current = get();
	if (current.kind() != STARTER) throwError("quote doesn't match");
	std::cout << "link:\n\tfile=" + file + ".pi\n";

}
