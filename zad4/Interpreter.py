
import AST
from SymbolTable import *
from Memory import *
from Exceptions import  *
from visit import *
import sys
from Operation import Operation

sys.setrecursionlimit(10000)

class Interpreter(object):

    def __init__(self):
        self.memory_stack = MemoryStack()
        self.symbol_table = SymbolTable("functions_defs", None)
        self.current_scope_name = "global"

    @on('node')
    def visit(self, node):
        pass
    """
    This is the generic method that initializes the
    dynamic dispatcher.
    """

    @when(AST.Program)
    def visit(self,node):
        node.main_parts_interlacing.accept(self)

    @when(AST.Declaration)
    def visit(self,node):
        node.inits.accept(self)

    @when(AST.Declarations)
    def visit(self,node):
        if node.declarations: node.declarations.accept(self)
        if node.declaration: node.declaration.accept(self)

    @when (AST.Init)
    def visit(self,node):
        value = node.expr.accept(self)
        self.memory_stack.insert(node.id.id,value)

    @when(AST.MainPartsInerlacing)
    def visit(self,node):
        if node.main_parts: node.main_parts.accept(self)
        node.main_part.accept(self)

    @when (AST.Inits)
    def visit(self,node):
        node.init.accept(self)
        if node.inits: node.inits.accept(self)

    @when (AST.PExprListOrEmpty)
    def visit(self,node):
        if node.expr_list: return node.expr_list.accept(self)

    @when (AST.Expr)
    def visit(self,node):
        node.expr.accept(self)

    @when(AST.MainPart)
    def visit(self,node):
        node.main_part.accept(self)

    @when(AST.Assignment)
    def visit(self, node):
        value = node.expr.accept(self)
        self.memory_stack.set(node.id.id,value)

    @when(AST.PrintInstr)
    def visit(self,node):
        exprs = node.expr_list.accept(self)
        for e in exprs if type(exprs) is tuple else (exprs,): print e,
        # ^ here we ensure that the result is always iterable
        print

    @when (AST.PExprList)
    def visit(self, node):
        values = node.expr.accept(self)
        values = values if type(values) is tuple else (values,)
        if node.expr_list:
            res = node.expr_list.accept(self)
            values += res if type(res) is tuple else (res,)
            # ^ instructions like this serve the purpose of flattening the tuple
        return values

    @when(AST.BinExpr)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        operation_manager = Operation()
        res = operation_manager.calculate(r1,r2,node.op)
        return res

    @when (AST.ID)
    def visit(self, node):
        value = self.memory_stack.get(node.id)
        if value is not None: return value # it goes to sth that is not init
        else: return node.id #it goes to init

    @when(AST.Integer)
    def visit(self, node):
        return int(node.value)

    @when(AST.Float)
    def visit(self, node):
        return float(node.value)

    @when(AST.String)
    def visit(self, node):
        return str(node.value[1:-1])

    @when(AST.WhileInstr)
    def visit(self, node):
        r = None
        while node.cond.accept(self):
            try:
                r = node.instr.accept(self)
            except BreakException:
                break
            except ContinueException:
                pass
        return r

    @when(AST.CompoundInstr)
    def visit(self,node):
        self.memory_stack.push("scope")
        if node.declarations: node.declarations.accept(self)
        try:
            if node.instructionsOpt:
                node.instructionsOpt.accept(self)
        except BreakException:
            self.memory_stack.pop()
            raise BreakException
        except ContinueException:
            self.memory_stack.pop()
            raise ContinueException
        self.memory_stack.pop()

    @when(AST.InstructionsOpt)
    def visit(self,node):
        if node.instructions: node.instructions.accept(self)

    @when(AST.Instructions)
    def visit(self,node):
        if node.instructions: node.instructions.accept(self)
        node.instruction.accept(self)

    @when(AST.ChoiceInstr)
    def visit(self,node):
        if node.if_cond.accept(self):
            node.if_instr.accept(self)
        elif node.else_instr:
            node.else_instr.accept(self)

    @when(AST.Instruction)
    def visit(self,node):
        node.expr.accept(self)

    @when(AST.RepeatInstr)
    def visit(self,node):
        while 1:
            try:
                r = node.instr.accept(self)
            except BreakException:
                break
            except ContinueException:
                pass
            if node.condition.accept(self): break

    @when(AST.BreakInstr)
    def visit(self,node):
        raise BreakException()

    @when(AST.ContinueInstr)
    def visit(self,node):
        raise ContinueException()

    @when(AST.Condition)
    def visit(self, node):
        return node.expr.accept(self)

    @when (AST.ReturnInstr)
    def visit(self, node):
        raise ReturnValueException(node.expr.accept(self))

    @when(AST.DeclaredFunc)
    def visit(self,node):
        if node.expr_list_or_empty: args_list = node.expr_list_or_empty.accept(self)
        else: args_list = ()
        self.memory_stack.push_function_mem(node.id.id)
        args_list = args_list if type(args_list) is tuple else (args_list,)
        funVar = self.symbol_table.get(node.id.id)
        ret_val = 0
        for i in range(args_list.__len__()):
            self.memory_stack.insert(funVar.fun_vars[i][0],args_list[i])
        try:
            funVar.ast_node.compound_instr.accept(self)
        except ReturnValueException as ret:
            ret_val = ret.value
        self.memory_stack.pop_function_mem()
        return ret_val

    @when(AST.FuncDefsOpt)
    def visit(self,node):
        if node.fundefs: node.fundefs.accept(self)

    @when(AST.FuncDefs)
    def visit(self,node):
        node.fundef.accept(self)
        if node.fundefs: node.fundefs.accept(self)


    @when(AST.FuncDef)
    def visit(self,node):
        if node.args_list_or_empty:
            arg_types,fun_vars = node.args_list_or_empty.accept(self)
        else:
            arg_types,fun_vars = [(),()]
        #for convnenience this is a list-pair of: 1)types 2)pairs (name,type)
        #arg_types are only types without names composing local vars
        #fun_vars are full description of local variables, that we must add to
        #the new scope created below
        funcDefVar = FuncSymbol(node.id.id,node.type,arg_types,fun_vars,node)
        # ^ I also preserve the reference to the node: it will be called later
        self.symbol_table.put(node.id.id, funcDefVar)

    @when(AST.ArgsListOrEmpty)
    def visit(self, node):
        if node.argsList: return node.argsList.accept(self)
        else: return [(),()]

    @when(AST.ArgsList)
    def visit(self, node):
        res = node.arg.accept(self)
        if node.args_list:
            types,var_desc = node.args_list.accept(self)
            res[0] += types
            res[1] += var_desc
        return res

    @when(AST.Arg)
    def visit(self, node):
        return [(node.type,), ([node.id.id, node.type],)]
        #for convnenience this is a list-pair of: 1)types 2)pairs (name,type)