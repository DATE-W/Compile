# NodeVisitor类的完整实现
class NodeVisitor:
    def visit_program(self, node):
        print('Visiting Program Node')
        self.visit(node.block)

    def visit_block(self, node):
        print('Visiting Block Node')
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_var_decl(self, node):
        print('Visiting VarDecl Node')
        self.visit(node.var_node)
        self.visit(node.type_node)

    def visit_type(self, node):
        print('Visiting Type Node with value:', node.value)

    def visit_compound_statement(self, node):
        print('Visiting CompoundStatement Node')
        for child in node.children:
            self.visit(child)

    def visit_assignment(self, node):
        print('Visiting Assignment Node')
        self.visit(node.left)
        self.visit(node.right)

    def visit_var(self, node):
        print('Visiting Var Node with value:', node.value)

    def visit_no_op(self, node):
        print('Visiting NoOp Node')

    def visit_binary_operator(self, node):
        print('Visiting BinaryOperator Node')
        self.visit(node.left)
        print('Operator:', node.token.value)
        self.visit(node.right)

    def visit_number(self, node):
        print('Visiting Number Node with value:', node.value)

    def visit(self, node):
        """如果节点存在，则调用该节点类型的访问方法"""
        if node is not None:
            method_name = 'visit_' + type(node).__name__
            visitor = getattr(self, method_name, self.generic_visit)
            return visitor(node)
        else:
            return self.visit_no_op(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))
