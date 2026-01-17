LookaheadIterator — py-tree-sitter 0.25.2 documentation



[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

[![py-tree-sitter 0.25.2 documentation - Home](../_static/logo.png)](../index.html)

# LookaheadIterator

## Contents

# LookaheadIterator[#](#lookaheaditerator "Link to this heading")

*class* tree\_sitter.LookaheadIterator[#](#tree_sitter.LookaheadIterator "Link to this definition")
:   Bases: [`Iterator`](https://docs.python.org/3.10/library/collections.abc.html#collections.abc.Iterator "(in Python v3.10)")

    A class that is used to look up symbols valid in a specific parse state.

    Tip

    Lookahead iterators can be useful to generate suggestions and improve syntax error diagnostics.

    To get symbols valid in an `ERROR` node, use the lookahead iterator on its first leaf node state.
    For `MISSING` nodes, a lookahead iterator created on the previous non-extra leaf node may be appropriate.

    ## Methods[#](#methods "Link to this heading")

    names()[#](#tree_sitter.LookaheadIterator.names "Link to this definition")
    :   Get a list of all symbol names.

    reset(*state*, *language=None*)[#](#tree_sitter.LookaheadIterator.reset "Link to this definition")
    :   Reset the lookahead iterator.

        Returns:
        :   `True` if it was reset successfully or `False` if it failed.

    symbols()[#](#tree_sitter.LookaheadIterator.symbols "Link to this definition")
    :   Get a list of all symbol IDs.

    ## Special Methods[#](#special-methods "Link to this heading")

    \_\_iter\_\_()[#](#tree_sitter.LookaheadIterator.__iter__ "Link to this definition")
    :   Implements `iter(self)`.

    \_\_next\_\_()[#](#tree_sitter.LookaheadIterator.__next__ "Link to this definition")
    :   Implements `next(self)`.

    ## Attributes[#](#attributes "Link to this heading")

    current\_symbol[#](#tree_sitter.LookaheadIterator.current_symbol "Link to this definition")
    :   The current symbol ID.

        Newly created iterators will return the `ERROR` symbol.

    current\_symbol\_name[#](#tree_sitter.LookaheadIterator.current_symbol_name "Link to this definition")
    :   The current symbol name.

    language[#](#tree_sitter.LookaheadIterator.language "Link to this definition")
    :   The current language.

Contents