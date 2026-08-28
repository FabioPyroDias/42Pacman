from parser.parser import parser_configuration_file
import sys
from enums import Direction


if __name__ == "__main__":
    parser_configuration_file(sys.argv[1])
    print(Direction.EAST.value - Direction.NORTH.value)
