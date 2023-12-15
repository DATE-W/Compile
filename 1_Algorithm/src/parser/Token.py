"""是否是终结符"""
token_dict = {
    'PROG': False,
    'HEADER': False,
    'SUBPROG': False,
    'PROGRAM': True,
    'CONST_STATEMENT': False,
    'CONST_': False,
    'CONST_DEF': False,
    'VARIABLE_STATEMENT': False,
    'VARIABLE_': False,
    'ID': False,
    'COMP_STATEMENT': False,
    'M_IF': False,
    'M_BEFORE_WHILE': False,
    'M_AFTER_WHILE': False,
    # 'COMP_BODY': False,
    # 'COMP_BODY_': False,
    'COMP_BEGIN': False,
    'STATEMENT': False,
    'ASSIGN_STATEMENT': False,
    'EXPR': False,
    'PLUS': False,
    'ITEM': False,
    'FACTOR': False,
    'MUL': False,
    'REL': False,
    'COND_STATEMENT': False,
    'WHILE_STATEMENT': False,
    'CONDITION': False,
    'UINT': False,
    'num': True,
    'id': True,
    'BEGIN': True,
    'END': True,
    'IF': True,
    'THEN': True,
    'ELSE': True,
    'DO': True,
    'CONST': True,
    'VAR': True,
    'WHILE': True,
    ';': True,
    ',': True,
    ':=': True,
    '(': True,
    ')': True,
    '+': True,
    '-': True,
    '*': True,
    '/': True,
    '=': True,
    '<': True,
    '<=': True,
    '>': True,
    '>=': True,
    '<>': True,
    '^': True,
}

"""
example:

PROGRAM add
VAR x,y;
x:=1;

process should be: (input, state, symbol)
PROGRAM, 0, #
action: s3
id, 03, #PROGRAM
action: s9
VAR, 039, #PROGRAM id
action: r14 (ID -> id)
VAR, 038, #PROGRAM ID
action: r2 (HEADER -> PROGRAM ID)
VAR, 01, #HEADER
action: r5 (CONST_STATEMENT -> ^)
VAR, 016, #HEADER CONST_STATEMENT
action: s13
id, 016'13', #HEADER CONST_STATEMENT VAR
action: s20
,, 016'13''20', #HEADER CONST_STATEMENT VAR id
action: r14
,, 016'13''19', #HEADER CONST_STATEMENT VAR ID
action: r12 (VARIABLE_ -> VAR ID)
,, 016'15', #HEADER CONST_STATEMENT VARIABLE_
action: s33
id, 016'15''33', #HEADER CONST_STATEMENT VARIABLE_ , 
action: s20
;, 016'15''33''20', #HEADER CONST_STATEMENT VARIABLE_ , id
action: r14
;, 016'15''33''63', #HEADER CONST_STATEMENT VARIABLE_ , ID
action: r13 (VARIABLE_ -> VARIABLE_ , ID)
;, 016'15', #HEADER CONST_STATEMENT VARIABLE_
action: s32
id, 016'15''32', #HEADER CONST_STATEMENT VARIABLE_ ;
action: r10 (VARIABLE_STATEMENT -> VARIABLE_ ;)
id, 016'14', #HEADER CONST_STATEMENT VARIABLE_STATEMENT
action: s31
:=, 016'14''31', #HEADER CONST_STATEMENT VARIABLE_STATEMENT id
action: r14
:=, 016'14''21', #HEADER CONST_STATEMENT VARIABLE_STATEMENT ID
action: s37
num, 016'14''21''37', #HEADER CONST_STATEMENT VARIABLE_STATEMENT ID :=
action: s70
;, 016'14''21''37''70', #HEADER CONST_STATEMENT VARIABLE_STATEMENT ID := num
action: r9 (UINT -> num)
;, 016'14''21''37''72', #HEADER CONST_STATEMENT VARIABLE_STATEMENT ID := UINT
action: r30 (FACTOR -> UINT)
;, 016'14''21''37''68', #HEADER CONST_STATEMENT VARIABLE_STATEMENT ID := FACTOR
action: r27 (ITEM -> FACTOR)
;, 016'14''21''37''66', #HEADER CONST_STATEMENT VARIABLE_STATEMENT ID := ITEM
action: r25 (EXPR -> ITEM)
;, 016'14''21''37''67', #HEADER CONST_STATEMENT VARIABLE_STATEMENT ID := EXPR
action: s105
#, 016'14''21''37''67''105', #HEADER CONST_STATEMENT VARIABLE_STATEMENT ID := EXPR ;
action: r23 (ASSIGN_STATEMENT -> ID := EXPR ;)
#, 016'14''28',  #HEADER CONST_STATEMENT VARIABLE_STATEMENT ASSIGN_STATEMENT
action: r18 (STATEMENT -> ASSIGN_STATEMENT)
#, 016'14''25',  #HEADER CONST_STATEMENT VARIABLE_STATEMENT STATEMENT
action: r3 (SUBPROG -> CONST_STATEMENT VARIABLE_STATEMENT STATEMENT)
#, 015,  #HEADER SUBPROG
action: r1 (PROG -> HEADER SUBPROG)
#, 02, #PROG
action: acc
"""
token_list = [
    'PROGRAM',
    'id',
    'VAR',
    'id',
    ',',
    'id',
    ';',
    'id',
    ':=',
    'num',
    # ';'
]

'''
example:

PROGRAM example
    VAR x, y;
    BEGIN
        x := 2;
        IF x > 3 THEN
            y := x + 5
    END
'''
token_list_1 = [
    ('PROGRAM', ''),
    ('id', 'example'),
    ('VAR', ''),
    ('id', 'x'),
    (',', ''),
    ('id', 'y'),
    (';', ''),
    ('BEGIN', ''),
    ('id', 'x'),
    (':=', ''),
    ('num', '2'),
    (';', ''),
    ('IF', ''),
    ('id', 'x'),
    ('>', ''),
    ('num', '3'),
    ('THEN', ''),
    ('id', 'y'),
    (':=', ''),
    ('id', 'x'),
    ('+', ''),
    ('num', '5'),
    # (';', ''),
    ('END', '')
]
