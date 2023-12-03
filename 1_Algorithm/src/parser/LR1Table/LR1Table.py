from collections import defaultdict

from src.parser.LR1Table.Grammar import Grammar


# def union(set_1, set_2):
#     """将后者并入前者，若前者改变则返回True"""
#     set_1_len = len(set_1)
#     set_1 |= set_2
#     return set_1_len != len(set_1)

def FIRST(Gra: Grammar):
    first_sets = defaultdict(set)

    def first(symbol):
        # if symbol in Gra.terminals:  # 终结符
        #     return {symbol}
        if symbol in first_sets:  # 已经计算过
            return first_sets[symbol]

        if symbol in Gra.terminals:  # 终结符
            first_sets[symbol] = {symbol}
            return {symbol}

        first_set = set()
        for production in Gra.grammar[symbol]:
            if production == ('^',):  # 空
                first_set.add('^')
            else:
                for sym in production:
                    sym_first_set = first(sym)
                    first_set.update(sym_first_set - {'^'})
                    if '^' not in sym_first_set:  # 如果非终结符FIRST集有空字，则继续循环看下一个字符
                        break
                else:
                    first_set.add('^')
        first_sets[symbol] = first_set

        return first_set

    for symbol in Gra.grammar:
        first(symbol)

    return dict(first_sets)


def FOLLOW(Gra: Grammar):
    first_sets = FIRST(Gra)
    follow_sets = defaultdict(set)
    follow_sets[Gra.start_symbol].add('#')

    while True:
        updated = False
        for head, bodies in Gra.grammar.items():
            for body in bodies:
                follow = set(follow_sets[head])
                for symbol in reversed(body):
                    if symbol in Gra.nonterminals:  # 非终结符
                        previous_follow = follow_sets[symbol].copy()  # 记录原有的FOLLOW集
                        follow_sets[symbol].update(follow - {'^'})  # 更新
                        if '^' in first_sets[symbol]:  # 最后的非终结符推出空，往前继续
                            follow = follow.union(first_sets[symbol]) - {'^'}  # 从后往前每一个可能为空的非终结符
                        else:
                            follow = first_sets[symbol]
                        if previous_follow != follow_sets[symbol]:
                            updated = True
                    else:  # 终结符直接加入FOLLOW
                        follow = {symbol}

        if not updated:
            break  # 没有更新说明FOLLOW已求出

    return dict(follow_sets)




class LR1Table:
    def __init__(self):
        pass

    def getClosure(self):
        pass

    def GOTO(self):
        pass



if __name__ == '__main__':
    grammar_str = open('grammar4.pl0').read()
    #
    grammar = Grammar(grammar_str)
    print(grammar)
    print()

    first = FIRST(grammar)
    print('First:')
    print(first)
    print()

    follow = FOLLOW(grammar)
    print('Follow:')
    print(follow)