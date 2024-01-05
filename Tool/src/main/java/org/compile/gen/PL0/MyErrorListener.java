package org.compile.gen.PL0;

import org.antlr.v4.runtime.*;

public class MyErrorListener extends BaseErrorListener {

    @Override
    public void syntaxError(Recognizer<?, ?> recognizer,
                            Object offendingSymbol,
                            int line, int charPositionInLine,
                            String msg, RecognitionException e) {
        throw new PL0ParseException("错误发生在行 " + line + ":" + charPositionInLine + " - " + msg);
    }
}
