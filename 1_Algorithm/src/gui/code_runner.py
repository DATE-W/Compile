import os

from src.codegen.Codegen import Codegen
from src.lexer import Lexer
from src.parser.Grammar import Grammar
from src.parser.LR1Table import LR1Table


def code_runner(code: str):
    # grammar_path = './grammar/grammar.pl0'
    # in_folder_path = './in'
    # out_folder_path = './out'
    # files = [os.path.abspath(os.path.join(in_folder_path, file)) for file in os.listdir(in_folder_path) if
    #          file.endswith(".pl0")]
    # for file_path in files:
    #     codegen = Codegen((LR1Table(Grammar(open(grammar_path).read())).
    #                        get_reduce_result(Lexer(file_path).tokenize())))
    #     try:
    #         codegen.process()
    #         print(f'\nCode:\n{codegen}')
    #         out_path = f'{out_folder_path}/{os.path.basename(file_path).split(".")[0]}-out.txt'
    #         print(f'Result has been saved to {out_path}.')
    #         with open(out_path, 'w') as file:
    #             file.write(str(codegen))
    #     except RuntimeError as re:
    #         print(re)
    grammar_path = './grammar/grammar.pl0'
    out_folder_path = './out'

    # 1. 打开并读取文法文件
    grammar_file_content = open(grammar_path).read()

    # 2. 创建一个 Grammar 对象
    grammar = Grammar(grammar_file_content)

    # 3. 创建一个 LR1Table 对象
    lr1_table = LR1Table(grammar)

    try:
        # 4. 创建一个 Lexer 对象并对代码进行词法分析
        lexer = Lexer(code)
        tokens = lexer.tokenize()
    except RuntimeError as re:
        return None, re

    try:
        # 5. 获取归约结果
        reduce_results = lr1_table.get_reduce_result(tokens)
    except RuntimeError as re:
        return None, re

    try:
        # 6. 创建 Codegen 对象
        codegen = Codegen(reduce_results)
        codegen.process()
        print(f'\nCode:\n{codegen}')
        out_path = f'{out_folder_path}/output.txt'
        print(f'Result has been saved to {out_path}.')
        with open(out_path, 'w') as file:
            file.write(str(codegen))
    except RuntimeError as re:
        # print(re)
        return None, re

    return lr1_table.get_parse_table(), str(codegen)