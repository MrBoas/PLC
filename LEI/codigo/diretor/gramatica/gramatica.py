import sys
from antlr4 import *
from gramaticaLexer import gramaticaLexer
from gramaticaParser import gramaticaParser

def main(argv):
    input = FileStream(argv[1])
    lexer = gramaticaLexer(input)
    stream = CommonTokenStream(lexer)
    parser = gramaticaParser(stream)
    tree = parser.dsl()
    # print(lexer)
    # print(stream)
    # print(parser)
    # print(tree)

main(sys.argv)