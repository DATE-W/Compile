package org.compile;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.tree.*;
import org.compile.gen.PL0.*;

import java.io.FileNotFoundException;
import java.io.IOException;

public class PL0Compile {
    public static void main(String[] args) throws Exception {
        try {
            CharStream input = CharStreams.fromFileName("src/main/java/org/compile/in/test.pl0");
            // 使用ANTLR生成的词法分析器和语法分析器
            PL0Lexer lexer = new PL0Lexer(input);
            CommonTokenStream tokens = new CommonTokenStream(lexer);
            PL0Parser parser = new PL0Parser(tokens);
            parser.setBuildParseTree(true);
            PL0Parser.ProgramContext tree = parser.program();
            PL0VisitorImpl visitor = new PL0VisitorImpl();
            visitor.visit(tree);
            System.out.println(visitor.getCodeString());

            System.out.println("解析完成");
        } catch (FileNotFoundException e) {
            System.err.println("文件未找到: " + e.getMessage());
        } catch (IOException e) {
            System.err.println("读取文件时发生错误: " + e.getMessage());
        }
    }
}