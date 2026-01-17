Range — py-tree-sitter 0.25.2 documentation



[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

[![py-tree-sitter 0.25.2 documentation - Home](../_static/logo.png)](../index.html)

# Range

## Contents

# Range[#](#range "Link to this heading")

*class* tree\_sitter.Range(*start\_point*, *end\_point*, *start\_byte*, *end\_byte*)[#](#tree_sitter.Range "Link to this definition")
:   A range of positions in a multi-line text document, both in terms of bytes and of rows and columns.

    ## Methods[#](#methods "Link to this heading")

    edit(*start\_byte*, *old\_end\_byte*, *new\_end\_byte*, *start\_point*, *old\_end\_point*, *new\_end\_point*)[#](#tree_sitter.Range.edit "Link to this definition")
    :   Edit this range to keep it in-sync with source code that has been edited.

        Tip

        This is useful for editing ranges without requiring a tree or node instance.

        Added in version 0.26.0.

    ## Special Methods[#](#special-methods "Link to this heading")

    \_\_eq\_\_(*value*, */*)[#](#tree_sitter.Range.__eq__ "Link to this definition")
    :   Implements `self==value`.

    \_\_ne\_\_(*value*, */*)[#](#tree_sitter.Range.__ne__ "Link to this definition")
    :   Implements `self!=value`.

    \_\_repr\_\_()[#](#tree_sitter.Range.__repr__ "Link to this definition")
    :   Implements `repr(self)`.

    \_\_hash\_\_()[#](#tree_sitter.Range.__hash__ "Link to this definition")
    :   Implements `hash(self)`.

    ## Attributes[#](#attributes "Link to this heading")

    end\_byte[#](#tree_sitter.Range.end_byte "Link to this definition")
    :   The end byte.

    end\_point[#](#tree_sitter.Range.end_point "Link to this definition")
    :   The end point.

    start\_byte[#](#tree_sitter.Range.start_byte "Link to this definition")
    :   The start byte.

    start\_point[#](#tree_sitter.Range.start_point "Link to this definition")
    :   The start point.

Contents