from Procedure import Procedure
class Codegen:
    def __init__(self, reduce_result):
        # 定义根过程，即最外层，第0层
        self.procedure = Procedure()
        self.procedure.add_procedure("_global",0)

        # 语法分析后得到的结果
        self.reduce_result = reduce_result

        # 中间变量计数器
        self.temp_counter = 0

        # 记录上一个被遍历的式子
        self.symbol_stack = []

    def process_const(self, generative):
        # 'UINT -> num'
        if generative[:4] == 'UINT':
            self.symbol_stack.append('1') # 假设提取出来的常量值是1
        elif generative == "CONST_DEF -> ID = UINT":
            # 将 值 pop出去
            const_value = self.symbol_stack.pop()
            # 将 = pop出去
            self.symbol_stack.pop()
            # 将 常量名 pop出去
            const_name = self.symbol_stack.pop()
            self.procedure.add_const(const_name, const_value)

    def process_var(self, generative):
        # 'ID -> id'
        if generative[:2] == 'ID':
            self.symbol_stack.append('x') # 假设提取出的变量名
            self.procedure.add_var('x')

    def process_procedure(self, generative):
        pass

    def process_assign(self, generative):


    def process(self):
        for item in self.reduce_result:
            if item in [
                'CONST_STATEMENT -> CONST_ ;',
                'CONST_STATEMENT -> ^',
                'CONST_ -> CONST CONST_DEF',
                'CONST_ -> CONST_ , CONST_DEF'
                'CONST_DEF -> ID = UINT',
                'UINT -> num'
            ]:
                self.process_const(item)
            elif item in [
                'VARIABLE_STATEMENT -> VARIABLE_;',
                'VARIABLE_STATEMENT -> ^',
                'VARIABLE_ -> VAR ID',
                'VARIABLE_ -> VARIABLE_, ID',
                'ID -> id'
            ]:
                self.process_var(item)
            elif item in [
                'PROG -> HEADER SUBPROG',
                'HEADER -> PROGRAM ID',
                'SUBPROG -> CONST_STATEMENT VARIABLE_STATEMENT STATEMENT',
            ]:
                self.process_procedure(item)
            elif item in [
                'ASSIGN_STATEMENT -> ID := EXPR'
            ]:
                self.process_assign(item)