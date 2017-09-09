#!/usr/bin/python

class Symbol(object):
    def __init__(self, name, type):
        self.name = name
        self.type = type

class FuncSymbol(Symbol):
    def __init__(self,name,type,orered_tuple_of_types):
        self.name = name
        self.type = type
        self.types = orered_tuple_of_types

class VariableSymbol(Symbol):

    def __init__(self, name, type):
        self.name = name
        self.type = type


class SymbolTable(object):

    def __init__(self,  name, parent): # parent scope and symbol table name
        self.parent = parent
        self.name = name
        self.table = {}

    def put(self, name, symbol): # put variable symbol or fundef under <name> entry
        self.table[name] = symbol

    def get(self, name): # get variable symbol or fundef from <name> entry
        if self.table.has_key(name):
            return self.table[name]
        else:
            return None

    def getParentScope(self): #peek, not pop!!
        return self.parent


    def pushScope(self, name):
        new_scope = SymbolTable(name,self)
        return new_scope


    def popScope(self):
        return self.parent


