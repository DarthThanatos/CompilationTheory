import ply.yacc as yacc

from test import tokens

precedence = (

    ('left', "PLUS", "MINUS"),
    ('left', "TIMES", "DIVIDE"),
    ('right', "UMINUS"),
)

def p_expression_plus(p):
    '''expression : expression PLUS term
                  | expression MINUS term'''
    """
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    """
    p[0] = ('binary-exp', p[2],p[1],p[3])

def p_expression_term(p):
    'expression : term'
    p[0] = ('expr-to-term',p[1])
    #p[0] = p[1]

def p_term_times(p):
    'term : term TIMES factor'
    p[0] = ('binary-term','*',p[1],p[3])
    #p[0] = p[1] * p[3]

def p_term_div(p):
    'term : term DIVIDE factor'
    p[0] = ('binary-term','/',p[1],p[3])
    #p[0] = p[1] / p[3]

def p_term_factor(p):
    'term : factor'
    p[0] = ('term - to - factor', p[1])
    #p[0] = p[1]

def p_factor_num(p):
    'factor : NUMBER'
    p[0] = ('factor - to - num', p[1])
    #p[0] = p[1]

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    #p[0] = p[2]
    p[0] = ('group expr', p[2])

def p_expr_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = ('uminus expr', p[2])
    #p[0] = -p[2]

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

parser = yacc.yacc()
with open("input.txt", "r") as fh:
    result = parser.parse(fh.read())
    print result
"""
while True:
    try:
        s = raw_input('calc> ')
    except EOFError:
        break
    if not s: continue
    result = parser.parse(s)
    print(result)
"""


