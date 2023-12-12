from src.parser.LR1Table.Grammar import Grammar


class LR1Table:
    def __init__(self, gra: Grammar):
        # 扩展文法
        self.gra_prime = Grammar(f"{gra.start_symbol}' -> {gra.start_symbol}\n{gra.grammar_str}")
        # 开始符号的长度 + 1
        self.max_gra_prime_len = len(max(self.gra_prime.grammar, key=len))
        self.gra_indexed = []

        # 语法规范化，去除 |
        for head, bodies in self.gra_prime.grammar.items():
            for body in bodies:
                self.gra_indexed.append([head, body])

        # 求 first follow 集合
        self.first, self.follow = self.get_first_and_follow(self.gra_prime)
        # self.print_first_and_follow()

        # 构建项目集规范族
        self.Collection = self.LR1_items(self.gra_prime)
        # self.print_collections()

        # 构建LR1分析表
        self.action = sorted(list(self.gra_prime.terminals)) + ['#']
        self.goto = sorted(list(self.gra_prime.nonterminals - {self.gra_prime.start_symbol}))
        self.parse_table_symbols = self.action + self.goto
        self.parse_table = self.LR1_construct_table()
        # self.print_table()

    def get_first_and_follow(self, gra: Grammar):
        def union(set_1, set_2):
            set_1_len = len(set_1)
            set_1 |= set_2
            return set_1_len != len(set_1)

        first = {symbol: set() for symbol in gra.symbols}
        first.update((terminal, {terminal}) for terminal in gra.terminals)  # first terminal 加入
        follow = {symbol: set() for symbol in gra.nonterminals}
        follow[gra.start_symbol].add('#')
        while True:
            updated = False
            for head, bodies in gra.grammar.items():
                for body in bodies:
                    for symbol in body:
                        if symbol != '^':
                            updated |= union(first[head], first[symbol] - set('^'))
                            if '^' not in first[symbol]:
                                break
                        else:
                            updated |= union(first[head], set('^'))
                    else:
                        updated |= union(first[head], set('^'))
                    aux = follow[head]
                    for symbol in reversed(body):
                        if symbol == '^':
                            continue
                        if symbol in follow:
                            updated |= union(follow[symbol], aux - set('^'))
                        if '^' in first[symbol]:
                            aux = aux | first[symbol]
                        else:
                            aux = first[symbol]
            if not updated:
                return first, follow

    def construct_follow(self, s: tuple, extra: str) -> set:
        """求LR1向前搜索符"""
        ret = set()
        flag = True
        for x in s:
            ret = ret | self.first[x]
            if '^' not in self.first[x]:
                flag = False
                break
        ret.discard('^')
        if flag:
            ret = ret | {extra}
        return ret

    def LR1_closure(self, dict_of_trans: dict) -> dict:
        ret = dict_of_trans
        while True:
            item_len = len(ret)
            for head, bodies in dict_of_trans.copy().items():
                for body in bodies.copy():
                    if '.' in body[:-1]:  # .在产生式中并且不是最后一个元素
                        symbol_after_dot = body[body.index('.') + 1]
                        if symbol_after_dot in self.gra_prime.nonterminals:  # .后是非终结符
                            symbol_need_first_loc = body.index('.') + 2
                            if symbol_need_first_loc == len(body):  # .后是产生式最后一个元素
                                # 处理A -> ... .B的情况
                                for gra_body in self.gra_prime.grammar[symbol_after_dot]:
                                    # ret.setdefault((symbol_after_dot, head[1]), set()).add( ('.',) if gra_body == ('^',) else ('.',) + gra_body)
                                    # 准备一个键，由点后的符号和原始项的查找符号组成
                                    key = (symbol_after_dot, head[1])
                                    # 检查 ret 字典中是否已经存在该键
                                    if key not in ret:
                                        ret[key] = set()
                                    # 根据 gra_body 的值构建新的产生式
                                    new_production = None
                                    if gra_body == ('^',):  # gra_body是空产生式
                                        new_production = ('.',)
                                    else:  # gra_body不是空产生式，在其开头添加点 '.'
                                        new_production = ('.',) + gra_body
                                    # 将新的产生式添加集合中
                                    ret[key].add(new_production)

                            else:
                                # 处理A -> ... .BC的情况
                                for j in self.construct_follow(body[symbol_need_first_loc:], head[1]):
                                    for gra_body in self.gra_prime.grammar[symbol_after_dot]:
                                        # ret.setdefault((symbol_after_dot, j), set()).add( ('.',) if gra_body == ('^',) else ('.',) + gra_body)
                                        # 准备一个键，由点后的符号和原始项的查找符号组成
                                        key = (symbol_after_dot, j)
                                        # 检查 ret 字典中是否已经存在该键
                                        if key not in ret:
                                            ret[key] = set()
                                        # 根据 gra_body 的值构建新的产生式
                                        new_production = None
                                        if gra_body == ('^',):  # gra_body是空产生式
                                            new_production = ('.',)
                                        else:  # gra_body不是空产生式，在其开头添加点 '.'
                                            new_production = ('.',) + gra_body
                                        # 将新的产生式添加集合中
                                        ret[key].add(new_production)

            # 闭包不再发生变化，则说明闭包已经求出
            if item_len == len(ret):
                break
        return ret

    def LR1_GOTO(self, state: dict, c: str) -> dict:
        goto = {}
        for head, bodies in state.items():
            for body in bodies:
                if '.' in body[:-1]:  # .在产生式中且不是最后一个元素
                    dot_pos = body.index('.')
                    if body[dot_pos + 1] == c:  # 如果.后的元素是c
                        replaced_dot_body = body[:dot_pos] + (c, '.') + body[dot_pos + 2:]  # 把.从c前移到c后
                        for C_head, C_bodies in self.LR1_closure({head: {replaced_dot_body}}).items():
                            goto.setdefault(C_head, set()).update(C_bodies)

        return goto

    # 构建项目集规范族
    def LR1_items(self, gra_prime):
        start_item = {(gra_prime.start_symbol, '#'): {('.', gra_prime.start_symbol[:-1])}}
        C = [self.LR1_closure(start_item)]  # 求 I0 的闭包
        while True:
            flag_len = len(C)
            for item in C.copy():
                for X in gra_prime.symbols:
                    goto = self.LR1_GOTO(item, X)
                    if goto and goto not in C:
                        C.append(goto)
            if flag_len == len(C):  # 如果没有产生新的式子，则表示已经构建完毕
                return C

    # 构建解析表
    def LR1_construct_table(self):
        # 初始化解析表，表格中的每个条目都为空字符串
        parse_table = {r: {c: '' for c in self.parse_table_symbols} for r in range(len(self.Collection))}
        # 遍历每个项集合每个产生式
        for i, I in enumerate(self.Collection):
            for head, bodies in I.items():
                for body in bodies:
                    # CASE 2 a: 如果点 '.' 不在产生式的末尾
                    if '.' in body[:-1]:
                        # 获取点后的符号
                        symbol_after_dot = body[body.index('.') + 1]
                        # 如果点后的符号是终结符
                        if symbol_after_dot in self.gra_prime.terminals:
                            # 计算移入操作并更新解析表
                            s = f's{self.Collection.index(self.LR1_GOTO(I, symbol_after_dot))}'
                            # 如果该条目还未被占用，则添加移入操作
                            if s not in parse_table[i][symbol_after_dot]:
                                if 'r' in parse_table[i][symbol_after_dot]:
                                    parse_table[i][symbol_after_dot] += '/'
                                parse_table[i][symbol_after_dot] += s

                    # CASE 2 b: 如果点 '.' 在产生式末尾且不是增广文法的开始符号
                    elif body[-1] == '.' and head[0] != self.gra_prime.start_symbol:
                        # 遍历文法的每个产生式
                        for j, (gra_head, gra_body) in enumerate(self.gra_indexed):
                            # 如果找到匹配的产生式
                            if gra_head == head[0] and (gra_body == body[:-1] or gra_body == ('^',) and body == ('.',)):
                                # 如果该条目还未被占用，则添加规约操作
                                if parse_table[i][head[1]]:
                                    print("conflict！！！")
                                    # exit(-1)  # 如果该条目已被占用，则退出（存在冲突）
                                    parse_table[i][head[1]] += '/'
                                parse_table[i][head[1]] += f'r{j}'
                                # print(f'({i}, {head[1]}): ', parse_table[i][head[1]])
                                # print(self.gra_indexed[j])
                                break

                    # CASE 2 c: 接受条件，当点 '.' 在增广文法的开始符号的产生式末尾
                    else:
                        parse_table[i]['#'] = 'acc'

            # CASE 3: 处理非终结符的跳转
            for A in self.gra_prime.nonterminals:
                j = self.LR1_GOTO(I, A)
                # 如果跳转目标存在于项集合中，则更新解析表
                if j in self.Collection:
                    parse_table[i][A] = self.Collection.index(j)

        return parse_table

    def print_first_and_follow(self):
        print("First:")
        for i in self.first:
            print(f'\'{i}\': {self.first[i]}')
        print("\nFollow:")
        for i in self.follow:
            print(f'\'{i}\': {self.follow[i]}')

    def print_collections(self):
        """打印项目集规范族"""
        print("\nCollections:")
        for i in range(len(self.Collection)):  # Ii
            print(f'I{i}:')
            for j in self.Collection[i]:
                print(f'{j}: {self.Collection[i][j]}')

    def print_table(self):
        for r in self.parse_table:
            print(f'\n{r}: ', end="")
            for c in self.parse_table[r]:
                if self.parse_table[r][c]:
                    print(f'\'{c}\':{self.parse_table[r][c]}', end=" ")


if __name__ == '__main__':
    grammar_str = open('grammars/grammar4.pl0').read()
    #
    grammar = Grammar(grammar_str)
    print(grammar)
    print()

    table = LR1Table(grammar)

    table.print_first_and_follow()
    table.print_collections()
    table.print_table()