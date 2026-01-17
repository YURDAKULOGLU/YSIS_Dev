Query — py-tree-sitter 0.25.2 documentation



[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

[![py-tree-sitter 0.25.2 documentation - Home](../_static/logo.png)](../index.html)

# Query

## Contents

# Query[#](#query "Link to this heading")

*class* tree\_sitter.Query(*language*, *source*)[#](#tree_sitter.Query "Link to this definition")
:   A set of patterns that match nodes in a syntax tree.

    Raises:
    :   [**QueryError**](tree_sitter.QueryError.html#tree_sitter.QueryError "tree_sitter.QueryError") – If any error occurred while creating the query.

    See also

    [Query Syntax](https://tree-sitter.github.io/tree-sitter/using-parsers#query-syntax)

    Note

    The following predicates are supported by default:

    * `#eq?`, `#not-eq?`, `#any-eq?`, `#any-not-eq?`
    * `#match?`, `#not-match?`, `#any-match?`, `#any-not-match?`
    * `#any-of?`, `#not-any-of?`
    * `#is?`, `#is-not?`
    * `#set!`

    ## Methods[#](#methods "Link to this heading")

    capture\_name(*index*)[#](#tree_sitter.Query.capture_name "Link to this definition")
    :   Get the name of the capture at the given index.

    capture\_quantifier(*pattern\_index*, *capture\_index*)[#](#tree_sitter.Query.capture_quantifier "Link to this definition")
    :   Get the quantifier of the capture at the given indexes.

    disable\_capture(*name*)[#](#tree_sitter.Query.disable_capture "Link to this definition")
    :   Disable a certain capture within a query.

        Important

        Currently, there is no way to undo this.

    disable\_pattern(*index*)[#](#tree_sitter.Query.disable_pattern "Link to this definition")
    :   Disable a certain pattern within a query.

        Important

        Currently, there is no way to undo this.

    end\_byte\_for\_pattern(*index*)[#](#tree_sitter.Query.end_byte_for_pattern "Link to this definition")
    :   Get the byte offset where the given pattern ends in the query’s source.

    is\_pattern\_guaranteed\_at\_step(*index*)[#](#tree_sitter.Query.is_pattern_guaranteed_at_step "Link to this definition")
    :   Check if a pattern is guaranteed to match once a given byte offset is reached.

    is\_pattern\_non\_local(*index*)[#](#tree_sitter.Query.is_pattern_non_local "Link to this definition")
    :   Check if the pattern with the given index is “non-local”.

        Note

        A non-local pattern has multiple root nodes and can match within a repeating sequence of nodes, as specified by the grammar. Non-local patterns disable certain optimizations that would otherwise be possible when executing a query on a specific range of a syntax tree.

    is\_pattern\_rooted(*index*)[#](#tree_sitter.Query.is_pattern_rooted "Link to this definition")
    :   Check if the pattern with the given index has a single root node.

    pattern\_assertions(*index*)[#](#tree_sitter.Query.pattern_assertions "Link to this definition")
    :   Get the property assertions for the given pattern index.

        Assertions are performed using the `#is?` and `#is-not?` predicates.

        Returns:
        :   *A dictionary of assertions, where the first item is the optional property value and the second item indicates whether the assertion was positive or negative.*

    pattern\_settings(*index*)[#](#tree_sitter.Query.pattern_settings "Link to this definition")
    :   Get the property settings for the given pattern index.

        Properties are set using the `#set!` predicate.

        Returns:
        :   *A dictionary of properties with optional values.*

    start\_byte\_for\_pattern(*index*)[#](#tree_sitter.Query.start_byte_for_pattern "Link to this definition")
    :   Get the byte offset where the given pattern starts in the query’s source.

    string\_value(*index*)[#](#tree_sitter.Query.string_value "Link to this definition")
    :   Get the string literal at the given index.

    ## Attributes[#](#attributes "Link to this heading")

    capture\_count[#](#tree_sitter.Query.capture_count "Link to this definition")
    :   The number of captures in the query.

    pattern\_count[#](#tree_sitter.Query.pattern_count "Link to this definition")
    :   The number of patterns in the query.

    string\_count[#](#tree_sitter.Query.string_count "Link to this definition")
    :   The number of string literals in the query.

Contents