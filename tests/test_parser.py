from parser.parser import parser_configuration_file
import sys


if __name__ == "__main__":
    configs = parser_configuration_file(sys.argv[1])
