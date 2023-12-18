from src.parser.Token import token_dict


class Grammar:
    def __init__(self, grammar_str):
        self.grammar = {}
        self.grammar_str = grammar_str
        self.terminals = set()
        self.nonterminals = set()
        self.start_symbol = None  # S'
        self.grammar_str_list = list(filter(None, grammar_str.splitlines()))

        for s in self.grammar_str_list:
            head, _, bodies = s.partition(' -> ')
            # if not head.isupper():
            #     raise ValueError(f'\'{head} -> {bodies}\': Head \'{head}\' is not capitalized to be treated as a nonterminal.')
            if not self.start_symbol:
                self.start_symbol = head
            self.grammar.setdefault(head, [])
            self.nonterminals.add(head)
            bodies = [tuple(body.split()) for body in ' '.join(bodies.split()).split('|')]

            for body in bodies:
                if '^' in body and body != ('^',):
                    raise ValueError(f'\'{head} -> {" ".join(body)}\': Null symbol \'^\' is not allowed here.')
                self.grammar[head].append(body)
                for symbol in body:
                    # if not symbol.isupper() and symbol != '^':
                    if token_dict[symbol] and symbol != '^':
                        self.terminals.add(symbol)
                    # elif symbol.isupper():
                    elif not token_dict[symbol]:
                        self.nonterminals.add(symbol)
        self.symbols = self.terminals | self.nonterminals

    def __str__(self):
        return f'grammar:{self.grammar}\nterminals:{self.terminals}\nnonterminals:{self.nonterminals}\nstart:{self.start_symbol}'


if __name__ == '__main__':
    grammar_str = open('grammars/grammar.pl0').read()
    print(Grammar(grammar_str))