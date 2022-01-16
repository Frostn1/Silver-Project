import argparse
from src.tools.colors import *
from src.tools.argparser import *

SILVER_VERSION = '1.0.0'


def main():
    parser = argparse.ArgumentParser(prog='py -m src.test.test')
    parser.add_argument('--test',help='Run test on folders and/or .si files' , nargs='+', action=Test)
    parser.add_argument('--version', action='version', version=f'Silver-Test v{SILVER_VERSION}')
    args = parser.parse_args()
    
if __name__ == "__main__":
    main()