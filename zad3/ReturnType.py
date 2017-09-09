class ReturnType:
    def __init__(self):

        EQ = r"=="
        NEQ = r"!="
        LE = r"<="
        GE = r">="
        OR = r"\|\|"
        AND = r"&&"
        SHL = r"<<"
        SHR = r">>"

        self.ttype = {}
        self.ttype['+'] = {}
        self.ttype['-'] = {}
        self.ttype['*'] = {}
        self.ttype['/'] = {}
        self.ttype['%'] = {}
        self.ttype['|'] = {}
        self.ttype['&'] = {}
        self.ttype['^'] = {}
        self.ttype[AND] = {}
        self.ttype[OR] = {}
        self.ttype[SHL] = {}
        self.ttype[SHR] = {}
        self.ttype[EQ] = {}
        self.ttype[NEQ] = {}
        self.ttype[LE] = {}
        self.ttype[GE] = {}
        self.ttype['>'] = {}
        self.ttype['<'] = {}
        self.ttype['='] = {}

        self.ttype['+']['int'] = {}
        self.ttype['-']['int'] = {}
        self.ttype['*']['int'] = {}
        self.ttype['/']['int'] = {}
        self.ttype['%']['int'] = {}
        self.ttype['|']['int'] = {}
        self.ttype['&']['int'] = {}
        self.ttype['^']['int'] = {}
        self.ttype[AND]['int'] = {}
        self.ttype[OR]['int'] = {}
        self.ttype[SHL]['int'] = {}
        self.ttype[SHR]['int'] = {}
        self.ttype[EQ]['int'] = {}
        self.ttype[NEQ]['int'] = {}
        self.ttype[LE]['int'] = {}
        self.ttype[GE]['int'] = {}
        self.ttype['>']['int']= {}
        self.ttype['<']['int'] = {}

        self.ttype['+']['float'] = {}
        self.ttype['-']['float'] = {}
        self.ttype['*']['float'] = {}
        self.ttype['/']['float'] = {}
        self.ttype['%']['float'] = {}
        self.ttype['|']['float'] = {}
        self.ttype['&']['float'] = {}
        self.ttype['^']['float'] = {}
        self.ttype[AND]['float'] = {}
        self.ttype[OR]['float'] = {}
        self.ttype[SHL]['float'] = {}
        self.ttype[SHR]['float'] = {}
        self.ttype[EQ]['float'] = {}
        self.ttype[NEQ]['float'] = {}
        self.ttype[LE]['float'] = {}
        self.ttype[GE]['float'] = {}
        self.ttype['>']['float']= {}
        self.ttype['<']['float'] = {}

        self.ttype['+']['string'] = {}
        self.ttype['*']['string'] = {}
        self.ttype[EQ]['string'] = {}
        self.ttype[NEQ]['string'] = {}
        self.ttype[LE]['string'] = {}
        self.ttype[GE]['string'] = {}
        self.ttype['>']['string']= {}
        self.ttype['<']['string'] = {}

        #integers
        self.ttype['+']['int']['int'] = 'int'
        self.ttype['+']['int']['float'] = 'float'

        self.ttype['-']['int']['int'] = 'int'
        self.ttype['-']['int']['float'] = 'float'

        self.ttype['*']['int']['int'] = 'int'
        self.ttype['*']['int']['float'] = 'float'

        self.ttype['/']['int']['int'] = 'int'
        self.ttype['/']['int']['float'] = 'float'

        self.ttype['%']['int']['int'] = 'int'
        self.ttype['|']['int']['int'] = 'int'
        self.ttype['&']['int']['int'] = 'int'
        self.ttype['^']['int']['int'] = 'int'
        self.ttype[AND]['int']['int'] = 'int'
        self.ttype[OR]['int']['int'] = 'int'
        self.ttype[SHL]['int']['int'] = 'int'
        self.ttype[SHR]['int']['int'] = 'int'
        self.ttype[EQ]['int']['int'] = 'int'
        self.ttype[NEQ]['int']['int'] = 'int'

        self.ttype['>']['int']['int'] = 'int'
        self.ttype['>']['int']['float'] = 'float'

        self.ttype['<']['int']['int'] = 'int'
        self.ttype['<']['int']['float'] = 'float'

        self.ttype[LE]['int']['int'] = 'int'
        self.ttype[LE]['int']['float'] = 'float'

        self.ttype[GE]['int']['int'] = 'int'
        self.ttype[GE]['int']['float'] = 'float'

        # floats

        self.ttype['+']['float']['float'] = 'float'
        self.ttype['+']['float']['int'] = 'float'

        self.ttype['-']['float']['float'] = 'float'
        self.ttype['-']['float']['int'] = 'float'

        self.ttype['*']['float']['float'] = 'float'
        self.ttype['*']['float']['int'] = 'float'

        self.ttype['/']['float']['float'] = 'float'
        self.ttype['/']['float']['int'] = 'float'

        self.ttype['>']['float']['float'] = 'float'
        self.ttype['>']['float']['int'] = 'float'

        self.ttype['<']['float']['float'] = 'float'
        self.ttype['<']['float']['int'] = 'float'

        self.ttype[LE]['float']['float'] = 'float'
        self.ttype[LE]['float']['int'] = 'float'

        self.ttype[GE]['float']['float'] = 'float'
        self.ttype[GE]['float']['int'] = 'float'

        #strings
        self.ttype['+']['string']['string'] = 'string'
        self.ttype['*']['string']['int'] = 'string'
        self.ttype['>']['string']['string'] = 'string'
        self.ttype['<']['string']['string'] = 'string'
        self.ttype[LE]['string']['string'] = 'string'
        self.ttype[GE]['string']['string'] = 'string'

        #assignments
        self.ttype['=']['string'] = {}
        self.ttype['=']['float'] = {}
        self.ttype['=']['int'] = {}

        self.ttype['=']['string']['string'] = 'string'
        self.ttype['=']['float']['int'] = 'float'
        self.ttype['=']['float']['float'] = 'float'
        self.ttype['=']['int']['float'] = 'int',"Warning: assigning float to int, possible loss of precision"
        self.ttype['=']['int']['int'] = 'int'