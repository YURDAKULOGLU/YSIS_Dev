Node — py-tree-sitter 0.25.2 documentation



[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

[![py-tree-sitter 0.25.2 documentation - Home](../_static/logo.png)](../index.html)

# Node

## Contents

# Node[#](#node "Link to this heading")

*class* tree\_sitter.Node[#](#tree_sitter.Node "Link to this definition")
:   A single node within a syntax `Tree`.

    ## Methods[#](#methods "Link to this heading")

    child(*index*, */*)[#](#tree_sitter.Node.child "Link to this definition")
    :   Get this node’s child at the given index, where `0` represents the first child.

        Caution

        This method is fairly fast, but its cost is technically `log(i)`, so if you might be iterating over a long list of children, you should use [`children`](#tree_sitter.Node.children "tree_sitter.Node.children") or [`walk()`](#tree_sitter.Node.walk "tree_sitter.Node.walk") instead.

    child\_by\_field\_id(*id*, */*)[#](#tree_sitter.Node.child_by_field_id "Link to this definition")
    :   Get the first child with the given numerical field id.

        Hint

        You can convert a field name to an id using [`Language.field_id_for_name()`](tree_sitter.Language.html#tree_sitter.Language.field_id_for_name "tree_sitter.Language.field_id_for_name").

        See also

        [`child_by_field_name()`](#tree_sitter.Node.child_by_field_name "tree_sitter.Node.child_by_field_name")

    child\_by\_field\_name(*name*, */*)[#](#tree_sitter.Node.child_by_field_name "Link to this definition")
    :   Get the first child with the given field name.

    child\_with\_descendant(*descendant*, */*)[#](#tree_sitter.Node.child_with_descendant "Link to this definition")
    :   Get the node that contains the given descendant.

    children\_by\_field\_id(*id*, */*)[#](#tree_sitter.Node.children_by_field_id "Link to this definition")
    :   Get a list of children with the given numerical field id.

        See also

        [`children_by_field_name()`](#tree_sitter.Node.children_by_field_name "tree_sitter.Node.children_by_field_name")

    children\_by\_field\_name(*name*, */*)[#](#tree_sitter.Node.children_by_field_name "Link to this definition")
    :   Get a list of children with the given field name.

    descendant\_for\_byte\_range(*start\_byte*, *end\_byte*, */*)[#](#tree_sitter.Node.descendant_for_byte_range "Link to this definition")
    :   Get the smallest node within this node that spans the given byte range.

    descendant\_for\_point\_range(*start\_point*, *end\_point*, */*)[#](#tree_sitter.Node.descendant_for_point_range "Link to this definition")
    :   Get the smallest node within this node that spans the given point range.

    edit(*start\_byte*, *old\_end\_byte*, *new\_end\_byte*, *start\_point*, *old\_end\_point*, *new\_end\_point*)[#](#tree_sitter.Node.edit "Link to this definition")
    :   Edit this node to keep it in-sync with source code that has been edited.

        Note

        This method is only rarely needed. When you edit a syntax tree via [`Tree.edit()`](tree_sitter.Tree.html#tree_sitter.Tree.edit "tree_sitter.Tree.edit"), all of the nodes that you retrieve from the tree afterwards will already reflect the edit. You only need to use this when you have a specific [`Node`](#tree_sitter.Node "tree_sitter.Node") instance that you want to keep and continue to use after an edit.

    field\_name\_for\_child(*child\_index*, */*)[#](#tree_sitter.Node.field_name_for_child "Link to this definition")
    :   Get the field name of this node’s child at the given index.

    field\_name\_for\_named\_child()[#](#tree_sitter.Node.field_name_for_named_child "Link to this definition")
    :   field\_name\_for\_child(self, child\_index, /)
        –

        Get the field name of this node’s *named* child at the given index.

    first\_child\_for\_byte(*byte*, */*)[#](#tree_sitter.Node.first_child_for_byte "Link to this definition")
    :   Get the node’s first child that contains or starts after the given byte offset.

    first\_named\_child\_for\_byte(*byte*, */*)[#](#tree_sitter.Node.first_named_child_for_byte "Link to this definition")
    :   Get the node’s first *named* child that contains or starts after the given byte offset.

    named\_child(*index*, */*)[#](#tree_sitter.Node.named_child "Link to this definition")
    :   Get this node’s *named* child at the given index, where `0` represents the first child.

        Caution

        This method is fairly fast, but its cost is technically `log(i)`, so if you might be iterating over a long list of children, you should use [`children`](#tree_sitter.Node.children "tree_sitter.Node.children") or [`walk()`](#tree_sitter.Node.walk "tree_sitter.Node.walk") instead.

    named\_descendant\_for\_byte\_range(*start\_byte*, *end\_byte*, */*)[#](#tree_sitter.Node.named_descendant_for_byte_range "Link to this definition")
    :   Get the smallest *named* node within this node that spans the given byte range.

    named\_descendant\_for\_point\_range(*start\_point*, *end\_point*, */*)[#](#tree_sitter.Node.named_descendant_for_point_range "Link to this definition")
    :   Get the smallest *named* node within this node that spans the given point range.

    walk()[#](#tree_sitter.Node.walk "Link to this definition")
    :   Create a new [`TreeCursor`](tree_sitter.TreeCursor.html#tree_sitter.TreeCursor "tree_sitter.TreeCursor") starting from this node.

    ## Special Methods[#](#special-methods "Link to this heading")

    \_\_eq\_\_(*value*, */*)[#](#tree_sitter.Node.__eq__ "Link to this definition")
    :   Implements `self==value`.

    \_\_hash\_\_()[#](#tree_sitter.Node.__hash__ "Link to this definition")
    :   Implements `hash(self)`.

    \_\_ne\_\_(*value*, */*)[#](#tree_sitter.Node.__ne__ "Link to this definition")
    :   Implements `self!=value`.

    \_\_repr\_\_()[#](#tree_sitter.Node.__repr__ "Link to this definition")
    :   Implements `repr(self)`.

    \_\_str\_\_()[#](#tree_sitter.Node.__str__ "Link to this definition")
    :   Implements `str(self)`.

    ## Attributes[#](#attributes "Link to this heading")

    byte\_range[#](#tree_sitter.Node.byte_range "Link to this definition")
    :   The byte range of source code that this node represents, in terms of bytes.

    child\_count[#](#tree_sitter.Node.child_count "Link to this definition")
    :   This node’s number of children.

    children[#](#tree_sitter.Node.children "Link to this definition")
    :   This node’s children.

        Note

        If you’re walking the tree recursively, you may want to use [`walk()`](#tree_sitter.Node.walk "tree_sitter.Node.walk") instead.

    descendant\_count[#](#tree_sitter.Node.descendant_count "Link to this definition")
    :   This node’s number of descendants, including the node itself.

    end\_byte[#](#tree_sitter.Node.end_byte "Link to this definition")
    :   The byte offset where this node ends.

    end\_point[#](#tree_sitter.Node.end_point "Link to this definition")
    :   This node’s end point.

    grammar\_id[#](#tree_sitter.Node.grammar_id "Link to this definition")
    :   This node’s type as a numerical id as it appears in the grammar ignoring aliases.

    grammar\_name[#](#tree_sitter.Node.grammar_name "Link to this definition")
    :   This node’s symbol name as it appears in the grammar ignoring aliases.

    has\_changes[#](#tree_sitter.Node.has_changes "Link to this definition")
    :   Check if this node has been edited.

    has\_error[#](#tree_sitter.Node.has_error "Link to this definition")
    :   Check if this node represents a syntax error or contains any syntax errors anywhere within it.

    id[#](#tree_sitter.Node.id "Link to this definition")
    :   This node’s numerical id.

        Note

        Within a given syntax tree, no two nodes have the same id. However, if a new tree is created based on an older tree, and a node from the old tree is reused in the process, then that node will have the same id in both trees.

    is\_error[#](#tree_sitter.Node.is_error "Link to this definition")
    :   Check if this node represents a syntax error.

        Syntax errors represent parts of the code that could not be incorporated into a valid syntax tree.

    is\_extra[#](#tree_sitter.Node.is_extra "Link to this definition")
    :   Check if this node is \_extra\_.

        Extra nodes represent things which are not required by the grammar but can appear anywhere (e.g. whitespace).

    is\_missing[#](#tree_sitter.Node.is_missing "Link to this definition")
    :   Check if this node is \_missing\_.

        Missing nodes are inserted by the parser in order to recover from certain kinds of syntax errors.

    is\_named[#](#tree_sitter.Node.is_named "Link to this definition")
    :   Check if this node is \_named\_.

        Named nodes correspond to named rules in the grammar, whereas *anonymous* nodes correspond to string literals in the grammar.

    kind\_id[#](#tree_sitter.Node.kind_id "Link to this definition")
    :   This node’s type as a numerical id.

    named\_child\_count[#](#tree_sitter.Node.named_child_count "Link to this definition")
    :   This node’s number of \_named\_ children.

    named\_children[#](#tree_sitter.Node.named_children "Link to this definition")
    :   This node’s \_named\_ children.

    next\_named\_sibling[#](#tree_sitter.Node.next_named_sibling "Link to this definition")
    :   This node’s next named sibling.

    next\_parse\_state[#](#tree_sitter.Node.next_parse_state "Link to this definition")
    :   The parse state after this node.

    next\_sibling[#](#tree_sitter.Node.next_sibling "Link to this definition")
    :   This node’s next sibling.

    parent[#](#tree_sitter.Node.parent "Link to this definition")
    :   This node’s immediate parent.

    parse\_state[#](#tree_sitter.Node.parse_state "Link to this definition")
    :   This node’s parse state.

    prev\_named\_sibling[#](#tree_sitter.Node.prev_named_sibling "Link to this definition")
    :   This node’s previous named sibling.

    prev\_sibling[#](#tree_sitter.Node.prev_sibling "Link to this definition")
    :   This node’s previous sibling.

    range[#](#tree_sitter.Node.range "Link to this definition")
    :   The range of source code that this node represents.

    start\_byte[#](#tree_sitter.Node.start_byte "Link to this definition")
    :   The byte offset where this node starts.

    start\_point[#](#tree_sitter.Node.start_point "Link to this definition")
    :   This node’s start point

    text[#](#tree_sitter.Node.text "Link to this definition")
    :   The text of the node, if the tree has not been edited

    type[#](#tree_sitter.Node.type "Link to this definition")
    :   This node’s type as a string.

Contents