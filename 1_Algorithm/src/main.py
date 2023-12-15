import os

from src.codegen.Codegen import Codegen
from src.lexer import Lexer
from src.parser.Grammar import Grammar
from src.parser.LR1Table import LR1Table

grammar = Grammar(open('./grammar/grammar.pl0').read())
path = './in/test.txt'
codegen = Codegen((LR1Table(grammar).
                   get_reduce_result(Lexer(path).tokenize())))
try:
    codegen.process()
    print('\nCode: ')
    print(codegen)
    with open(f'./out/{os.path.basename(path).split(".")[0]}-out.txt', 'w') as file:
        file.write(str(codegen))
except RuntimeError as re:
    print(re)
