// Generated from D:/sthgithub/Compile/Tool/src/main/java/org/compile/antlr/PL0.g4 by ANTLR 4.13.1
package org.compile.gen.PL0;
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link PL0Parser}.
 */
public interface PL0Listener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link PL0Parser#program}.
	 * @param ctx the parse tree
	 */
	void enterProgram(PL0Parser.ProgramContext ctx);
	/**
	 * Exit a parse tree produced by {@link PL0Parser#program}.
	 * @param ctx the parse tree
	 */
	void exitProgram(PL0Parser.ProgramContext ctx);
	/**
	 * Enter a parse tree produced by {@link PL0Parser#programHeader}.
	 * @param ctx the parse tree
	 */
	void enterProgramHeader(PL0Parser.ProgramHeaderContext ctx);
	/**
	 * Exit a parse tree produced by {@link PL0Parser#programHeader}.
	 * @param ctx the parse tree
	 */
	void exitProgramHeader(PL0Parser.ProgramHeaderContext ctx);
	/**
	 * Enter a parse tree produced by {@link PL0Parser#subprog}.
	 * @param ctx the parse tree
	 */
	void enterSubprog(PL0Parser.SubprogContext ctx);
	/**
	 * Exit a parse tree produced by {@link PL0Parser#subprog}.
	 * @param ctx the parse tree
	 */
	void exitSubprog(PL0Parser.SubprogContext ctx);
	/**
	 * Enter a parse tree produced by {@link PL0Parser#constStatement}.
	 * @param ctx the parse tree
	 */
	void enterConstStatement(PL0Parser.ConstStatementContext ctx);
	/**
	 * Exit a parse tree produced by {@link PL0Parser#constStatement}.
	 * @param ctx the parse tree
	 */
	void exitConstStatement(PL0Parser.ConstStatementContext ctx);
	/**
	 * Enter a parse tree produced by {@link PL0Parser#constDefinition}.
	 * @param ctx the parse tree
	 */
	void enterConstDefinition(PL0Parser.ConstDefinitionContext ctx);
	/**
	 * Exit a parse tree produced by {@link PL0Parser#constDefinition}.
	 * @param ctx the parse tree
	 */
	void exitConstDefinition(PL0Parser.ConstDefinitionContext ctx);
	/**
	 * Enter a parse tree produced by {@link PL0Parser#variableStatement}.
	 * @param ctx the parse tree
	 */
	void enterVariableStatement(PL0Parser.VariableStatementContext ctx);
	/**
	 * Exit a parse tree produced by {@link PL0Parser#variableStatement}.
	 * @param ctx the parse tree
	 */
	void exitVariableStatement(PL0Parser.VariableStatementContext ctx);
	/**
	 * Enter a parse tree produced by {@link PL0Parser#compoundStatement}.
	 * @param ctx the parse tree
	 */
	void enterCompoundStatement(PL0Parser.CompoundStatementContext ctx);
	/**
	 * Exit a parse tree produced by {@link PL0Parser#compoundStatement}.
	 * @param ctx the parse tree
	 */
	void exitCompoundStatement(PL0Parser.CompoundStatementContext ctx);
	/**
	 * Enter a parse tree produced by {@link PL0Parser#statement}.
	 * @param ctx the parse tree
	 */
	void enterStatement(PL0Parser.StatementContext ctx);
	/**
	 * Exit a parse tree produced by {@link PL0Parser#statement}.
	 * @param ctx the parse tree
	 */
	void exitStatement(PL0Parser.StatementContext ctx);
	/**
	 * Enter a parse tree produced by {@link PL0Parser#emptyStatement}.
	 * @param ctx the parse tree
	 */
	void enterEmptyStatement(PL0Parser.EmptyStatementContext ctx);
	/**
	 * Exit a parse tree produced by {@link PL0Parser#emptyStatement}.
	 * @param ctx the parse tree
	 */
	void exitEmptyStatement(PL0Parser.EmptyStatementContext ctx);
	/**
	 * Enter a parse tree produced by {@link PL0Parser#assignmentStatement}.
	 * @param ctx the parse tree
	 */
	void enterAssignmentStatement(PL0Parser.AssignmentStatementContext ctx);
	/**
	 * Exit a parse tree produced by {@link PL0Parser#assignmentStatement}.
	 * @param ctx the parse tree
	 */
	void exitAssignmentStatement(PL0Parser.AssignmentStatementContext ctx);
	/**
	 * Enter a parse tree produced by {@link PL0Parser#ifStatement}.
	 * @param ctx the parse tree
	 */
	void enterIfStatement(PL0Parser.IfStatementContext ctx);
	/**
	 * Exit a parse tree produced by {@link PL0Parser#ifStatement}.
	 * @param ctx the parse tree
	 */
	void exitIfStatement(PL0Parser.IfStatementContext ctx);
	/**
	 * Enter a parse tree produced by {@link PL0Parser#whileStatement}.
	 * @param ctx the parse tree
	 */
	void enterWhileStatement(PL0Parser.WhileStatementContext ctx);
	/**
	 * Exit a parse tree produced by {@link PL0Parser#whileStatement}.
	 * @param ctx the parse tree
	 */
	void exitWhileStatement(PL0Parser.WhileStatementContext ctx);
	/**
	 * Enter a parse tree produced by {@link PL0Parser#condition}.
	 * @param ctx the parse tree
	 */
	void enterCondition(PL0Parser.ConditionContext ctx);
	/**
	 * Exit a parse tree produced by {@link PL0Parser#condition}.
	 * @param ctx the parse tree
	 */
	void exitCondition(PL0Parser.ConditionContext ctx);
	/**
	 * Enter a parse tree produced by {@link PL0Parser#relationalOperator}.
	 * @param ctx the parse tree
	 */
	void enterRelationalOperator(PL0Parser.RelationalOperatorContext ctx);
	/**
	 * Exit a parse tree produced by {@link PL0Parser#relationalOperator}.
	 * @param ctx the parse tree
	 */
	void exitRelationalOperator(PL0Parser.RelationalOperatorContext ctx);
	/**
	 * Enter a parse tree produced by {@link PL0Parser#plusOperator}.
	 * @param ctx the parse tree
	 */
	void enterPlusOperator(PL0Parser.PlusOperatorContext ctx);
	/**
	 * Exit a parse tree produced by {@link PL0Parser#plusOperator}.
	 * @param ctx the parse tree
	 */
	void exitPlusOperator(PL0Parser.PlusOperatorContext ctx);
	/**
	 * Enter a parse tree produced by {@link PL0Parser#mulOperator}.
	 * @param ctx the parse tree
	 */
	void enterMulOperator(PL0Parser.MulOperatorContext ctx);
	/**
	 * Exit a parse tree produced by {@link PL0Parser#mulOperator}.
	 * @param ctx the parse tree
	 */
	void exitMulOperator(PL0Parser.MulOperatorContext ctx);
	/**
	 * Enter a parse tree produced by {@link PL0Parser#expression}.
	 * @param ctx the parse tree
	 */
	void enterExpression(PL0Parser.ExpressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link PL0Parser#expression}.
	 * @param ctx the parse tree
	 */
	void exitExpression(PL0Parser.ExpressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link PL0Parser#item}.
	 * @param ctx the parse tree
	 */
	void enterItem(PL0Parser.ItemContext ctx);
	/**
	 * Exit a parse tree produced by {@link PL0Parser#item}.
	 * @param ctx the parse tree
	 */
	void exitItem(PL0Parser.ItemContext ctx);
	/**
	 * Enter a parse tree produced by {@link PL0Parser#factor}.
	 * @param ctx the parse tree
	 */
	void enterFactor(PL0Parser.FactorContext ctx);
	/**
	 * Exit a parse tree produced by {@link PL0Parser#factor}.
	 * @param ctx the parse tree
	 */
	void exitFactor(PL0Parser.FactorContext ctx);
	/**
	 * Enter a parse tree produced by {@link PL0Parser#unsignedInteger}.
	 * @param ctx the parse tree
	 */
	void enterUnsignedInteger(PL0Parser.UnsignedIntegerContext ctx);
	/**
	 * Exit a parse tree produced by {@link PL0Parser#unsignedInteger}.
	 * @param ctx the parse tree
	 */
	void exitUnsignedInteger(PL0Parser.UnsignedIntegerContext ctx);
	/**
	 * Enter a parse tree produced by {@link PL0Parser#identifier}.
	 * @param ctx the parse tree
	 */
	void enterIdentifier(PL0Parser.IdentifierContext ctx);
	/**
	 * Exit a parse tree produced by {@link PL0Parser#identifier}.
	 * @param ctx the parse tree
	 */
	void exitIdentifier(PL0Parser.IdentifierContext ctx);
}