Parser — py-tree-sitter 0.25.2 documentation



[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

[![py-tree-sitter 0.25.2 documentation - Home](../_static/logo.png)](../index.html)

# Parser

## Contents

# Parser[#](#parser "Link to this heading")

*class* tree\_sitter.Parser(*language*, *\**, *included\_ranges=None*, *timeout\_micros=None*)[#](#tree_sitter.Parser "Link to this definition")
:   A class that is used to produce a [`Tree`](tree_sitter.Tree.html#tree_sitter.Tree "tree_sitter.Tree") based on some source code.

    ## Methods[#](#methods "Link to this heading")

    parse(*source*, */*, *old\_tree=None*, *encoding='utf8'*)[#](#tree_sitter.Parser.parse "Link to this definition")
    :   Parse a slice of a bytestring or bytes provided in chunks by a callback.

        The callback function takes a byte offset and position and returns a bytestring starting at that offset and position. The slices can be of any length. If the given position is at the end of the text, the callback should return an empty slice.

        Returns:
        :   A [`Tree`](tree_sitter.Tree.html#tree_sitter.Tree "tree_sitter.Tree") if parsing succeeded or `None` if the parser does not have an assigned language or the timeout expired.

    print\_dot\_graphs(*file*)[#](#tree_sitter.Parser.print_dot_graphs "Link to this definition")
    :   Set the file descriptor to which the parser should write debugging graphs during parsing. The graphs are formatted in the DOT language. You can turn off this logging by passing `None`.

    reset()[#](#tree_sitter.Parser.reset "Link to this definition")
    :   Instruct the parser to start the next parse from the beginning.

        Note

        If the parser previously failed because of a timeout, then by default, it will resume where it left off on the next call to [`parse()`](#tree_sitter.Parser.parse "tree_sitter.Parser.parse").
        If you don’t want to resume, and instead intend to use this parser to parse some other document, you must call [`reset()`](#tree_sitter.Parser.reset "tree_sitter.Parser.reset") first.

    ## Attributes[#](#attributes "Link to this heading")

    included\_ranges[#](#tree_sitter.Parser.included_ranges "Link to this definition")
    :   The ranges of text that the parser will include when parsing.

    language[#](#tree_sitter.Parser.language "Link to this definition")
    :   The language that will be used for parsing.

    logger[#](#tree_sitter.Parser.logger "Link to this definition")
    :   The logger that the parser should use during parsing.

Contents