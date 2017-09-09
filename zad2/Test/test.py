import ply.lex as lex
from ply.lex import TOKEN
import sys

literals="&"

reserved ={
	'if' : 'IF',
	'while' : 'WHILE'
}

tokens = [ 'PLUS','MINUS', 'TIMES',  'DIVIDE',  'LPAREN',  'RPAREN',  'NUMBER', 'ID', 'SPACE'] + list(reserved.values())

t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_ignore_SPACE  = r'\s+'

def t_NUMBER(t):
	r'\d+'
	t.value = int(t.value)
	return t

id = r'[a-zA-Z_][a-zA-Z_0-9]*'

@TOKEN(id)
def t_ID(t):
	t.type = reserved.get(t.value,'ID')
	return t

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

def t_error(t) :
	print "Illegal character '%s'" %t.value[0]
	t.lexer.skip(1)

"""
def t_eof(t):
	more = raw_input('Type more text:')
	if more:
		lexer.input(more)
		return lexer.token()
	return None
"""

lexer = lex.lex() #build the lexer
"""
with open("input.txt", "r") as fh:
	lexer.input( fh.read() )
	for token in lexer:
		print((token.type, token.value, token.lineno, token.lexpos))
"""