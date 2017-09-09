class Operation:

    def __init__(self):
        self.operation_map = {}
        self.operation_map["+"] = self.plus
        self.operation_map["-"] = self.minus
        self.operation_map["*"] = self.times
        self.operation_map["/"] = self.div
        self.operation_map["%"] = self.mod
        self.operation_map["|"] = self.bitor
        self.operation_map["&"] = self.bitand
        self.operation_map["^"] = self.xor
        self.operation_map["&&"] = self.and_
        self.operation_map[r"\|\|"] = self.or_
        self.operation_map["<<"] = self.shl
        self.operation_map[">>"] = self.shr
        self.operation_map["=="] = self.eq
        self.operation_map["!="] = self.neq
        self.operation_map["<="] = self.le
        self.operation_map[">="] = self.ge
        self.operation_map[">"] = self.g
        self.operation_map["<"] = self.l
        self.operation_map["="] = self.assign

    def plus(self,var1,var2,type1,type2):
        return var1 + var2

    def minus(self,var1,var2,type1,type2):
        return var1 - var2

    def times(self,var1,var2,type1,type2):
        return var1 * var2

    def div(self,var1,var2,type1,type2):
        return var1 / var2

    def mod(self,var1,var2,type1,type2):
        return var1 % var2

    def bitor(self,var1,var2,type1,type2):
        return var1 | var2

    def bitand(self,var1,var2,type1,type2):
        return var1 & var2

    def xor(self,var1,var2,type1,type2):
        return var1 ^ var2

    def and_(self,var1,var2,type1,type2):
        return var1 and var2

    def or_(self,var1,var2,type1,type2):
        return var1 or var2

    def shl(self,var1,var2,type1,type2):
        return var1 << var2

    def shr(self,var1,var2,type1,type2):
        return var1 >> var2

    def eq(self,var1,var2,type1,type2):
        return var1 == var2

    def neq(self,var1,var2,type1,type2):
        return var1 != var2

    def le(self,var1,var2,type1,type2):
        return var1 <= var2

    def ge(self,var1,var2,type1,type2):
        return var1>=var2

    def g(self,var1,var2,type1,type2):
        return var1 > var2

    def l(self,var1,var2,type1,type2):
        return var1 < var2

    def assign(self,var1,var2,type1,type2):
        if type1 == 'float': return float(var2)
        elif type1 == 'int': return int(var2)
        else: return str(var2)

    def calculate(self,var1,var2,op):
        fun = self.operation_map[op]
        return fun(var1,var2,type(var1), type(var2))