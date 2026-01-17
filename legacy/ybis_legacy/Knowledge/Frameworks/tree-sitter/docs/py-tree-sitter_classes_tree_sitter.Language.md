Language — py-tree-sitter 0.25.2 documentation



[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

[![py-tree-sitter 0.25.2 documentation - Home](../_static/logo.png)](../index.html)

# Language

## Contents

# Language[#](#language "Link to this heading")

*class* tree\_sitter.Language(*ptr*)[#](#tree_sitter.Language "Link to this definition")
:   A class that defines how to parse a particular language.

    ## Methods[#](#methods "Link to this heading")

    copy()[#](#tree_sitter.Language.copy "Link to this definition")
    :   Create a copy of the language.

    field\_id\_for\_name(*name*, */*)[#](#tree_sitter.Language.field_id_for_name "Link to this definition")
    :   Get the numerical id for the given field name.

    field\_name\_for\_id(*field\_id*, */*)[#](#tree_sitter.Language.field_name_for_id "Link to this definition")
    :   Get the field name for the given numerical id.

    id\_for\_node\_kind(*kind*, *named*, */*)[#](#tree_sitter.Language.id_for_node_kind "Link to this definition")
    :   Get the numerical id for the given node kind.

    lookahead\_iterator(*state*, */*)[#](#tree_sitter.Language.lookahead_iterator "Link to this definition")
    :   Create a new [`LookaheadIterator`](tree_sitter.LookaheadIterator.html#tree_sitter.LookaheadIterator "tree_sitter.LookaheadIterator") for this language and parse state.

    next\_state(*state*, *id*, */*)[#](#tree_sitter.Language.next_state "Link to this definition")
    :   Get the next parse state.

        Tip

        Combine this with `lookahead_iterator` to generate completion suggestions or valid symbols in error nodes.

        Examples

        ```
        >>> state = language.next_state(node.parse_state, node.grammar_id)
        ```

    node\_kind\_for\_id(*id*, */*)[#](#tree_sitter.Language.node_kind_for_id "Link to this definition")
    :   Get the name of the node kind for the given numerical id.

    node\_kind\_is\_named(*id*, */*)[#](#tree_sitter.Language.node_kind_is_named "Link to this definition")
    :   Check if the node type for the given numerical id is named (as opposed to an anonymous node type).

    node\_kind\_is\_supertype(*id*, */*)[#](#tree_sitter.Language.node_kind_is_supertype "Link to this definition")
    :   Check if the node type for the given numerical id is a supertype.

        Supertype nodes represent abstract categories of syntax nodes (e.g. “expression”).

    node\_kind\_is\_visible(*id*, */*)[#](#tree_sitter.Language.node_kind_is_visible "Link to this definition")
    :   Check if the node type for the given numerical id is visible (as opposed to an auxiliary node type).

    subtypes(*supertype*, */*)[#](#tree_sitter.Language.subtypes "Link to this definition")
    :   Get all subtype symbol IDs for a given supertype symbol.

    ## Special Methods[#](#special-methods "Link to this heading")

    \_\_copy\_\_()[#](#tree_sitter.Language.__copy__ "Link to this definition")
    :   Use [`copy.copy()`](https://docs.python.org/3.10/library/copy.html#copy.copy "(in Python v3.10)") to create a copy of the language.

    \_\_eq\_\_(*value*, */*)[#](#tree_sitter.Language.__eq__ "Link to this definition")
    :   Implements `self==value`.

    \_\_hash\_\_()[#](#tree_sitter.Language.__hash__ "Link to this definition")
    :   Implements `hash(self)`.

        Important

        On 32-bit platforms, you must use `hash(self) & 0xFFFFFFFF` to get the actual hash.

    \_\_ne\_\_(*value*, */*)[#](#tree_sitter.Language.__ne__ "Link to this definition")
    :   Implements `self!=value`.

    \_\_repr\_\_()[#](#tree_sitter.Language.__repr__ "Link to this definition")
    :   Implements `repr(self)`.

    ## Attributes[#](#attributes "Link to this heading")

    abi\_version[#](#tree_sitter.Language.abi_version "Link to this definition")
    :   The ABI version number that indicates which version of the Tree-sitter CLI was used to generate this language.

    field\_count[#](#tree_sitter.Language.field_count "Link to this definition")
    :   The number of distinct field names in this language.

    name[#](#tree_sitter.Language.name "Link to this definition")
    :   The name of the language.

    node\_kind\_count[#](#tree_sitter.Language.node_kind_count "Link to this definition")
    :   The number of distinct node types in this language.

    parse\_state\_count[#](#tree_sitter.Language.parse_state_count "Link to this definition")
    :   The number of valid states in this language.

    semantic\_version[#](#tree_sitter.Language.semantic_version "Link to this definition")
    :   The [Semantic Version](https://semver.org/) of the language.

    supertypes[#](#tree_sitter.Language.supertypes "Link to this definition")
    :   The supertype symbols of the language.

Contents