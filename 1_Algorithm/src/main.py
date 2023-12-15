import os

from src.codegen.Codegen import Codegen
from src.lexer import Lexer
from src.parser.Grammar import Grammar
from src.parser.LR1Table import LR1Table


grammar_path = './grammar/grammar.pl0'
in_folder_path = './in'
out_folder_path = './out'
files = [os.path.abspath(os.path.join(in_folder_path,file)) for file in os.listdir(in_folder_path) if file.endswith(".pl0")]
# file_path = 'in/test.pl0'
# file_path = 'in/multi-while.pl0'
for file_path in files:
    codegen = Codegen((LR1Table(Grammar(open(grammar_path).read())).
                       get_reduce_result(Lexer(file_path).tokenize())))
    try:
        codegen.process()
        print(f'\nCode: {codegen}')
        with open(f'{out_folder_path}/{os.path.basename(file_path).split(".")[0]}-out.txt', 'w') as file:
            file.write(str(codegen))
    except RuntimeError as re:
        print(re)
