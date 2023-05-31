from lib.compiler.lexer.lexer import lex
from lib.file_handler import parse_args, read_file


def main() -> None:
    file_path: str = parse_args()
    file_content: str = read_file(file_path)
    tokens = lex(file_content)

if __name__ == '__main__':
    main()
