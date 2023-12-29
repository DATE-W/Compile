package org.compile.gen.PL0;

import java.util.HashMap;
import java.util.Map;
import java.util.Stack;

public class PL0VisitorImpl extends PL0BaseVisitor<String> {
    private class Code {
        String op;
        String arg1;
        String arg2;
        String result;
        int line;

        public Code(String op, String arg1, String arg2, String result, int line) {
            this.op = op;
            this.arg1 = arg1;
            this.arg2 = arg2;
            this.result = result;
            this.line = line;
        }

        @Override
        public String toString() {
            return line + ": (" + op + ", " + (arg1 != null ? arg1 : "-") + ", " + (arg2 != null ? arg2 : "-") + ", " + result + ")";
        }
    }

    private int tempCounter = 0;        // 中间变量数量
    private int lineCounter = 100;      // 总行数
    private Stack<String> stack = new Stack<>();
    private Map<String, String> varDict = new HashMap<>();
    private Map<String, String> constDict = new HashMap<>();
    private Stack<Integer> whileStack = new Stack<>();      // 记录循环开始的行和需要回填的行
    private Stack<Integer> ifStack = new Stack<>();         // 记录需要回填的行
    private Map<Integer, Code> code = new HashMap<>();

    private void emit(String op, String arg1, String arg2, String result) {
        code.put(lineCounter, new Code(op, arg1, arg2, result, lineCounter));
        lineCounter++;
    }

    private String newTemp() {
        return "t" + (tempCounter++);
    }

    public String getCodeString() {
        StringBuilder sb = new StringBuilder();
        for (Code c : code.values()) {
            sb.append(c.toString()).append("\n");
        }
        return sb.toString();
    }

    private void addVar(String name) {
        if (varDict.containsKey(name)) {
            throw new RuntimeException("Redefinition in var " + name);
        }
        varDict.put(name, "");
    }

    private void updateVar(String name, String value) throws RuntimeException {
        if (!varDict.containsKey(name)) {
            if (constDict.containsKey(name)) {
                throw new RuntimeException("Cannot assign const " + name);
            } else {
                throw new RuntimeException("NotFound var " + name);
            }
        }
        varDict.put(name, value);
    }

    private void addConst(String name, String value) throws RuntimeException {
        if (constDict.containsKey(name)) {
            throw new RuntimeException("Redefinition in const " + name);
        }
        constDict.put(name, value);
    }

    @Override
    public String visitProgram(PL0Parser.ProgramContext ctx) {
        // 访问子节点
        visitChildren(ctx);
        return null;
    }

    @Override
    public String visitProgramHeader(PL0Parser.ProgramHeaderContext ctx) {
        // 处理程序头部
        String programName = ctx.identifier().getText();
        System.out.println("Program Name: " + programName);
        return null;
    }

    @Override
    public String visitSubprog(PL0Parser.SubprogContext ctx) {
        // 处理子程序
        visitChildren(ctx);
        return null;
    }


    @Override
    public String visitConstStatement(PL0Parser.ConstStatementContext ctx) {
        // 访问所有常量声明
        for (PL0Parser.ConstDefinitionContext constDef : ctx.constDefinition()) {
            visitConstDefinition(constDef);
        }
        return null;
    }

    @Override
    public String visitConstDefinition(PL0Parser.ConstDefinitionContext ctx) {
        // 处理常量定义
        String constName = ctx.identifier().getText();
        String constValue = ctx.unsignedInteger().getText();
        addConst(constName, constValue);
        emit(":=", constValue, "-", constName);
        return null;
    }

    @Override
    public String visitVariableStatement(PL0Parser.VariableStatementContext ctx) {
        // 处理变量声明
        for (PL0Parser.IdentifierContext idCtx : ctx.identifier()) {
            String varName = idCtx.getText();
            addVar(varName);
        }
        return null;
    }

    @Override
    public String visitCompoundStatement(PL0Parser.CompoundStatementContext ctx) {
        // 访问复合语句中的所有语句
        for (PL0Parser.StatementContext stmtCtx : ctx.statement()) {
            visitStatement(stmtCtx);
        }
        return null;
    }

    @Override
    public String visitAssignmentStatement(PL0Parser.AssignmentStatementContext ctx) {
        String id = visit(ctx.identifier());
        String expr = visit(ctx.expression());
        emit(":=", expr, "-", id);
        return null;
    }

    @Override
    public String visitIfStatement(PL0Parser.IfStatementContext ctx) {
        visitCondition(ctx.condition());
        int ifExitLine = lineCounter;
        emit("j", "-", "-", "-"); // 占位符
        visit(ctx.statement());
        code.get(ifExitLine).result = String.valueOf(lineCounter);
        return null;
    }

    @Override
    public String visitWhileStatement(PL0Parser.WhileStatementContext ctx) {
        int startLine = lineCounter;
        visitCondition(ctx.condition());
        int exitLine = lineCounter;
        emit("j", "-", "-", "-"); // 占位符
        visit(ctx.statement());
        emit("j", "-", "-", String.valueOf(startLine));
        code.get(exitLine).result = String.valueOf(lineCounter);
        return null;
    }

    @Override
    public String visitCondition(PL0Parser.ConditionContext ctx) {
        String left = visit(ctx.expression(0));
        String right = visit(ctx.expression(1));
        String op = visitRelationalOperator(ctx.relationalOperator());
        int nextLine = lineCounter + 2;
        emit("j" + op, left, right, String.valueOf(nextLine));
        return null;
    }

    @Override
    public String visitRelationalOperator(PL0Parser.RelationalOperatorContext ctx) {
        // 返回关系运算符
        return ctx.getText();
    }

    @Override
    public String visitPlusOperator(PL0Parser.PlusOperatorContext ctx) {
        // 返回加法或减法运算符
        return ctx.getText();
    }

    @Override
    public String visitMulOperator(PL0Parser.MulOperatorContext ctx) {
        // 返回乘法或除法运算符
        return ctx.getText();
    }


    @Override
    public String visitExpression(PL0Parser.ExpressionContext ctx) {
        // 确认是否是二元表达式
        if (ctx.children.size() > 1) {
            String left = visit(ctx.getChild(0)); // 访问左侧表达式
            String op = ctx.getChild(1).getText(); // 获取操作符
            String right = visit(ctx.getChild(2)); // 访问右侧表达式

            if (op.equals("+") || op.equals("-")) {
                String tempVar = newTemp(); // 为表达式创建一个临时变量
                emit(op, left, right, tempVar); // 生成四元式中间代码
                return tempVar; // 返回临时变量作为表达式的结果
            }
        }
        // 如果不是二元表达式，直接访问子节点
        return visitChildren(ctx);
    }

    @Override
    public String visitItem(PL0Parser.ItemContext ctx) {
        // 类似于 visitExpression 的逻辑，但用于处理乘除
        if (ctx.children.size() > 1) {
            String left = visit(ctx.getChild(0));
            String op = ctx.getChild(1).getText();
            String right = visit(ctx.getChild(2));

            if (op.equals("*") || op.equals("/")) {
                String tempVar = newTemp();
                emit(op, left, right, tempVar);
                return tempVar;
            }
        }
        return visitChildren(ctx);
    }

    @Override
    public String visitFactor(PL0Parser.FactorContext ctx) {
        // 处理基础因子，例如数字和标识符
        return visitChildren(ctx);
    }

    @Override
    public String visitUnsignedInteger(PL0Parser.UnsignedIntegerContext ctx) {
        String value = ctx.getText();
        stack.push(value);
        return value;
    }

    @Override
    public String visitIdentifier(PL0Parser.IdentifierContext ctx) {
        String id = ctx.getText();
        stack.push(id);
        return id;
    }
}