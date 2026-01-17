TreeCursor — py-tree-sitter 0.25.2 documentation



[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

[![py-tree-sitter 0.25.2 documentation - Home](../_static/logo.png)](../index.html)

# TreeCursor

## Contents

# TreeCursor[#](#treecursor "Link to this heading")

*class* tree\_sitter.TreeCursor[#](#tree_sitter.TreeCursor "Link to this definition")
:   A class for walking a syntax [`Tree`](tree_sitter.Tree.html#tree_sitter.Tree "tree_sitter.Tree") efficiently.

    Important

    The cursor can only walk into children of the node it was constructed with.

    ## Methods[#](#methods "Link to this heading")

    copy()[#](#tree_sitter.TreeCursor.copy "Link to this definition")
    :   Create an independent copy of the cursor.

    goto\_descendant(*index*, */*)[#](#tree_sitter.TreeCursor.goto_descendant "Link to this definition")
    :   Move the cursor to the node that is the n-th descendant of the original node that the cursor was constructed with, where `0` represents the original node itself.

    goto\_first\_child()[#](#tree_sitter.TreeCursor.goto_first_child "Link to this definition")
    :   Move this cursor to the first child of its current node.

        Returns:
        :   `True` if the cursor successfully moved, or `False` if there were no children.

    goto\_first\_child\_for\_byte(*byte*, */*)[#](#tree_sitter.TreeCursor.goto_first_child_for_byte "Link to this definition")
    :   Move this cursor to the first child of its current node that contains or starts after the given byte offset.

        Returns:
        :   The index of the child node if it was found, `None` otherwise.

    goto\_first\_child\_for\_point(*point*, */*)[#](#tree_sitter.TreeCursor.goto_first_child_for_point "Link to this definition")
    :   Move this cursor to the first child of its current node that contains or starts after the given given row/column point.

        Returns:
        :   The index of the child node if it was found, `None` otherwise.

    goto\_last\_child()[#](#tree_sitter.TreeCursor.goto_last_child "Link to this definition")
    :   Move this cursor to the last child of its current node.

        Returns:
        :   `True` if the cursor successfully moved, or `False` if there were no children.

        Caution

        This method may be slower than [`goto_first_child()`](#tree_sitter.TreeCursor.goto_first_child "tree_sitter.TreeCursor.goto_first_child") because it needs to iterate through all the children to compute the child’s position.

    goto\_next\_sibling()[#](#tree_sitter.TreeCursor.goto_next_sibling "Link to this definition")
    :   Move this cursor to the next sibling of its current node.

        Returns:
        :   `True` if the cursor successfully moved, or `False` if there was no next sibling.

    goto\_parent()[#](#tree_sitter.TreeCursor.goto_parent "Link to this definition")
    :   Move this cursor to the parent of its current node.

        Returns:
        :   `True` if the cursor successfully moved, or `False` if there was no parent node (i.e. the cursor was already on the root node).

    goto\_previous\_sibling()[#](#tree_sitter.TreeCursor.goto_previous_sibling "Link to this definition")
    :   Move this cursor to the previous sibling of its current node.

        Returns:
        :   `True` if the cursor successfully moved, or `False` if there was no previous sibling.

        Caution

        This method may be slower than [`goto_next_sibling()`](#tree_sitter.TreeCursor.goto_next_sibling "tree_sitter.TreeCursor.goto_next_sibling") due to how node positions are stored.
        In the worst case, this will need to iterate through all the children up to the previous sibling node to recalculate its position.

    reset(*node*, */*)[#](#tree_sitter.TreeCursor.reset "Link to this definition")
    :   Re-initialize the cursor to start at the original node that it was constructed with.

    reset\_to(*cursor*, */*)[#](#tree_sitter.TreeCursor.reset_to "Link to this definition")
    :   Re-initialize the cursor to the same position as another cursor.

        Unlike [`reset()`](#tree_sitter.TreeCursor.reset "tree_sitter.TreeCursor.reset"), this will not lose parent information and allows reusing already created cursors.

    ## Special Methods[#](#special-methods "Link to this heading")

    \_\_copy\_\_()[#](#tree_sitter.TreeCursor.__copy__ "Link to this definition")
    :   Use [`copy.copy()`](https://docs.python.org/3.10/library/copy.html#copy.copy "(in Python v3.10)") to create a copy of the cursor.

    ## Attributes[#](#attributes "Link to this heading")

    depth[#](#tree_sitter.TreeCursor.depth "Link to this definition")
    :   The depth of the cursor’s current node relative to the original node that it was constructed with.

    descendant\_index[#](#tree_sitter.TreeCursor.descendant_index "Link to this definition")
    :   The index of the cursor’s current node out of all of the descendants of the original node that the cursor was constructed with.

    field\_id[#](#tree_sitter.TreeCursor.field_id "Link to this definition")
    :   The numerical field id of this tree cursor’s current node, if available.

    field\_name[#](#tree_sitter.TreeCursor.field_name "Link to this definition")
    :   The field name of this tree cursor’s current node, if available.

    node[#](#tree_sitter.TreeCursor.node "Link to this definition")
    :   The current node.

Contents