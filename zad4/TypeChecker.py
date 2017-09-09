#!/usr/bin/python
import AST
from ReturnType import ReturnType
from SymbolTable import SymbolTable
from SymbolTable import VariableSymbol,FuncSymbol
from scanner import Scanner

def print_recursive(ast_node,level):
    for p in ast_node:
        if type(p) == tuple:
            print_recursive(p,level+1)
        elif p != '':
            for pipe in range(level):
                print '|',
            print p

class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        #print method
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    #def visit_NoneType(self,node):
    #    pass

    def generic_visit(self, node):        # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        elif node.children is not None:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)

    # simpler version of generic_visit, not so general
    #def generic_visit(self, node):
    #    for child in node.children:
    #        self.visit(child)



class TypeChecker(NodeVisitor):

    def __init__(self):
        self.stack = SymbolTable("global",None)
        self.error_occured = False

    def pickMinPos(self,coord1,coord2):
        if coord1[0] == coord2[0]:
            if coord1[1] < coord2[1]: return coord1
            else: return coord2
        else:
            if coord1[0] < coord2[0]:return coord1
            else: return coord2

    def visit_BinExpr(self, node):
                                          # alternative usage,
                                          # requires definition of accept method in class Node
        type1_desc = self.visit(node.left)[0]     # type1 = node.left.accept(self)
        type2_desc = self.visit(node.right) [0]   # type2 = node.right.accept(self)
        #type_desc: tuples in form (type,line,column) if this is constant
        #if  type_desc is variable, its name will be attached as the 4th element of the tuple
        op    = node.op
        #print "bin",type1_desc,type2_desc
        type1,coords1 = type1_desc[0],(type1_desc[1],type1_desc[2])
        type2,coords2 = type2_desc[0],(type2_desc[1],type2_desc[2])
        min_line,min_col = self.pickMinPos(coords1,coords2)
        returnType = ReturnType()
        try:
            if type1 == 'id':
                id = type1_desc[3]
                p = self.stack #search all scopes for a variable name
                while p is not None:
                    var = p.get(id)
                    if var:
                        if type(var) == FuncSymbol:
                            print "There already is a declared function for the name", id
                            p = None
                            break
                        type1 = var.type
                        break
                    p = p.getParentScope()
                if p is None:
                    print 'Using undeclared element',id,'line:',min_line,"column:",min_col
                    self.error_occured = True
                    # here we check if we found bottom of the stack i.e.  p== None. Else p != None because of the break instr
            if type2 == 'id':
                id = type2_desc[3]
                p = self.stack #search all scopes for a variable name
                while p is not None:
                    var = p.get(id)
                    if var:
                        if type(var) == FuncSymbol:
                            print "There already is a declared function for the name", id
                            p = None
                            break
                        type2 = var.type
                        break
                    p = p.getParentScope()
                if p is None:
                    print 'Using undeclared element', id,'line:',min_line,"column:",min_col
                    self.error_occured = True
                    # here we check if we found bottom of the stack i.e.  p== None. Else p != None because of the break instr
            res = [(returnType.ttype[op][type1][type2],min_line,min_col)]
            return res
        except KeyError:
            print "operation not allowed between",type1,"and",type2,"line", min_line,"column",min_col
            self.error_occured = True
            return [('error',min_line,min_col)]


    def searchAllScopes(self, key):
        # searches all scopes trying to find if the name
        # has been declared somewhere down the stack
        p = self.stack
        while p is not None:
            res = p.get(key)
            if res:
                return res
            p = p.getParentScope()
        return None

    def visit_Assignment(self, node):
        item = self.searchAllScopes(node.id.id)
        # ^ searching if this item has not been declared higher
        if not item:
            print "Variable", node.id.id,"has not been defined, line:", node.id.lineno,"column:",node.id.column
            self.error_occured = True
        else:
            if type(item) == FuncSymbol:
                print "Assignment to a function? Really? line:", node.id.lineno,"column:",node.id.column
                self.error_occured = True
            else:
                res = self.visit(node.expr)[0]
                res_type = res[0]
                try:
                    returnType = ReturnType()
                    if res[0] == "id":
                        var = self.searchAllScopes(res[3])
                        if var:
                            if type(var) == FuncSymbol:
                                print "Wrong usage of function",var.name,"line:",node.id.lineno,"column:",node.id.column
                                self.error_occured = True
                                res_type = "error"
                            else:
                                res_type = var.type
                    operation = returnType.ttype["="][item.type][res_type]
                    if type(operation) == tuple:
                        print operation[1],"line:",node.id.lineno, "column:",node.id.column
                except KeyError:
                    print "Variable",node.id.id,"has type:", item.type,"but got:",res_type,\
                        "line:",node.id.lineno,"column:",node.id.column
                    self.error_occured = True

    def visit_Expr(self,node):
        res = self.visit(node.expr)
        print "expr",res
        return  res

    def visit_Condition(self,node):
        res = self.visit(node.expr)
        return res

    def visit_BreakInstr(self,node):
        if not self.isInScope("while") and not self.isInScope("repeat"):
            print "Break instruction can only be invoked from  within a loop, line:", node.lineno, "column:",node.column
            self.error_occured = True

    def visit_ContinueInstr(self,node):
        if not self.isInScope("while") and not self.isInScope("repeat"):
            print "Continue instruction can only be invoked from  within a loop, line:", node.lineno, "column:",node.column
            self.error_occured = True

    def visit_ChoiceInstr(self,node):
        self.visit(node.if_cond)
        self.stack = self.stack.pushScope("if")
        self.visit(node.if_instr)
        self.stack = self.stack.popScope()
        if node.else_instr:
            self.stack = self.stack.pushScope("else")
            self.visit(node.else_instr)
            self.stack = self.stack.popScope()

    def visit_RepeatInstr(self,node):
        self.stack = self.stack.pushScope("repeat")
        for child in node.children: self.visit(child)
        self.stack = self.stack.popScope()

    def visit_WhileInstr(self,node):
        self.stack = self.stack.pushScope("while")
        checked_cond = self.visit(node.cond)
        if checked_cond[0][0] == 'error':
            print "wrong condition, expected expression, got error, line:",checked_cond[0][1], "column:",checked_cond[0][2]
            self.error_occured = True
        self.visit(node.instr)
        self.stack = self.stack.popScope()

    def visit_CompoundInstr(self,node):
        self.stack = self.stack.pushScope("scope")
        if node.declarations: self.visit(node.declarations)
        if node.instructionsOpt: self.visit(node.instructionsOpt)
        self.stack = self.stack.popScope()

    def visit_FuncDef(self,node):
        if node.args_list_or_empty:
            arg_types,fun_vars = self.visit(node.args_list_or_empty)
        else:
            arg_types,fun_vars = [(),()]
        #for convnenience this is a list-pair of: 1)types 2)pairs (name,type)
        #arg_types are only types without names composing local vars
        #fun_vars are full description of local variables, that we must add to
        #the new scope created below
        if not self.stack.get(node.id.id):
            # ^ declaration of function must be added to the global scope
            redefinition_error = False
            self.stack = self.stack.pushScope("fun " + node.type)
            for var_desc in fun_vars:
                var = VariableSymbol(var_desc[0],var_desc[1])
                if not self.stack.get(var_desc[0]): #if the variable name was not used in the current context
                    self.stack.put(var_desc[0],var)
                    #^here we make a use of fun_vars: we just iterate through the collection
                    # creating objects of type VariableSymbol without the need
                    #of any further processing of the elements of that collection
                else:
                    print "variable redefinition at line:",node.id.lineno,"column:",node.id.column
                    self.error_occured = True
                    redefinition_error = True
            if not redefinition_error:
                funcDefVar = FuncSymbol(node.id.id,node.type,arg_types)
                self.stack.getParentScope().put(node.id.id, funcDefVar)
                # ^ we are already in the function body scope, so we need to "borrow" the parent scope for this operation
            self.visit(node.compound_instr)
            self.stack = self.stack.popScope()
        else:
            print "Redefinition of the function",node.id.id,"line:",node.id.lineno,"column:",node.id.column
            self.error_occured = True

    def isInScope(self, name):
        # this is called by visitor of continue, break and return;
        # checks if the parent scope or some scope "down the stack"
        # is of the proper type(its name has to be while, repeat or fun_type)
        p = self.stack
        while p is not None:
            name_elems = p.name.split()
            # if in "name" is passed "while" or "repeat", arg 'name' will perfectly match scope name
            # otherwise it requires farther processing, since its name is "parametrized"
            # like: fun str or fun int
            if name_elems[0] == name:
                return name_elems
            p = p.getParentScope()
        return None

    def visit_ReturnInstr(self,node):
        scope_desc = self.isInScope("fun")# scope_desc has the form of ["fun", type]
        if not scope_desc:
            print "return can only be invoked from within a function, line:", node.lineno,"column:",node.column
            self.error_occured = True
        else:
            varRetValDesc = self.visit(node.expr)[0]
            # parse argument of "return"; retVal is in form ["type",line,column] if this is literal
            # otherwise it is variable and is of form ["id",line,column,var_name]
            var_ret_type = varRetValDesc[0]
            if var_ret_type == "id":
                var_obj = self.searchAllScopes(varRetValDesc[3])
                # check if object of the variable name exists somewhere in the stack and has the correct type
                if var_obj:
                    var_ret_type = var_obj.type
                else:
                    print "Element", varRetValDesc[3], "has not been declared, line:", node.lineno, "column:", node.column
                    self.error_occured = True
            try:
                returnType = ReturnType()
                try_operation = returnType.ttype["="][scope_desc[1]][var_ret_type]
                if type(try_operation) == tuple:
                    print try_operation[1], "line: ", node.lineno, "column:", node.column
            except KeyError:
                print "Type error: Return type is", scope_desc[1] + ",","got",var_ret_type,"instead, line:",node.lineno,"column:",node.column
                self.error_occured = True

    def visit_ArgsListOrEmpty(self,node):
        if node.argsList:
            return self.visit(node.argsList)
        else: return [(),()]

    def visit_ArgsList(self,node):
        res = self.visit(node.arg)
        if node.args_list:
            types,var_desc = self.visit(node.args_list)
            res[0] += types
            res[1] += var_desc
        return res

    def visit_DeclaredFunc(self,node):
        args_names =[]
        returnType = ReturnType()
        if node.expr_list_or_empty:
            args_names = self.visit(node.expr_list_or_empty)
        fundefvar = self.searchAllScopes(node.id.id)
        if fundefvar and type(fundefvar) == FuncSymbol:
            fun_args = fundefvar.types
            if fun_args.__len__() == args_names.__len__():
                error_in_arguments = False
                for i in range (fun_args.__len__()):
                    arg_type = args_names[i][0]
                    # ^ default if passed a constant
                    if args_names[i][0] == 'id':
                        #if passed a named variable we must check if it has been declared:
                        var = self.searchAllScopes(args_names[i][3])
                        if var:
                            #check if argument has been declared and is not a function name
                            if type(var) == VariableSymbol:
                                arg_type = var.type
                            else:
                                #We have a function!
                                print "Wrong call of a function",var.name, " at line:", node.id.lineno,"column:",node.id.column
                                error_in_arguments = True
                                self.error_occured = True
                        else:
                            print "Variable", args_names[i][3],"has not been declared, line:", node.id.lineno,"column:",node.id.column
                            error_in_arguments = True
                            self.error_occured = True
                    try:
                        table_val = returnType.ttype['='][fun_args[i]][arg_type]
                        if type(table_val) == tuple:
                            print table_val[1],"at line:",node.id.lineno,"column:",node.id.column
                            # ^ here we check if there is no extra msg indicating possible loss of precision
                    except KeyError:
                        print "Argument of a function",node.id.id,"has type:",arg_type ,"but expected type is:", fun_args[i],\
                            "line:",node.id.lineno,"column:",node.id.column
                        error_in_arguments = True
                        self.error_occured = True
                if not error_in_arguments:
                    return [(fundefvar.type,node.id.lineno,node.id.column)]
                else:
                    self.error_occured = True
                    return [('error',node.id.lineno,node.id.column)]
            else:
                print "function",node.id.id,"takes", fun_args.__len__(),"arguments, passed", args_names.__len__(),\
                    "line:",node.id.lineno,"column:",node.id.column
                self.error_occured = True
                return [('error',node.id.lineno,node.id.column)]
        else:
            print "function",node.id.id,"has not been declared,line:",node.id.lineno,"column:",node.id.column
            self.error_occured = True
            return [('error',node.id.lineno,node.id.column)]

    def visit_PExprListOrEmpty(self,node):
        if node.expr_list:
            return self.visit(node.expr_list)
        else: return []

    def visit_PrintInstr(self,node):
        list_desc = self.visit(node.expr_list)
        # list of tuples in form ('id', line,column, name) or (type, line,column)
        for desc in list_desc:
            if desc[0] == "id":
                var_obj = self.searchAllScopes(desc[3])
                if not var_obj:
                    print "Element", desc[3],"has not been declared at line:",desc[1], "column:",desc[2]
                    self.error_occured = True


    def visit_PExprList(self,node):
        res = self.visit(node.expr)
        if node.expr_list:
            res += self.visit(node.expr_list)
        return res

    def visit_Arg(self,node):
        return [(node.type,), ([node.id.id, node.type],)]
        #for convnenience this is a list-pair of: 1)types 2)pairs (name,type)

    def visit_Declaration(self,node):
        returnType = ReturnType()
        res = self.visit(node.inits)
        for declaration in res if res!= None else []:
            child_name, child_type, line, column =\
                declaration[0],declaration[1],declaration[2],declaration[3]
            # ^ that tuple can mean assigning a variable, which has not 4 but 5 elements
            if child_type == "id":
                #if the operation does assigning a variable, we need first check if it was
                #declared and if it has correct type:
                assigned_variable_name = declaration[4]
                var = self.stack.get(assigned_variable_name)
                if var:
                    if type(var) == VariableSymbol:
                        #get the var's type
                        child_type = var.type
                    else:
                        print "Wrong call of a function",assigned_variable_name, " at line:", line,"column:",column
                        self.error_occured = True
                else:
                    print "variable",assigned_variable_name, "has not been declared, line:", line,"column:",column
                    self.error_occured = True
            try:
               table_val = returnType.ttype["="][node.type][child_type]
               if type(table_val) == tuple:
                   print table_val[1],"at line:",line,"column:",column
                   # ^ here we check if there is no extra msg indicating possible loss of precision
               if self.stack.get(child_name) is not None:
                   print "Redeclaration of","'" + child_name+"'","at line:",line,"column:",column
                   self.error_occured = True
               else:
                   var_symbol = VariableSymbol(child_name,node.type)
                   self.stack.put(child_name,var_symbol)
            except KeyError:
                print "wrong assignment: type",node.type,"declaration:", child_type,"at line:",line,"column:",column
                self.error_occured = True

    def visit_Inits(self,node):
        res = self.visit(node.init)
        if node.inits: res += self.visit(node.inits)
        #print "inits",res
        return res

    def visit_Init(self,node):
        res = (node.id.id,) #name of the variable, later referenced to as child_name
        if node.expr:
            res += self.visit(node.expr)[0]
            #print "init",res
            return [res]

    def visit_ID(self,node):
        return [('id',node.lineno,node.column,node.id)]

    def visit_Integer(self, node):
        return [('int',node.lineno,node.column)]

    def visit_Float(self, node):
        return [("float",node.lineno,node.column)]

    def visit_String(self,node):
        return [("string",node.lineno,node.column)]

