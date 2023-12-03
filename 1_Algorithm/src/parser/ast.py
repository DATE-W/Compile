class ASTNode:
    """抽象语法树的基类节点"""
    def accept(self, visitor):
        """接受访问者"""
        pass

class ProgramNode(ASTNode):
    """程序节点，代表整个程序"""
    def __init__(self, block):
        self.block = block

    def accept(self, visitor):
        return visitor.visit_program(self)

class BlockNode(ASTNode):
    """块节点，代表一系列语句"""
    def __init__(self, declarations, compound_statement):
        self.declarations = declarations
        self.compound_statement = compound_statement

    def accept(self, visitor):
        return visitor.visit_block(self)

class VarDeclNode(ASTNode):
    """变量声明节点"""
    def __init__(self, var_node, type_node):
        self.var_node = var_node
        self.type_node = type_node

    def accept(self, visitor):
        return visitor.visit_var_decl(self)

class TypeNode(ASTNode):
    """类型节点，例如整型、浮点型"""
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def accept(self, visitor):
        return visitor.visit_type(self)

class CompoundStatementNode(ASTNode):
    """复合语句节点，包含一系列语句"""
    def __init__(self, children):
        self.children = children

    def accept(self, visitor):
        return visitor.visit_compound_statement(self)

class AssignmentNode(ASTNode):
    """赋值语句节点"""
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def accept(self, visitor):
        return visitor.visit_assignment(self)

class VarNode(ASTNode):
    """变量节点"""
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def accept(self, visitor):
        return visitor.visit_var(self)

class NoOpNode(ASTNode):
    """空操作节点，用于表示空语句或占位"""
    def accept(self, visitor):
        return visitor.visit_no_op(self)

class BinaryOperatorNode(ASTNode):
    """二元操作符节点，例如加法、乘法"""
    def __init__(self, left, token, right):
        self.left = left
        self.token = token
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary_operator(self)

class NumberNode(ASTNode):
    """数字节点"""
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def accept(self, visitor):
        return visitor.visit_number(self)