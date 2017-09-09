
class Node(object):

    def __str__(self):
        #return self.printTree()
        return ''


class Program(Node):
    def __init__(self, main_parts_interlacing ):
        """
        self.declarations = declarations
        self.fundefopt = fundefopt
        self.instr_opt = instr_opt
        """
        self.main_parts_interlacing = main_parts_interlacing

class MainPartsInerlacing(Node):
    def __init__(self, main_parts, main_part ):
        self.main_parts = main_parts
        self.main_part = main_part

class MainPart(Node):
    def __init__(self, main_part ):
        self.main_part = main_part

class Declarations(Node):
    def __init__(self, declarations=None, declaration=None):
        self.declarations = declarations
        self.declaration = declaration

class Declaration(Node):
    def __init__(self, type, inits):
        self.type = type
        self.inits = inits

class Inits(Node):
    def __init__(self, init, inits=None ):
        self.inits = inits
        self. init = init

class Init(Node):
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr


class FuncDefsOpt(Node):
    def __init__(self, fundefs=None):
        self.fundefs = fundefs

class FuncDefs(Node):
    def __init__(self, fundef,fundefs=None):
        self.fundefs = fundefs
        self.fundef = fundef

class FuncDef(Node):
    def __init__(self, type, id, args_list_or_empty, compound_instr):
        self.type = type
        self.id = id
        self.args_list_or_empty = args_list_or_empty
        self.compound_instr = compound_instr

class DeclaredFunc(Node):
    def __init__(self,id,expr_list_or_empty):
        self.id = id
        self.expr_list_or_empty = expr_list_or_empty

class ArgsListOrEmpty(Node):
    def __init__(self, argsList=None):
        self.argsList= argsList

class ArgsList(Node):
    def __init__(self, arg, args_list = None):
        self.args_list= args_list
        self.arg = arg

class Arg(Node):
    def __init__(self, type,id):
        self.type = type
        self.id = id

class InstructionsOpt(Node):
    def __init__(self, instructions = None):
        self.instructions = instructions

class Instructions(Node):
    def __init__(self, instructions, instruction):
        self.instructions = instructions
        self.instruction = instruction

class Instruction(Node):
    def __init__(self,expr):
        self.expr = expr

class PrintInstr(Instruction):
    def __init__(self, expr_list):
        self.expr_list = expr_list

class LabeledInstr(Instruction):
    def __init__(self,id,instruction):
        self.id = id
        self.instruction = instruction

class Assignment(Instruction):
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr

class ChoiceInstr(Instruction):
    def __init__(self, if_cond, if_instr, else_instr = None):
        self.if_cond = if_cond
        self.if_instr = if_instr
        self.else_instr = else_instr

class WhileInstr(Instruction):
    def __init__(self, cond, instr):
        self.cond = cond
        self.instr = instr

class RepeatInstr(Instruction):
    def __init__(self, instr, condition):
        self.instr = instr
        self.condition = condition

class ReturnInstr(Instruction):
    def __init__(self, expr):
        self.expr = expr

class BreakInstr(Instruction):
    def __init__(self):
        pass

class ContinueInstr(Instruction):
    def __init__(self):
        pass

class CompoundInstr(Instruction):
    def __init__(self, declarations, instructionsOpt):
        self.declarations = declarations
        self.instructionsOpt = instructionsOpt


class Condition(Node):
    def __init__(self, expr):
        self.expr = expr

class BinExpr(Node):

    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class Expr(Node):
    def __init__(self, expr):
        self.expr = expr

class ID (Node):
    def __init__(self,id):
        self.id = id

class Const(Node):
    def __init__(self, value):
        self.value = value

class Integer(Const):
    def __init__(self, value):
        self.value = int(value)


class Float(Const):
    def __init__(self,value):
        self.value = float(value)

class String(Const):
    def __init__(self,value):
        self.value = str(value)

class PExprListOrEmpty(Node):
    def __init__(self, expr_list = None):
        self.expr_list = expr_list

class PExprList(Node):
    def __init__(self, expr, expr_list = None):
        self.expr_list = expr_list
        self.expr = expr
