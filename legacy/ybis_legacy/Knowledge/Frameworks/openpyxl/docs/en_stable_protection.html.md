Protection — openpyxl 3.1.3 documentation

### Navigation

* [index](genindex.html "General Index")
* [modules](py-modindex.html "Python Module Index") |
* [next](charts/introduction.html "Charts") |
* [previous](workbook_custom_doc_props.html "Custom Document Properties") |
* [openpyxl 3.1.3 documentation](index.html) »
* Protection

# Protection[](#protection "Link to this heading")

Warning

Password protecting a workbook or worksheet only provides a quite basic level of security.
The data is not encrypted, so can be modified by any number of freely available tools. In
fact the specification states: “Worksheet or workbook element protection should not be
confused with file security. It is meant to make your workbook safe from unintentional
modification, and cannot protect it from malicious modification.”

Openpyxl provides support for protecting a workbook and worksheet from modification. The Open XML
“Legacy Password Hash Algorithm” is used to generate hashed password values unless another
algorithm is explicitly configured.

## Workbook Protection[](#workbook-protection "Link to this heading")

To prevent other users from viewing hidden worksheets, adding, moving, deleting, or hiding worksheets, and
renaming worksheets, you can protect the structure of your workbook with a password. The password can be
set using the [`openpyxl.workbook.protection.WorkbookProtection.workbookPassword()`](api/openpyxl.workbook.protection.html#openpyxl.workbook.protection.WorkbookProtection.workbookPassword "openpyxl.workbook.protection.WorkbookProtection.workbookPassword") property

```
>>> wb.security.workbookPassword = '...'
>>> wb.security.lockStructure = True
```

Similarly removing change tracking and change history from a shared workbook can be prevented by setting
another password. This password can be set using the
[`openpyxl.workbook.protection.WorkbookProtection.revisionsPassword()`](api/openpyxl.workbook.protection.html#openpyxl.workbook.protection.WorkbookProtection.revisionsPassword "openpyxl.workbook.protection.WorkbookProtection.revisionsPassword") property

```
>>> wb.security.revisionsPassword = '...'
```

Other properties on the [`openpyxl.workbook.protection.WorkbookProtection`](api/openpyxl.workbook.protection.html#openpyxl.workbook.protection.WorkbookProtection "openpyxl.workbook.protection.WorkbookProtection") object control exactly what
restrictions are in place, but these will only be enforced if the appropriate password is set.

Specific setter functions are provided if you need to set the raw password value without using the
default hashing algorithm - e.g.

```
hashed_password = ...
wb.security.set_workbook_password(hashed_password, already_hashed=True)
```

## Worksheet Protection[](#worksheet-protection "Link to this heading")

Various aspects of a worksheet can also be locked by setting attributes on the
[`openpyxl.worksheet.protection.SheetProtection`](api/openpyxl.worksheet.protection.html#openpyxl.worksheet.protection.SheetProtection "openpyxl.worksheet.protection.SheetProtection") object. Unlike workbook protection, sheet
protection may be enabled with or without using a password. Sheet protection is enabled using the
`openpxyl.worksheet.protection.SheetProtection.sheet` attribute or calling enable() or disable():

```
>>> ws = wb.active
>>> ws.protection.sheet = True
>>> ws.protection.enable()
>>> ws.protection.disable()
```

If no password is specified, users can disable configured sheet protection without specifying a password.
Otherwise they must supply a password to change configured protections. The password is set using
the `openpxyl.worksheet.protection.SheetProtection.password()` property

```
>>> ws = wb.active
>>> ws.protection.password = '...'
```

[![Logo](_static/logo.png)](index.html)

### [Table of Contents](index.html)

* [Protection](#)
  + [Workbook Protection](#workbook-protection)
  + [Worksheet Protection](#worksheet-protection)

#### Previous topic

[Custom Document Properties](workbook_custom_doc_props.html "previous chapter")

#### Next topic

[Charts](charts/introduction.html "next chapter")

### This Page

* [Show Source](_sources/protection.rst.txt)

### Quick search

### Navigation

* [index](genindex.html "General Index")
* [modules](py-modindex.html "Python Module Index") |
* [next](charts/introduction.html "Charts") |
* [previous](workbook_custom_doc_props.html "Custom Document Properties") |
* [openpyxl 3.1.3 documentation](index.html) »
* Protection

© Copyright 2010 - 2024, See AUTHORS.
Created using [Sphinx](https://www.sphinx-doc.org/) 7.3.7.