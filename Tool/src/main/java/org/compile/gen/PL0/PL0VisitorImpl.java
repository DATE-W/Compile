package org.compile.gen.PL0;

import java.util.HashMap;
import java.util.Map;
import java.util.Stack;

public class PL0VisitorImpl extends PL0BaseVisitor<String> {
    /**
     * 内部类 Code，用于表示四元式代码。
     */
    private class Code {
        String op; // 操作符
        String arg1; // 第一个参数
        String arg2; // 第二个参数
        String result; // 结果
        int line; // 行号

        /**
         * 构造函数
         * @param op 操作符
         * @param arg1 第一个参数
         * @param arg2 第二个参数
         * @param result 结果
         * @param line 行号
         */
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

    // 类成员变量定义
    private int tempCounter = 0; // 用于生成临时变量的计数器
    private int lineCounter = 100; // 当前代码的行号
    private Stack<String> stack = new Stack<>(); // 用于表达式求值的栈
    private Map<String, String> varDict = new HashMap<>(); // 变量字典
    private Map<String, String> constDict = new HashMap<>(); // 常量字典
    private Map<Integer, Code> code = new HashMap<>(); // 存储生成的代码

    /**
     * 生成四元式代码并将其添加到代码列表中。
     * @param op 操作符
     * @param arg1 第一个参数
     * @param arg2 第二个参数
     * @param result 结果
     */
    private void emit(String op, String arg1, String arg2, String result) {
        code.put(lineCounter, new Code(op, arg1, arg2, result, lineCounter));
        lineCounter++;
    }

    /**
     * 生成新的临时变量。
     * @return 生成的临时变量名称。
     */
    private String newTemp() {
        return "t" + (tempCounter++);
    }

    /**
     * 获取生成的代码的字符串表示。
     * @return 代码的字符串表示。
     */
    public String getCodeString() {
        StringBuilder sb = new StringBuilder();
        for (Code c : code.values()) {
            sb.append(c.toString()).append("\n");
        }
        return sb.toString();
    }

    /**
     * 向变量字典中添加新变量。
     * @param name 变量名称
     */
    private void addVar(String name) {
        if (varDict.containsKey(name) || constDict.containsKey(name)) {
            throw new RuntimeException("变量重定义：" + name);
        }
        varDict.put(name, "");
    }

    /**
     * 更新变量的值。
     * @param name 变量名称
     * @param value 变量的值
     */
    private void updateVar(String name, String value) throws RuntimeException {
        if (!varDict.containsKey(name)) {
            if (constDict.containsKey(name)) {
                throw new RuntimeException("无法给常量赋值：" + name);
            } else {
                throw new RuntimeException("未找到变量：" + name);
            }
        }
        varDict.put(name, value);
    }

    /**
     * 向常量字典中添加新常量。
     * @param name 常量名称
     * @param value 常量的值
     */
    private void addConst(String name, String value) throws RuntimeException {
        if (constDict.containsKey(name) || varDict.containsKey(name)) {
            throw new RuntimeException("常量重定义：" + name);
        }
        constDict.put(name, value);
    }

    public void printSymbolTable() {
        System.out.println("符号表:");
        for (String key : constDict.keySet()) {
            System.out.println("SymbolTable: { name: " + key + ", type: const, value: " + constDict.get(key) + "}");
        }
        for (String key : varDict.keySet()) {
            System.out.println("SymbolTable: { name: " + key + ", type: var}");
        }
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
        updateVar(id,expr);
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