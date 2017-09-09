import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator


class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self,lvl):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.Program)
    def printTree(self,lvl):
        """
        self.declarations.printTree(lvl)
        self.fundefopt.printTree(lvl)
        self.instr_opt.printTree(lvl)
        """
        self.main_parts_interlacing.printTree(lvl)

    @addToClass(AST.MainPartsInerlacing)
    def printTree(self,lvl):
        """
        self.declarations.printTree(lvl)
        self.fundefopt.printTree(lvl)
        self.instr_opt.printTree(lvl)
        """
        if self.main_parts: self.main_parts.printTree(lvl)
        if self.main_part:
            default_lvl = lvl
            if type(self.main_part) == AST.Declaration:
                print "DECL"
                default_lvl = lvl + 1
            elif type(self.main_part) == AST.FuncDef:
                print "FUNDEF"
                default_lvl = lvl + 1
        self.main_part.printTree(default_lvl)


    @addToClass(AST.Declarations)
    def printTree(self,lvl):
        if self.declarations or self.declaration:
            for pipe in range(lvl): print '|',
        if self.declarations:
            self.declarations.printTree(lvl)
        if self.declaration:
            print "DECL"
            self.declaration.printTree(lvl+1)

    @addToClass(AST.Declaration)
    def printTree(self,lvl):
        if self.inits: self.inits.printTree(lvl)

    @addToClass(AST.Inits)
    def printTree(self,lvl):
        if self.init: self.init.printTree(lvl)
        if self.inits: self.inits.printTree(lvl)

    @addToClass(AST.Init)
    def printTree(self,lvl):
        for pipe in range(lvl): print '|',
        print '='
        self.id.printTree(lvl+1)
        self.expr.printTree(lvl+1)

    @addToClass(AST.InstructionsOpt)
    def printTree(self,lvl):
        if self.instructions: self.instructions.printTree(lvl)

    @addToClass(AST.Instructions)
    def printTree(self,lvl):
        if self.instructions: self.instructions.printTree(lvl)
        if self.instruction: self.instruction.printTree(lvl)

    @addToClass(AST.Instruction)
    def printTree(self,lvl):
           if self.expr: self.expr.printTree(lvl)

    @addToClass(AST.PrintInstr)
    def printTree(self,lvl):
        for pipe in range(lvl): print '|',
        print "PRINT"
        self.expr_list.printTree(lvl+1)

    @addToClass(AST.LabeledInstr)
    def printTree(self,lvl):
        for pipe in range(lvl): print '|',
        print "LABELED"
        for pipe in range(lvl+1):print '|',
        print self.id
        self.expr_list.printTree(lvl+1)

    @addToClass(AST.Assignment)
    def printTree(self,lvl):
        for pipe in range(lvl): print '|',
        print "="
        self.id.printTree(lvl+1)
        self.expr.printTree(lvl+1)

    @addToClass(AST.ChoiceInstr)
    def printTree(self,lvl):
        for pipe in range(lvl): print '|',
        print "IF"
        self.if_cond.printTree(lvl+1),
        self.if_instr.printTree(lvl+1)
        if self.else_instr:
            for pipe in range(lvl): print '|',
            print "ELSE"
            self.else_instr.printTree(lvl+1)

    @addToClass(AST.WhileInstr)
    def printTree(self,lvl):
        for pipe in range(lvl): print '|',
        print "WHILE"
        self.cond.printTree(lvl+1)
        self.instr.printTree(lvl+1)

    @addToClass(AST.RepeatInstr)
    def printTree(self,lvl):
        for pipe in range(lvl): print '|',
        print "REPEAT"
        self.instr.printTree(lvl+1)
        for pipe in range(lvl): print '|',
        print "UNTIL"
        self.condition.printTree(lvl+1)

    @addToClass(AST.ReturnInstr)
    def printTree(self,lvl):
        for pipe in range(lvl): print '|',
        print "RETURN"
        self.expr.printTree(lvl+1)

    @addToClass(AST.BreakInstr)
    def printTree(self,lvl):
        for pipe in range(lvl): print '|',
        print "BREAK"

    @addToClass(AST.ContinueInstr)
    def printTree(self,lvl):
        for pipe in range(lvl): print '|',
        print "CONTINUE"

    @addToClass(AST.CompoundInstr)
    def printTree(self,lvl):
        if self.declarations: self.declarations.printTree(lvl)
        if self.instructionsOpt: self.instructionsOpt.printTree(lvl)

    @addToClass(AST.Condition)
    def printTree(self,lvl):
        self.expr.printTree(lvl)

    @addToClass(AST.BinExpr)
    def printTree(self,lvl):
        for pipe in range(lvl): print '|',
        print self.op
        self.left.printTree(lvl+1)
        self.right.printTree(lvl+1)

    @addToClass(AST.Expr)
    def printTree(self,lvl):
        if self.expr: self.expr.printTree(lvl)

    @addToClass(AST.ID)
    def printTree(self,lvl):
        for pipe in range(lvl): print '|',
        print self.id

    @addToClass(AST.Const)
    def printTree(self,lvl):
         #for pipe in range(lvl): print '|',
         #print self.value
        self.expr.printTree(lvl)

    @addToClass(AST.Integer)
    def printTree(self,lvl):
         for pipe in range(lvl): print '|',
         print self.value

    @addToClass(AST.Float)
    def printTree(self,lvl):
         for pipe in range(lvl): print '|',
         print self.value

    @addToClass(AST.String)
    def printTree(self,lvl):
         for pipe in range(lvl): print '|',
         print self.value

    @addToClass(AST.Const)
    def printTree(self,lvl):
         for pipe in range(lvl): print '|',
         print self.value

    @addToClass(AST.PExprListOrEmpty)
    def printTree(self,lvl):
         if self.expr_list: self.expr_list.printTree(lvl)

    @addToClass(AST.PExprList)
    def printTree(self,lvl):
         self.expr.printTree(lvl)
         if self.expr_list: self.expr_list.printTree(lvl)

    @addToClass(AST.FuncDefsOpt)
    def printTree(self,lvl):
         if self.fundefs:
             for pipe in range(lvl): print '|',
             print 'FUNDEF'
             self.fundefs.printTree(lvl+1)

    @addToClass(AST.FuncDefs)
    def printTree(self,lvl):
        self.fundef.printTree(lvl)
        if self.fundefs: self.fundefs.printTree(lvl)

    @addToClass(AST.FuncDef)
    def printTree(self,lvl):
         self.id.printTree(lvl)
         for pipe in range(lvl): print '|',
         print "RET", self.type
         if self.args_list_or_empty: self.args_list_or_empty.printTree(lvl)
         if self.compound_instr: self.compound_instr.printTree(lvl)

    @addToClass(AST.DeclaredFunc)
    def printTree(self,lvl):
         for pipe in range(lvl): print '|',
         print "FUNCALL"
         self.id.printTree(lvl+1)
         if self.expr_list_or_empty: self.expr_list_or_empty.printTree(lvl+1)

    @addToClass(AST.ArgsListOrEmpty)
    def printTree(self,lvl):
        if self.argsList: self.argsList.printTree(lvl)

    @addToClass(AST.ArgsList)
    def printTree(self,lvl):
        self.arg.printTree(lvl)
        if self.args_list: self.args_list.printTree(lvl)

    @addToClass(AST.Arg)
    def printTree(self,lvl):
        for pipe in range(lvl): print '|',
        print "ARG",
        self.id.printTree(0)