Tree — py-tree-sitter 0.25.2 documentation



[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

[![py-tree-sitter 0.25.2 documentation - Home](../_static/logo.png)](../index.html)

# Tree

## Contents

# Tree[#](#tree "Link to this heading")

*class* tree\_sitter.Tree[#](#tree_sitter.Tree "Link to this definition")
:   A tree that represents the syntactic structure of a source code file.

    ## Methods[#](#methods "Link to this heading")

    changed\_ranges(*new\_tree*)[#](#tree_sitter.Tree.changed_ranges "Link to this definition")
    :   Compare this old edited syntax tree to a new syntax tree representing the same document, returning a sequence of ranges whose syntactic structure has changed.

        Returns:
        :   *Ranges where the hierarchical structure of syntax nodes (from root to leaf) has changed between the old and new trees. Characters outside these ranges have identical ancestor nodes in both trees.*

        Note

        The returned ranges may be slightly larger than the exact changed areas, but Tree-sitter attempts to make them as small as possible.

        Tip

        For this to work correctly, this syntax tree must have been edited such that its ranges match up to the new tree.

        Generally, you’ll want to call this method right after calling the [`Parser.parse()`](tree_sitter.Parser.html#tree_sitter.Parser.parse "tree_sitter.Parser.parse") method. Call it on the old tree that was passed to the method, and pass the new tree that was returned from it.

    copy()[#](#tree_sitter.Tree.copy "Link to this definition")
    :   Create a shallow copy of the tree.

    edit(*start\_byte*, *old\_end\_byte*, *new\_end\_byte*, *start\_point*, *old\_end\_point*, *new\_end\_point*)[#](#tree_sitter.Tree.edit "Link to this definition")
    :   Edit the syntax tree to keep it in sync with source code that has been edited.

        You must describe the edit both in terms of byte offsets and of row/column points.

    print\_dot\_graph(*file*)[#](#tree_sitter.Tree.print_dot_graph "Link to this definition")
    :   Write a DOT graph describing the syntax tree to the given file.

    root\_node\_with\_offset(*offset\_bytes*, *offset\_extent*, */*)[#](#tree_sitter.Tree.root_node_with_offset "Link to this definition")
    :   Get the root node of the syntax tree, but with its position shifted forward by the given offset.

    walk()[#](#tree_sitter.Tree.walk "Link to this definition")
    :   Create a new [`TreeCursor`](tree_sitter.TreeCursor.html#tree_sitter.TreeCursor "tree_sitter.TreeCursor") starting from the root of the tree.

    ## Special Methods[#](#special-methods "Link to this heading")

    \_\_copy\_\_()[#](#tree_sitter.Tree.__copy__ "Link to this definition")
    :   Use [`copy.copy()`](https://docs.python.org/3.10/library/copy.html#copy.copy "(in Python v3.10)") to create a copy of the tree.

    ## Attributes[#](#attributes "Link to this heading")

    included\_ranges[#](#tree_sitter.Tree.included_ranges "Link to this definition")
    :   The included ranges that were used to parse the syntax tree.

    language[#](#tree_sitter.Tree.language "Link to this definition")
    :   The language that was used to parse the syntax tree.

    root\_node[#](#tree_sitter.Tree.root_node "Link to this definition")
    :   The root node of the syntax tree.

Contents