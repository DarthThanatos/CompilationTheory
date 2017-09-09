#!/usr/bin/python
from ply.lex import LexToken

from scanner import Scanner
from AST import *



class Cparser(object):


    def __init__(self):
        self.error_occured = False
        self.scanner = Scanner()
        self.scanner.build()

    tokens = Scanner.tokens


    precedence = (
       ("nonassoc", 'IFX'),
       ("nonassoc", 'ELSE'),
       ("right", '='),
       ("left", 'OR'),
       ("left", 'AND'),
       ("left", '|'),
       ("left", '^'),
       ("left", '&'),
       ("nonassoc", '<', '>', 'EQ', 'NEQ', 'LE', 'GE'),
       ("left", 'SHL', 'SHR'),
       ("left", '+', '-'),
       ("left", '*', '/', '%'),
    )


    def p_error(self, p):
        if p:
            print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, self.scanner.find_tok_column(p), p.type, p.value))
        else:
            print("Unexpected end of input")

    
    
    def p_program(self, p):
        """program : main_parts_interlacing"""
        #p[0] = ('program',p[1],p[2],p[3])
        p[0] = Program(p[1])

    def p_main_parts_interlacing(self, p):
        """main_parts_interlacing : main_parts_interlacing main_part
                                   | main_part
        """
        if p.__len__() == 3:
            p[0] = MainPartsInerlacing(p[1],p[2])
        else:
            p[0] = MainPartsInerlacing(None,p[1])

    def p_main_part(self, p):
        """
        main_part : declaration
                  | fundef
                  | instruction
        """
        p[0] = p[1]

    def p_declarations(self, p):
        """declarations : declarations declaration
                        | """
        #p[0] = ('') if p.__len__() == 1 else ('decl',p[1], p[2])
        p[0] = None if p.__len__() == 1 else Declarations(p[1], p[2])

    def p_declaration(self, p):
        """declaration : TYPE inits ';' 
                       | error ';' """
        #p[0] = ('declaration',p[1], p[2]) if p.__len__() == 4 else ('declaration-error',p[1])
        #p[0] = Declaration(p[1], p[2])
        if not type(p[1]) == LexToken: p[0] = Declaration(p[1], p[2])
        else: self.error_occured = True

    def p_inits(self, p):
        """inits : inits ',' init
                 | init """
        #p[0] = ('inits',p[1],p[3]) if p.__len__() == 4 \
        #    else ('init',p[1])
        p[0] = Inits(p[1],p[3]) if p.__len__() == 4 \
            else p[1]

    def p_init(self, p):
        """init : ID '=' expression """
        #p[0] = ('init','=',p[1],p[3])
        p[0] = Init(p[1],p[3])

    def p_instructions_opt(self, p):
        """instructions_opt : instructions
                            | """
        #p[0] = ('instructions_opt',p[1]) if p.__len__()==2 else('empty_instr')
        p[0] = InstructionsOpt(p[1]) if p.__len__()==2 else None
    
    def p_instructions(self, p):
        """instructions : instructions instruction
                        | instruction """
        #p[0] = ('instructions',p[1],p[2]) if p.__len__()==3 else ('instruction', p[1])
        p[0] = Instructions(p[1],p[2]) if p.__len__()==3 else p[1]
    
    def p_instruction(self, p):
        """instruction : print_instr
                       | labeled_instr
                       | assignment
                       | choice_instr
                       | while_instr 
                       | repeat_instr 
                       | return_instr
                       | break_instr
                       | continue_instr
                       | compound_instr
                       | expression ';' """
        #p[0] = ('instruction-node',p[1])
        p[0] = p[1]
    
    def p_print_instr(self, p):
        """print_instr : PRINT expr_list ';'
                       | PRINT error ';' """
        #p[0] = ('print_instr', p[1], p[2])
        if not type(p[2]) == LexToken: p[0] = PrintInstr(p[2])
        else: self.error_occured = True
    
    def p_labeled_instr(self, p):
        """labeled_instr : ID ':' instruction """
        #p[0] = ('labeled_instr', p[1], p[3])
        p[0] = LabeledInstr(p[1], p[3])
    
    def p_assignment(self, p):
        """assignment : ID '=' expression ';' """
        #p[0] = ('assignment',p[1],p[3])
        p[0] = Assignment(p[1],p[3])
    
    def p_choice_instr(self, p):
        """choice_instr : IF '(' condition ')' instruction  %prec IFX
                        | IF '(' condition ')' instruction ELSE instruction
                        | IF '(' error ')' instruction  %prec IFX
                        | IF '(' error ')' instruction ELSE instruction """
        #p[0] = ('if-cond-instr',p[3],p[5])if p.__len__() == 6 else ('if-cond-instr-else-instr',p[3],p[5],p[7])
        if not type(p[3]) == LexToken :p[0] = ChoiceInstr(p[3],p[5])if p.__len__() == 6 else ChoiceInstr(p[3],p[5],p[7])
        else: self.error_occured = True
    
    def p_while_instr(self, p):
        """while_instr : WHILE '(' condition ')' instruction
                       | WHILE '(' error ')' instruction """
        #p[0] = ('while-instr',p[3],p[5])
        if not type(p[3]) == LexToken: p[0] = WhileInstr(p[3],p[5])
        else: self.error_occured = True

    def p_repeat_instr(self, p):
        """repeat_instr : REPEAT instructions UNTIL condition ';' """
        #p[0] = ('repeat',p[2],p[4])
        p[0] = RepeatInstr(p[2],p[4])
    
    def p_return_instr(self, p):
        """return_instr : RETURN expression ';' """
        #p[0] = ('return',p[2])
        p[0] = ReturnInstr(p[2])
    
    def p_continue_instr(self, p):
        """continue_instr : CONTINUE ';' """
        #p[0] = ('continue')
        p[0] = ContinueInstr()
    
    def p_break_instr(self, p):
        """break_instr : BREAK ';' """
        #p[0] = ('break')
        p[0] = BreakInstr()
    
    
    def p_compound_instr(self, p):
        """compound_instr : '{' declarations instructions_opt '}' """
        #p[0] = ('compound_instr',p[2],p[3])
        p[0] = CompoundInstr(p[2],p[3])

    def p_condition(self, p):
        """condition : expression"""
        #p[0] = ('condition',p[1])
        p[0] = Condition(p[1])

    def p_const(self, p):
        """const : INTEGER
                 | FLOAT
                 | STRING"""
        #p[0] = p[1]
        p[0] = Const(p[1]) #to-do!!
    
    
    def p_expression(self, p):
        """expression : const
                      | ID
                      | expression '+' expression
                      | expression '-' expression
                      | expression '*' expression
                      | expression '/' expression
                      | expression '%' expression
                      | expression '|' expression
                      | expression '&' expression
                      | expression '^' expression
                      | expression AND expression
                      | expression OR expression
                      | expression SHL expression
                      | expression SHR expression
                      | expression EQ expression
                      | expression NEQ expression
                      | expression '>' expression
                      | expression '<' expression
                      | expression LE expression
                      | expression GE expression
                      | '(' expression ')'
                      | '(' error ')'
                      | ID '(' expr_list_or_empty ')'
                      | ID '(' error ')' """
        #p[0] = (p[1]) if p.__len__() == 2 else \
        #    (p[2],p[1],p[3]) if p.__len__() == 4  and p[1]!='(' else \
        #        p[2] if p.__len__() == 4 and p[1]=='(' else (p[1],p[3])
        """
        p[0] = p[1] if p.__len__() == 2 else \
            BinExpr(p[2],p[1],p[3]) if p.__len__() == 4  and p[1]!='(' else \
                p[2] if p.__len__() == 4 and p[1]=='(' else DeclaredFunc(p[1],p[3])
        """
        if p.__len__() == 2 :
            p[0] = p[1]
        elif p.__len__() == 4:
            if p[1] !='(':
                p[0] = BinExpr(p[2],p[1],p[3])
            else:
                if not type(p[2]) == LexToken: p[0] = p[2]
                else: self.error_occured = True
        else:
            if not type(p[3]) == LexToken: p[0] = DeclaredFunc(p[1],p[3])
            else: self.error_occured = True

    def p_expr_list_or_empty(self, p):
        """expr_list_or_empty : expr_list
                              | """
        #p[0] = ('expr_list',p[1]) if p.__len__()==2 else ('empty_exprlist')
        p[0] = PExprListOrEmpty(p[1]) if p.__len__()==2 else None
    
    def p_expr_list(self, p):
        """expr_list : expr_list ',' expression
                     | expression """
        #p[0] = ('expr_list',p[1],p[3]) if p.__len__() == 4 else ('expr',p[1])
        p[0] = PExprList(p[1],p[3]) if p.__len__() == 4 else p[1]
    
    def p_fundefs_opt(self, p):
        """fundefs_opt : fundefs
                       | """
        #p[0] = ('fundefs_opt',p[1]) if p.__len__() == 2 else ('no fundefs')
        p[0] = FuncDefsOpt(p[1]) if p.__len__() == 2 else None

    def p_fundefs(self, p):
        """fundefs : fundefs fundef
                   | fundef """
        #p[0] = ('fundefs',p[1],p[2]) if p.__len__() == 3 else ("fundef", p[1])
        p[0] = FuncDefs(p[1],p[2]) if p.__len__() == 3 else  p[1]
          
    def p_fundef(self, p):
        """fundef : TYPE ID '(' args_list_or_empty ')' compound_instr """
        #p[0] = ('fundef',p[2],p[1],p[4],p[6])
        p[0] = FuncDef(p[1],p[2],p[4],p[6])

    
    def p_args_list_or_empty(self, p):
        """args_list_or_empty : args_list
                              | """
        #p[0] = ('args_list_',p[1]) if p.__len__() == 2 else ("empty-args-list")
        p[0] = p[1] if p.__len__() == 2 else None
    
    def p_args_list(self, p):
        """args_list : args_list ',' arg 
                     | arg """
        #p[0] = ('args_list',p[1],p[3]) if p.__len__() == 4 else ('arg', p[1])
        p[0] = ArgsList(p[1],p[3]) if p.__len__() == 4 else p[1]

    def p_arg(self, p):
        """arg : TYPE ID """
        #p[0] = ('arg',p[1],p[2])
        p[0] = Arg(p[1],p[2])