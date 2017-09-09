
class Node(object):

    def __init__(self):
        self.children = ()

    def __str__(self):
        #return self.printTree()
        return ''

    def accept(self, visitor):
        return visitor.visit(self)


class Program(Node):
    def __init__(self, main_parts_interlacing ):
        """
        self.declarations = declarations
        self.fundefopt = fundefopt
        self.instr_opt = instr_opt
        """
        self.main_parts_interlacing = main_parts_interlacing
        self.children = [main_parts_interlacing]


class MainPartsInerlacing(Node):
    def __init__(self, main_parts, main_part ):
        self.main_parts = main_parts
        self.main_part = main_part
        self.children = [main_parts, main_part]


class MainPart(Node):
    def __init__(self, main_part ):
        self.main_part = main_part
        self.children = [main_part]

class Declarations(Node):
    def __init__(self, declarations=None, declaration=None):
        self.declarations = declarations
        self.declaration = declaration
        self.children = [declarations,declaration]

class Declaration(Node):
    def __init__(self, type, inits):
        self.type = type
        self.inits = inits
        self.children = [type,inits]

class Inits(Node):
    def __init__(self, init, inits=None ):
        self.inits = inits
        self. init = init
        self.children = [inits,init]

class Init(Node):
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr
        self.children = [id,expr]


class FuncDefsOpt(Node):
    def __init__(self, fundefs=None):
        self.fundefs = fundefs
        self.children = [fundefs]

class FuncDefs(Node):
    def __init__(self, fundef,fundefs=None):
        self.fundefs = fundefs
        self.fundef = fundef
        self.children = [fundefs,fundef]

class FuncDef(Node):
    def __init__(self, type, id, args_list_or_empty, compound_instr):
        self.type = type
        self.id = id
        self.args_list_or_empty = args_list_or_empty
        self.compound_instr = compound_instr
        self.children = [type,id,args_list_or_empty,compound_instr]

class DeclaredFunc(Node):
    def __init__(self,id,expr_list_or_empty):
        self.id = id
        self.expr_list_or_empty = expr_list_or_empty
        self.children = [id,expr_list_or_empty]

class ArgsListOrEmpty(Node):
    def __init__(self, argsList=None):
        self.argsList= argsList
        self.children = [argsList]

class ArgsList(Node):
    def __init__(self, arg, args_list = None):
        self.args_list= args_list
        self.arg = arg
        self.children = [args_list,arg]

class Arg(Node):
    def __init__(self, type,id):
        self.type = type
        self.id = id
        self.children = [type,id]

class InstructionsOpt(Node):
    def __init__(self, instructions = None):
        self.instructions = instructions
        self.children = [instructions]

class Instructions(Node):
    def __init__(self, instructions, instruction):
        self.instructions = instructions
        self.instruction = instruction
        self.children = [instructions,instruction]

class Instruction(Node):
    def __init__(self,expr):
        self.expr = expr
        self.children = [expr]

class PrintInstr(Instruction):
    def __init__(self, expr_list):
        self.expr_list = expr_list
        self.children = [expr_list]

class LabeledInstr(Instruction):
    def __init__(self,id,instruction):
        self.id = id
        self.instruction = instruction
        self.children = [id,instruction]

class Assignment(Instruction):
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr
        self.children = [id,expr]

class ChoiceInstr(Instruction):
    def __init__(self, if_cond, if_instr, else_instr = None):
        self.if_cond = if_cond
        self.if_instr = if_instr
        self.else_instr = else_instr
        self.children = [if_cond,if_instr,else_instr]

class WhileInstr(Instruction):
    def __init__(self, cond, instr):
        self.cond = cond
        self.instr = instr
        self.children = [cond,instr]

class RepeatInstr(Instruction):
    def __init__(self, instr, condition):
        self.instr = instr
        self.condition = condition
        self.children = [instr,condition]

class ReturnInstr(Instruction):
    def __init__(self, expr, line = 0, column = 0):
        self.expr = expr
        self.children = [expr]
        self.lineno = line
        self.column = column

class BreakInstr(Instruction):
    def __init__(self, line = 0, column = 0):
        self.children = None
        self.lineno = line
        self.column = column

class ContinueInstr(Instruction):
    def __init__(self, line, column):
        self.children = None
        self.lineno = line
        self.column = column

class CompoundInstr(Instruction):
    def __init__(self, declarations, instructionsOpt):
        self.declarations = declarations
        self.instructionsOpt = instructionsOpt
        self.children = [declarations,instructionsOpt]

class Condition(Node):
    def __init__(self, expr):
        self.expr = expr
        self.children = [expr]

class BinExpr(Node):

    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

        self.children = [op,left,right]

class Expr(Node):
    def __init__(self, expr):
        self.expr = expr
        self.children = [expr]

class ID (Node):
    def __init__(self,id,line,column):
        self.id = id
        self.lineno = line
        self.column = column
        self.children = [id]

class Const(Node):
    def __init__(self, value):
        self.type='const'
        self.value = value

class Integer(Const):
    def __init__(self, value,line,column):
        self.type='int'
        self.value = value
        self.lineno = line
        self.column = column


class Float(Const):
    def __init__(self,value, line,column):
        self.type='float'
        self.value = value
        self.lineno = line
        self.column = column

class String(Const):
    def __init__(self,value,line,column):
        self.type='string'
        self.value = value
        self.lineno = line
        self.column = column

class PExprListOrEmpty(Node):
    def __init__(self, expr_list = None):
        self.expr_list = expr_list
        self.children = [expr_list]

class PExprList(Node):
    def __init__(self, expr, expr_list = None):
        self.expr_list = expr_list
        self.expr = expr
        self.children = [expr_list,expr]
