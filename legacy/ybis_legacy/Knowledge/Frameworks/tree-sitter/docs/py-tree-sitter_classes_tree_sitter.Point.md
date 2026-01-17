Point — py-tree-sitter 0.25.2 documentation



[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

[![py-tree-sitter 0.25.2 documentation - Home](../_static/logo.png)](../index.html)

# Point

## Contents

# Point[#](#point "Link to this heading")

*class* tree\_sitter.Point(*row*, *column*)[#](#tree_sitter.Point "Link to this definition")
:   Bases: [`tuple`](https://docs.python.org/3.10/library/stdtypes.html#tuple "(in Python v3.10)")

    A position in a multi-line text document, in terms of rows and columns.

    ## Methods[#](#methods "Link to this heading")

    edit(*start\_byte*, *old\_end\_byte*, *new\_end\_byte*, *start\_point*, *old\_end\_point*, *new\_end\_point*)[#](#tree_sitter.Point.edit "Link to this definition")
    :   Edit this point to keep it in-sync with source code that has been edited.

        Returns:
        :   *The edited point and its new start byte.*

        Tip

        This is useful for editing points without requiring a tree or node instance.

        Added in version 0.26.0.

    ## Special Methods[#](#special-methods "Link to this heading")

    \_\_repr\_\_()[#](#tree_sitter.Point.__repr__ "Link to this definition")
    :   Implements `repr(self)`.

    ## Attributes[#](#attributes "Link to this heading")

    column[#](#tree_sitter.Point.column "Link to this definition")
    :   The zero-based column of the document.

        Note

        Measured in bytes.

    row[#](#tree_sitter.Point.row "Link to this definition")
    :   The zero-based row of the document.

Contents