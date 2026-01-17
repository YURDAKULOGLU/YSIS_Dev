QueryCursor — py-tree-sitter 0.25.2 documentation



[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

[![py-tree-sitter 0.25.2 documentation - Home](../_static/logo.png)](../index.html)

# QueryCursor

## Contents

# QueryCursor[#](#querycursor "Link to this heading")

*class* tree\_sitter.QueryCursor(*query*, *\**, *match\_limit=None*, *timeout\_micros=None*)[#](#tree_sitter.QueryCursor "Link to this definition")
:   A class for executing a [`Query`](tree_sitter.Query.html#tree_sitter.Query "tree_sitter.Query") on a syntax [`Tree`](tree_sitter.Tree.html#tree_sitter.Tree "tree_sitter.Tree").

    ## Methods[#](#methods "Link to this heading")

    captures(*node*, */*, *predicate=None*, *progress\_callback=None*)[#](#tree_sitter.QueryCursor.captures "Link to this definition")
    :   Get a list of *captures* within the given node.

        Returns:
        :   *A dict where the keys are the names of the captures and the values are lists of the captured nodes.*

        Hint

        This method returns all of the captures while [`matches()`](#tree_sitter.QueryCursor.matches "tree_sitter.QueryCursor.matches") only returns the last match.

    matches(*node*, */*, *predicate=None*, *progress\_callback=None*)[#](#tree_sitter.QueryCursor.matches "Link to this definition")
    :   Get a list of *matches* within the given node.

        Returns:
        :   *A list of tuples where the first element is the pattern index and the second element is a dictionary that maps capture names to nodes.*

    set\_byte\_range(*start*, *end*)[#](#tree_sitter.QueryCursor.set_byte_range "Link to this definition")
    :   Set the range of bytes in which the query will be executed.

        Raises:
        :   [**ValueError**](https://docs.python.org/3.10/library/exceptions.html#ValueError "(in Python v3.10)") – If the start byte exceeds the end byte.

        Note

        The query cursor will return matches that intersect with the given byte range. This means that a match may be returned even if some of its captures fall outside the specified range, as long as at least part of the match overlaps with it.

    set\_containing\_byte\_range(*start*, *end*)[#](#tree_sitter.QueryCursor.set_containing_byte_range "Link to this definition")
    :   Set the byte range within which all matches must be fully contained.

        Raises:
        :   [**ValueError**](https://docs.python.org/3.10/library/exceptions.html#ValueError "(in Python v3.10)") – If the start byte exceeds the end byte.

        Note

        In contrast to [`set_byte_range()`](#tree_sitter.QueryCursor.set_byte_range "tree_sitter.QueryCursor.set_byte_range"), this will restrict the query cursor to only return matches where *all* nodes are *fully* contained within the given range.
        Both methods can be used together, e.g. to search for any matches that intersect line 5000, as long as they are fully contained within lines 4500-5500

        Added in version 0.26.0.

    set\_containing\_point\_range(*start*, *end*)[#](#tree_sitter.QueryCursor.set_containing_point_range "Link to this definition")
    :   Set the point range within which all matches must be fully contained.

        Raises:
        :   [**ValueError**](https://docs.python.org/3.10/library/exceptions.html#ValueError "(in Python v3.10)") – If the start point exceeds the end point.

        Note

        In contrast to [`set_point_range()`](#tree_sitter.QueryCursor.set_point_range "tree_sitter.QueryCursor.set_point_range"), this will restrict the query cursor to only return matches where *all* nodes are *fully* contained within the given range.
        Both methods can be used together, e.g. to search for any matches that intersect line 5000, as long as they are fully contained within lines 4500-5500

        Added in version 0.26.0.

    set\_max\_start\_depth(*max\_start\_depth*)[#](#tree_sitter.QueryCursor.set_max_start_depth "Link to this definition")
    :   Set the maximum start depth for the query.

    set\_point\_range(*start*, *end*)[#](#tree_sitter.QueryCursor.set_point_range "Link to this definition")
    :   Set the range of points in which the query will be executed.

        Raises:
        :   [**ValueError**](https://docs.python.org/3.10/library/exceptions.html#ValueError "(in Python v3.10)") – If the start point exceeds the end point.

        Note

        The query cursor will return matches that intersect with the given point range. This means that a match may be returned even if some of its captures fall outside the specified range, as long as at least part of the match overlaps with it.

    ## Attributes[#](#attributes "Link to this heading")

    did\_exceed\_match\_limit[#](#tree_sitter.QueryCursor.did_exceed_match_limit "Link to this definition")
    :   Check if the query exceeded its maximum number of in-progress matches during its last execution.

    match\_limit[#](#tree_sitter.QueryCursor.match_limit "Link to this definition")
    :   The maximum number of in-progress matches.

Contents