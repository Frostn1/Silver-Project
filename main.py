from lib.compiler.error_handlers.exceptions import SilverException
from lib.compiler.lexer.lexer import lex
from lib.compiler.parser.syntax_parser import parse
from lib.file_handler import parse_args, read_file


def main() -> None:
    file_path: str = parse_args()
    file_content: str = read_file(file_path)
    tokens = lex(file_content)
    try:
        parse_tree = parse(tokens)
    except SilverException as e:
        print(e)

if __name__ == '__main__':
    main()
