### 求FIRST集和FOLLOW集

```java
def first_follow(G):
    def union(set_1, set_2):
        set_1_len = len(set_1)
        set_1 |= set_2
        return set_1_len != len(set_1)
    first = {symbol: set() for symbol in G.symbols}
    first.update((terminal, {terminal}) for terminal in G.terminals)  # first terminal 加入
    follow = {symbol: set() for symbol in G.nonterminals}
    follow[G.start_symbol].add('.')
    while True:
        updated = False
        for head, bodies in G.grammar.items():
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

```

这段代码实现了 FIRST 和 FOLLOW 集合的计算，但它本身并不解决左递归问题。左递归发生在语法规则中，当一个非终结符直接或间接地引用自身作为其产生式的一部分时。这段代码没有修改或重写语法规则，因此不能消除或处理左递归。它只是用于计算 FIRST 和 FOLLOW 集合，这是构建解析表（如 LL 或 LR 表）的一部分。

这段代码的主要功能如下：

1. **初始化 FIRST 集合**：对于文法中的每个符号，创建一个空集合。对于每个终结符，将其自身加入到其 FIRST 集合中。

2. **初始化 FOLLOW 集合**：对于文法中的每个非终结符，创建一个空集合。对于开始符号，将特殊符号 `'.'`（表示输入结束）加入到其 FOLLOW 集合中。

3. **计算 FIRST 集合**：
   - 遍历文法中的每个产生式。
   - 对于产生式中的每个符号，如果该符号不是空字符（`'^'`），将该符号的 FIRST 集合（不包括空字符）加入到产生式头部符号的 FIRST 集合中。如果该符号的 FIRST 集合不包含空字符，则停止处理当前产生式。
   - **无论是否存在左递归**，计算一个非终结符的 FIRST 集合时，只关注从该非终结符开始可能导出的终结符集合，因此左递归不会影响 FIRST 集合的计算。
   
4. **计算 FOLLOW 集合**：
   - 逆向遍历产生式中的符号。
   - 如果符号是非终结符，将 FOLLOW 集合中的符号加入到该符号的 FOLLOW 集合中。如果该符号的 FIRST 集合包含空字符，则将后续符号的 FIRST 集合（不包括空字符）也加入到该符号的 FOLLOW 集合中。
   - **无论是否存在左递归**，FOLLOW 集合的计算依赖于找出所有可能紧跟在非终结符之后的终结符。左递归不会影响这个过程，因为 FOLLOW 集合的计算是通过查看产生式中的符号位置关系来实现的，而不依赖于产生式是否递归。
   
5. **重复计算**：重复上述过程，直到 FIRST 和 FOLLOW 集合不再发生变化。

解决左递归问题通常涉及重写或重新排列语法规则，以消除对同一非终结符的直接或间接递归调用。例如，通过引入新的非终结符和产生式，或者通过将左递归规则转换为右递归规则来解决。这个过程通常在构建语法分析器之前进行，以确保语法分析器能正确地处理输入。