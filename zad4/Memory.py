
class StackFrame:
    def __init__(self, name,parent):
        self.name = name
        self.parent = parent
        self.values = {}

    def has_key(self, name):  # variable name
        return self.values.has_key(name)

    def get(self, name):         # gets from memory current value of variable <name>
        if self.has_key(name): return self.values[name]
        else: return None

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.values[name] = value

class Memory:

    def __init__(self, name, parent): # memory name
        self.name = name
        self.parent = parent
        self.local_stack = StackFrame("local",None)

    def get_from_local_stack(self,name):
        p = self.local_stack
        while p is not None:
            var = p.get(name)
            if var is not None:
                return var
            p = p.parent
        return None

    def put_on_local_stack(self, name, value):
        self.local_stack.put(name,value)

    def set_on_local_stack_worked(self,name,value): #returns true if found on stack and set properly, false otherwise
        p = self.local_stack
        while p is not None:
            var = p.get(name)
            if var is not None:
                p.values[name] = value
                return True
            p = p.parent
        return False

    def push_on_local_stack(self, memory):
        self.local_stack = StackFrame(memory,self.local_stack)

    def pop_from_local_stack(self):
        self.local_stack = self.local_stack.parent


class MemoryStack: #entire stack
                                                                             
    def __init__(self, stackName=None):
        if stackName: self.top = StackFrame(stackName, None)
        else: self.top = StackFrame("global", None)
        self.function_memory = None

    def search_global_stack(self,name):
        p = self.top
        while p is not None:
            var = p.get(name)
            if var is not None:
                return var
            p = p.parent
        return None

    def get(self, name):
        if self.function_memory:
            var = self.function_memory.get_from_local_stack(name)
            if var is not None: return var
            else: return self.search_global_stack(name)
        else:
            return self.search_global_stack(name)

    def insert(self, name, value): # inserts into memory stack variable <name> with value <value>
        if self.function_memory:
            self.function_memory.put_on_local_stack(name,value)
        else:
            self.top.put(name,value)

    def set_on_global_stack(self,name,value):
        p = self.top
        while p is not None:
            var = p.get(name)
            if var is not None:
                p.put(name,value)
                break
            p = p.parent

    def set(self, name, value):
        # sets variable <name> to value <value>
        if self.function_memory:
            if not self.function_memory.set_on_local_stack_worked(name,value):
                self.set_on_global_stack(name,value)
        else:
            self.set_on_global_stack(name,value)


    def push(self, memory): # pushes memory <memory> onto the most nested frame of stack memory or global stack if the former does not exist
        if self.function_memory:
            self.function_memory.push_on_local_stack(memory)
        else:
            self.top = StackFrame(memory,self.top)

    def pop(self):          # pops the top memory from the global stack
        if self.function_memory:
            self.function_memory.pop_from_local_stack()
        else:
            self.top = self.top.parent

    def push_function_mem(self,memory):
        self.function_memory = Memory(memory,self.function_memory)

    def pop_function_mem(self):
        self.function_memory = self.function_memory.parent