
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.2'

_lr_method = 'LALR'

_lr_signature = '\xf0R\xebt\x81\xdbD\xc0M\xb8DL\x8f\xfa\r\t'
    
_lr_action_items = {'RPAREN':([1,2,4,9,12,13,14,15,16,17,],[-3,-7,-6,15,-9,-5,-4,-8,-1,-2,]),'DIVIDE':([1,2,4,13,14,15,16,17,],[7,-7,-6,-5,-4,-8,7,7,]),'NUMBER':([0,3,6,7,8,10,11,],[2,2,2,2,2,2,2,]),'TIMES':([1,2,4,13,14,15,16,17,],[8,-7,-6,-5,-4,-8,8,8,]),'PLUS':([1,2,4,5,9,12,13,14,15,16,17,],[-3,-7,-6,10,10,-9,-5,-4,-8,-1,-2,]),'LPAREN':([0,3,6,7,8,10,11,],[3,3,3,3,3,3,3,]),'MINUS':([0,1,2,3,4,5,6,9,12,13,14,15,16,17,],[6,-3,-7,6,-6,11,6,11,-9,-5,-4,-8,-1,-2,]),'$end':([1,2,4,5,12,13,14,15,16,17,],[-3,-7,-6,0,-9,-5,-4,-8,-1,-2,]),}

_lr_action = { }
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = { }
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'term':([0,3,6,10,11,],[1,1,1,16,17,]),'expression':([0,3,6,],[5,9,12,]),'factor':([0,3,6,7,8,10,11,],[4,4,4,13,14,4,4,]),}

_lr_goto = { }
for _k, _v in _lr_goto_items.items():
   for _x,_y in zip(_v[0],_v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = { }
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> expression","S'",1,None,None,None),
  ('expression -> expression PLUS term','expression',3,'p_expression_plus','C:/Users/Robert/Desktop/Robert/agh/kompilatory/laby/zad2/MyYacc.py',13),
  ('expression -> expression MINUS term','expression',3,'p_expression_plus','C:/Users/Robert/Desktop/Robert/agh/kompilatory/laby/zad2/MyYacc.py',14),
  ('expression -> term','expression',1,'p_expression_term','C:/Users/Robert/Desktop/Robert/agh/kompilatory/laby/zad2/MyYacc.py',24),
  ('term -> term TIMES factor','term',3,'p_term_times','C:/Users/Robert/Desktop/Robert/agh/kompilatory/laby/zad2/MyYacc.py',29),
  ('term -> term DIVIDE factor','term',3,'p_term_div','C:/Users/Robert/Desktop/Robert/agh/kompilatory/laby/zad2/MyYacc.py',34),
  ('term -> factor','term',1,'p_term_factor','C:/Users/Robert/Desktop/Robert/agh/kompilatory/laby/zad2/MyYacc.py',39),
  ('factor -> NUMBER','factor',1,'p_factor_num','C:/Users/Robert/Desktop/Robert/agh/kompilatory/laby/zad2/MyYacc.py',44),
  ('factor -> LPAREN expression RPAREN','factor',3,'p_factor_expr','C:/Users/Robert/Desktop/Robert/agh/kompilatory/laby/zad2/MyYacc.py',49),
  ('expression -> MINUS expression','expression',2,'p_expr_uminus','C:/Users/Robert/Desktop/Robert/agh/kompilatory/laby/zad2/MyYacc.py',54),
]