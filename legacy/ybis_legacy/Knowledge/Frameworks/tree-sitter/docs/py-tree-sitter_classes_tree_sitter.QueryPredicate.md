QueryPredicate — py-tree-sitter 0.25.2 documentation



[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

[![py-tree-sitter 0.25.2 documentation - Home](../_static/logo.png)](../index.html)

# QueryPredicate

## Contents

# QueryPredicate[#](#querypredicate "Link to this heading")

*class* tree\_sitter.QueryPredicate[#](#tree_sitter.QueryPredicate "Link to this definition")
:   Bases: [`Protocol`](https://docs.python.org/3.10/library/typing.html#typing.Protocol "(in Python v3.10)")

    A custom query predicate that runs on a pattern.

    ## Special Methods[#](#special-methods "Link to this heading")

    \_\_call\_\_(*predicate*, *args*, *pattern\_index*, *captures*)[#](#tree_sitter.QueryPredicate.__call__ "Link to this definition")
    :   Parameters:
        :   * **predicate** ([*str*](https://docs.python.org/3.10/library/stdtypes.html#str "(in Python v3.10)")) – The name of the predicate.
            * **args** ([*list*](https://docs.python.org/3.10/library/stdtypes.html#list "(in Python v3.10)")*[*[*tuple*](https://docs.python.org/3.10/library/stdtypes.html#tuple "(in Python v3.10)")*[*[*str*](https://docs.python.org/3.10/library/stdtypes.html#str "(in Python v3.10)")*,* [*Literal*](https://docs.python.org/3.10/library/typing.html#typing.Literal "(in Python v3.10)")*[**'capture'**,* *'string'**]**]**]*) – The arguments to the predicate.
            * **pattern\_index** ([*int*](https://docs.python.org/3.10/library/functions.html#int "(in Python v3.10)")) – The index of the pattern within the query.
            * **captures** ([*dict*](https://docs.python.org/3.10/library/stdtypes.html#dict "(in Python v3.10)")*[*[*str*](https://docs.python.org/3.10/library/stdtypes.html#str "(in Python v3.10)")*,* [*list*](https://docs.python.org/3.10/library/stdtypes.html#list "(in Python v3.10)")*[*[*Node*](tree_sitter.Node.html#tree_sitter.Node "tree_sitter.Node")*]**]*) – The captures contained in the pattern.

        Returns:
        :   `True` if the predicate matches, `False` otherwise.

        Tip

        You don’t need to create an actual class, just a function with this signature.

Contents