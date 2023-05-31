import argparse

from lang_config import name


def parse_args() -> str:
    arg_parser = argparse.ArgumentParser(description=f'Argument parser for {name.LANGUAGE}')
    arg_parser.add_argument('File', help='File to compile', metavar='File', type=str, nargs=1)
    arguments = arg_parser.parse_args()
    return arguments.File[0]


def read_file(file_path: str) -> str:
    content: str
    with open(file_path, 'r') as file:
        content = file.read()
    return content
