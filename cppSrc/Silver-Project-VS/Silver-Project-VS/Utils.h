#pragma once
#include <Windows.h>
#include <iostream>
bool is_identifier_char(char c) noexcept;
bool is_digit(char c) noexcept;
bool is_space(char c) noexcept;
enum colour { 
	DARKBLUE = 1, 
	DARKGREEN, 
	DARKTEAL, 
	DARKRED, 
	DARKPINK, 
	DARKYELLOW, 
	GRAY, 
	DARKGRAY, 
	BLUE, 
	GREEN, 
	TEAL, 
	RED, 
	PINK, 
	YELLOW, 
	WHITE 
};

void col(unsigned short color);
void printHelp();