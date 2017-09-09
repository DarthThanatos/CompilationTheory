import ply.yacc as yacc
from test import tokens

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''

    #p[0] = ('binary-expression',p[2],p[1],p[3])
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    #p[0] = ('group-expression',p[2])
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    #p[0] = ('number-expression',p[1])
    p[0] = int(p[1])

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

parser = yacc.yacc()
with open("input.txt", "r") as fh:
    result = parser.parse(fh.read())
    print result



