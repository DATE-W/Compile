package org.compile;

import org.antlr.v4.runtime.*;
import org.antlr.v4.gui.TreeViewer;
import org.compile.gen.PL0.PL0Lexer;
import org.compile.gen.PL0.PL0Parser;
import org.compile.gen.PL0.PL0VisitorImpl;
import org.compile.gen.PL0.MyErrorListener;
import org.compile.gen.PL0.PL0ParseException;

import javax.swing.*;
import java.awt.*;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Arrays;

public class PL0Compile {
    public static void main(String[] args) {
        JFileChooser fileChooser = new JFileChooser();
        fileChooser.setCurrentDirectory(new File("./src/main/java/org/compile/in"));
        int result = fileChooser.showOpenDialog(null);

        if (result == JFileChooser.APPROVE_OPTION) {
            File selectedFile = fileChooser.getSelectedFile();
            try {
                CharStream input = CharStreams.fromFileName(selectedFile.getAbsolutePath());
                System.out.println("开始解析文件：" + selectedFile.getName());
                PL0Lexer lexer = new PL0Lexer(input);
                CommonTokenStream tokens = new CommonTokenStream(lexer);
                PL0Parser parser = new PL0Parser(tokens);

                parser.removeErrorListeners();
                parser.addErrorListener(new MyErrorListener());

                parser.setBuildParseTree(true);
                PL0Parser.ProgramContext tree = parser.program();

                TreeViewer viewer = new TreeViewer(Arrays.asList(parser.getRuleNames()), tree);
                viewer.setScale(1.5); // 缩放

                JScrollPane treeScrollPane = new JScrollPane(viewer); // 为语法树创建滚动面板

                PL0VisitorImpl visitor = new PL0VisitorImpl();
                visitor.visit(tree);
                String codeString = visitor.getCodeString();

                // 打印符号表
                visitor.printSymbolTable();

                JTextArea resultTextArea = new JTextArea(codeString); // 为结果创建文本区域
                resultTextArea.setFont(new Font("Monospaced", Font.PLAIN, 16)); // 设置字体大小
                JScrollPane resultScrollPane = new JScrollPane(resultTextArea); // 为结果创建滚动面板

                JTabbedPane tabbedPane = new JTabbedPane(); // 创建选项卡面板
                tabbedPane.addTab("解析结果", resultScrollPane);
                tabbedPane.addTab("语法树", treeScrollPane);

                JFrame frame = new JFrame("PL0 编译器 - " + selectedFile.getName());
                frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                frame.add(tabbedPane); // 将选项卡面板添加到窗口
                frame.setSize(800, 600);
                frame.setMinimumSize(new Dimension(500, 400));
                frame.setVisible(true);

                System.out.println("解析完成");
            } catch (PL0ParseException e) {
                System.err.println("PL0文件解析错误: " + e.getMessage());
            } catch (FileNotFoundException e) {
                System.err.println("文件未找到: " + e.getMessage());
            } catch (IOException e) {
                System.err.println("读取文件时发生错误: " + e.getMessage());
            }
        }
    }
}
