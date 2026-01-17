grammars - Outlines






[Skip to content](#outlines.grammars)

# grammars

A few common Lark grammars.

## `read_grammar(grammar_file_name, base_grammar_path=GRAMMAR_PATH)`

Read grammar file from default grammar path.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `grammar_file_name` | `str` | The name of the grammar file to read. | *required* |
| `base_grammar_path` | `Path` | The path to the directory containing the grammar file. | `GRAMMAR_PATH` |

Returns:

| Type | Description |
| --- | --- |
| `str` | The contents of the grammar file. |

Source code in `outlines/grammars.py`

|  |  |
| --- | --- |
| ```  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 ``` | ``` def read_grammar(     grammar_file_name: str,     base_grammar_path: Path = GRAMMAR_PATH, ) -> str:     """Read grammar file from default grammar path.      Parameters     ----------     grammar_file_name         The name of the grammar file to read.     base_grammar_path         The path to the directory containing the grammar file.      Returns     -------     str         The contents of the grammar file.      """     full_path = base_grammar_path / grammar_file_name     with open(full_path) as file:         return file.read() ``` |

2025-11-24




2025-11-24