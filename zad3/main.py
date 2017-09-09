import os
import sys
import ply.yacc as yacc
from Cparser import Cparser
from TreePrinter import TreePrinter
from TypeChecker import TypeChecker


if __name__ == '__main__':
	filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
	with open(filename, "r+") as file:
		try:
			_Cparser = Cparser()
			parser = yacc.yacc(module=_Cparser)
			text = file.read()
			ast = parser.parse(text, lexer=_Cparser.scanner)
			typeChecker = TypeChecker()
			if ast: typeChecker.visit(ast)
		except IOError:
			print("Cannot open {0} file".format(filename))
			sys.exit(0)