package org.compile;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.tree.*;
import org.compile.gen.PL0.*;

public class PL0Compile {
    public static void main(String[] args) throws Exception {
        // 假设args[0]是PL/0源代码文件的路径
        CharStream input = CharStreams.fromFileName("D:\\sthgithub\\Compile\\Tool\\src\\main\\java\\org\\compile\\in\\test.pl0");

        // 使用ANTLR生成的词法分析器和语法分析器
        PL0Lexer lexer = new PL0Lexer(input);
        CommonTokenStream tokens = new CommonTokenStream(lexer);
        PL0Parser parser = new PL0Parser(tokens);
        parser.setBuildParseTree(true);
        PL0Parser.ProgramContext tree = parser.program();
        PL0BaseVisitor<String> visitor = new PL0VisitorImpl();
        visitor.visit(tree);
        System.out.println(((PL0VisitorImpl) visitor).getCodeString());

        System.out.println("解析完成");
    }
}