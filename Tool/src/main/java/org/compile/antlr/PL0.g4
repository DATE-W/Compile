grammar PL0;
@header { package org.compile; }

program: programHeader subprog EOF;
programHeader: 'PROGRAM' identifier;
subprog: (constStatement)? (variableStatement)? compoundStatement;
constStatement: 'CONST' constDefinition (',' constDefinition)* ';';
constDefinition: identifier '=' unsignedInteger;
variableStatement: 'VAR' identifier (',' identifier)* ';';

compoundStatement: 'BEGIN' statement (';' statement)* 'END';
statement: assignmentStatement
         | ifStatement
         | whileStatement
         | compoundStatement
         | emptyStatement;
emptyStatement:;
assignmentStatement: identifier ':=' expression;
ifStatement: 'IF' condition 'THEN' statement;
whileStatement: 'WHILE' condition 'DO' statement;
condition: expression relationalOperator expression;

relationalOperator: '=' | '<>' | '<' | '<=' | '>' | '>=';
plusOperator: '+' | '-';
mulOperator: '*' | '/';

expression: (plusOperator)? item (plusOperator item)*;
item: factor (mulOperator factor)*;
factor: identifier | unsignedInteger | '(' expression ')';

unsignedInteger: DIGIT+;
identifier: LETTER (LETTER | DIGIT)*;
LETTER: [a-zA-Z];
DIGIT: [0-9];
WS: [ \t\r\n]+ -> skip;
