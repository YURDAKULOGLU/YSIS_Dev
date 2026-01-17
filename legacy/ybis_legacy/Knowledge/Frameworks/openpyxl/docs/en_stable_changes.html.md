3.1.3 (2024-05-29) — openpyxl 3.1.3 documentation

### Navigation

* [index](genindex.html "General Index")
* [modules](py-modindex.html "Python Module Index") |
* [previous](formula.html "Parsing Formulas") |
* [openpyxl 3.1.3 documentation](index.html) »
* 3.1.3 (2024-05-29)

# 3.1.3 (2024-05-29)[](#id1 "Link to this heading")

## Bugfixes[](#bugfixes "Link to this heading")

* [#1401](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1401) Column name caches are slow and use a lot of memory
* [#1457](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1457) Improved handling of duplicate named styles
* [#1842](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1842) Rich-text can be saved if lxml is not installed
* [#1954](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1954) Documentation for sheet views is incorrect
* [#1973](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1973) Timedeltas not read properly in read-only mode
* [#1987](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1987) List of formulae names contains mistakes
* [#1967](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1967) Filters does not handle non-numerical filters
* [#2054](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/2054) Type checking increases exponentially
* [#2057](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/2057) Loading pivot tables can be unnecessarily slow
* [#2102](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/2102) Improve performance when reading files with lots of custom properties
* [#2106](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/2106) Setting Trendline.name attribute raises exception when saving
* [#2120](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/2120) Timezone and Zombie formatting cannot be combined.
* [#2107](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/2107) Column name generation is inefficient and slow
* [#2122](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/2122) File handlers not always released in read-only mode
* [#2149](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/2149) Workbook files not properly closed on Python ≥ 3.11.8 and Windows
* [#2161](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/2161) Pivot cache definitions using tupleCache had serialisation issues

## Changes[](#changes "Link to this heading")

* Add a \_\_repr\_\_ method for Row and Column dimension objects so you don’t need to check every time.

# 3.1.2 (2023-03-11)[](#id18 "Link to this heading")

* [#1963](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1963) Cannot read worksheets in read-only mode with locally scoped definitions
* [#1974](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1974) Empty custom properties cause invalid files

# 3.1.1 (2023-02-13)[](#id21 "Link to this heading")

## Bugfixes[](#id22 "Link to this heading")

* [#1881](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1881) DocumentProperties times set by module import only
* [#1947](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1947) Worksheet-specific definitions are missing

# 3.1.0 (2023-01-31)[](#id25 "Link to this heading")

## New Features[](#new-features "Link to this heading")

* Added support for data table formulae
* Mapped chartspace graphical properties to charts for advanced formatting

## Bugfixes[](#id26 "Link to this heading")

* [#1156](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1156) Table filters are always overriden
* [#1360](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1360) Can’t read some ScatterCharts if n
* [#1724](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1724) Problem with multilevel indices in dataframes
* [#1763](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1763) Make calculating worksheet sizes slightly faster
* [#1772](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1772) Problem with category indices in dataframes
* [#1786](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1786) NamedStyles share attributes - mutables gotcha
* [#1851](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1851) Allow print area to be set to None
* [#1852](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1852) Worksheet for print title and print areas can’t be found
* [#1853](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1853) Custom document properties that are strings can be empty
* [#1858](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1858) ConditionalFormatting lost when pivot table updated
* [#1864](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1864) Better handling of defined names
* [#1904](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1904) dataframe\_to\_rows() misalignment on multiindex
* [#1908](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1908) Ditto
* [#1912](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1912) Excel doesn’t like xmlns:space on nodes with only whitespace, which it treats as empty.
* [#1942](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1942) Exception when print areas use table references.

## Pull Requests[](#pull-requests "Link to this heading")

* [PR409](https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/409/) Support for Rich Text in cells
* [PR411](https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/411/) Provide more information when workbook cannot be loaded
* [PR407](https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/407/) Support for Custom Document Properties

## Deprecations[](#deprecations "Link to this heading")

The following properties have been removed from worksheets: formula\_attributes, page\_breaks, show\_summary\_below, show\_summary\_right, page\_size orientation. Client code should use the relevant objects.

## Removals[](#removals "Link to this heading")

The following deprecated methods have been removed from workbooks: get\_named\_range, add\_named\_range, remove\_named\_range. And the get\_emu\_dimesions from images.

# 3.0.10 (2022-05-19)[](#id42 "Link to this heading")

## Bugfixes[](#id43 "Link to this heading")

* [#1684](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1684) Image files not closed when workbooks are saved
* [#1778](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1778) Problem with missing scope attribute in Pivot Table formats
* [#1821](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1821) Excel unhappy when multiple sorts are defined
* [#2014](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/2014) Accounting format interpreted as datetime

# 3.0.9 (2021-09-22)[](#id48 "Link to this heading")

## Bugfixes[](#id49 "Link to this heading")

* [#1284](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1284) Ignore blank ignored in existing Data Validations
* [#1539](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1539) Add support for cell protection for merged cell ranges
* [#1645](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1645) Timezone-aware datetimes raise an Exception
* [#1666](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1666) Improved normalisation of chart series
* [#1670](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1670) Catch OverflowError for out of range datetimes
* [#1708](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1708) Alignment.relativeIndent can be negative
* [#1736](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1769) Incorrect default value groupBy attribute

# 3.0.8 (brown bag)[](#brown-bag "Link to this heading")

Deleted because it contained breaking changes from 3.1

# 3.0.7 (2021-03-09)[](#id57 "Link to this heading")

## Bugfixes[](#id58 "Link to this heading")

* [#1510](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1510) Problems with zero time values
* [#1588](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1588) Not possible to correctly convert excel dates to timedelta
* [#1589](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1589) Exception raised when merging cells which do not have borders all the way round.
* [#1594](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1594) Python 2 print statement in the tutorial

## Pull Requests[](#id63 "Link to this heading")

* [PR392](https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/392/) Add documentation on datetime handling
* [PR393](https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/393/) Drop dependency on jdcal
* [PR394](https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/394/) Datetime rounding
* [PR395](https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/395/) Unify handling of 1900 epoch
* [PR397](https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/397/) Add explicit support for reading datetime deltas
* [PR399](https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/399/) Millisecond precision for datetimes

# 3.0.6 (2021-01-14)[](#id64 "Link to this heading")

## Bugfixes[](#id65 "Link to this heading")

* [#1154](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1154) Borders in differential styles are incorrect
* [#1287](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1528) Error when opening some pivot tables
* [#1366](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1366) Resave breaks the border format in conditional formatting rules
* [#1450](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1450) Read-only workbook not closed properly if generator interrupted
* [#1547](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1547) Pandas.Multiindex.labels deprecated
* [#1552](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1557) Pandas.Multiinex not expanded correctly
* [#1557](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1557) Cannot read rows with exponents
* [#1568](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1568) numpy.float is deprecated
* [#1571](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1571) Cells without coordinate attributes not always correctly handled

## Pull Requests[](#id75 "Link to this heading")

* [PR385](https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/385/) Improved handling of borders for differential styles
* [PR386](https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/386/) Support subclasses of datetime objects
* [PR387](https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/387/) Improved handling of cells without coordinates

# 3.0.5 (2020-08-21)[](#id76 "Link to this heading")

## Bugfixes[](#id77 "Link to this heading")

* [#1413](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1413) Incorrectly consider currency format as datetime
* [#1490](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1490) Cannot copy worksheets with merged cells
* [#1492](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1492) Empty worksheets do not return generators when looping.
* [#1496](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1496) Hyperlinks duplicated on multiple saves
* [#1500](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1500) Incorrectly literal format as datetime
* [#1502](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1502) Links set to range of cells not preserved
* [#1507](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1507) Exception when opening workbook with chartsheets and tables

# 3.0.4 (2020-06-24)[](#id85 "Link to this heading")

## Bugfixes[](#id86 "Link to this heading")

* [#844](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/844) Find tables by name
* [#1414](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1414) Worksheet protection missing in existing files
* [#1439](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1439) Exception when reading files with external images
* [#1452](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1452) Reading lots of merged cells is very slow.
* [#1455](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1455) Read support for Bubble Charts.
* [#1458](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1458) Preserve any indexed colours
* [#1473](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1473) Reading many thousand of merged cells is really slow.
* [#1474](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1474) Adding tables in write-only mode raises an exception.

## Pull Requests[](#id95 "Link to this heading")

* [PR377](https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/377/) Add support for finding tables by name or range.

# 3.0.3 (2020-01-20)[](#id96 "Link to this heading")

## Bugfixes[](#id97 "Link to this heading")

* [#1260](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1260) Exception when handling merged cells with hyperlinks
* [#1373](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1373) Problems when both lxml and defusedxml are installed
* [#1385](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1385) CFVO with incorrect values cannot be processed

# 3.0.2 (2019-11-25)[](#id101 "Link to this heading")

## Bug fixes[](#bug-fixes "Link to this heading")

* [#1267](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1267) DeprecationError if both defusedxml and lxml are installed
* [#1345](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1345) ws.\_current\_row is higher than ws.max\_row
* [#1365](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1365) Border bottom style is not optional when it should be
* [#1367](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1367) Empty cells in read-only, values-only mode are sometimes returned as ReadOnlyCells
* [#1368](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1368) Cannot add page breaks to existing worksheets if none exist already

## Pull Requests[](#id107 "Link to this heading")

* [PR359](https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/359/) Improvements to the documentation

# 3.0.1 (2019-11-14)[](#id108 "Link to this heading")

## Bugfixes[](#id109 "Link to this heading")

* [#1250](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1250) Cannot read empty charts.

## Pull Requests[](#id111 "Link to this heading")

* [PR354](https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/354/) Fix for #1250
* [PR352](https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/354/) TableStyleElement is a sequence

# 3.0.0 (2019-09-25)[](#id112 "Link to this heading")

## Python 3.6+ only release[](#python-3-6-only-release "Link to this heading")

# 2.6.4 (2019-09-25)[](#id113 "Link to this heading")

## Final release for Python 2.7 and 3.5[](#final-release-for-python-2-7-and-3-5 "Link to this heading")

## Bugfixes[](#id114 "Link to this heading")

* ` #1330 <<https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1330>>`\_ Cannot save workbooks with comments more than once.

# 2.6.3 (2019-08-19)[](#id115 "Link to this heading")

## Bugfixes[](#id116 "Link to this heading")

* [#1237](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1237) Fix 3D charts.
* [#1290](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1290) Minimum for holeSize in Doughnut charts too high
* [#1291](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1291) Warning for MergedCells with comments
* [#1296](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1296) Pagebreaks duplicated
* [#1309](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1309) Workbook has no default CellStyle
* [#1330](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1330) Workbooks with comments cannot be saved multiple times

## Pull Requests[](#id123 "Link to this heading")

* [PR344](https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/345/) Make sure NamedStyles number formats are correctly handled

# 2.6.2 (2019-03-29)[](#id124 "Link to this heading")

## Bugfixes[](#id125 "Link to this heading")

* [#1173](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1173) Workbook has no \_date\_formats attribute
* [#1190](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1190) Cannot create charts for worksheets with quotes in the title
* [#1228](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1228) MergedCells not removed when range is unmerged
* [#1232](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1232) Link to pivot table lost from charts
* [#1233](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1233) Chart colours change after saving
* [#1236](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1236) Cannot use ws.cell in read-only mode with Python 2.7

# 2.6.1 (2019-03-04)[](#id132 "Link to this heading")

## Bugfixes[](#id133 "Link to this heading")

* [#1174](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1174) ReadOnlyCell.is\_date does not work properly
* [#1175](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1175) Cannot read Google Docs spreadsheet with a Pivot Table
* [#1180](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1180) Charts created with openpyxl cannot be styled
* [#1181](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1181) Cannot handle some numpy number types
* [#1182](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1182) Exception when reading unknowable number formats
* [#1186](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1186) Only last formatting rule for a range loaded
* [#1191](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1191) Give MergedCell a value attribute
* [#1193](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1193) Cannot process worksheets with comments
* [#1197](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1197) Cannot process worksheets with both row and page breaks
* [#1204](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1204) Cannot reset dimensions in ReadOnlyWorksheets
* [#1211](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1211) Incorrect descriptor in ParagraphProperties
* [#1213](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1213) Missing hier attribute in PageField raises an exception

# 2.6.0 (2019-02-06)[](#id146 "Link to this heading")

## Bugfixes[](#id147 "Link to this heading")

* [#1162](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1162) Exception on tables with names containing spaces.
* [#1170](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1170) Cannot save files with existing images.

# 2.6.-b1 (2019-01-08)[](#b1-2019-01-08 "Link to this heading")

## Bugfixes[](#id150 "Link to this heading")

* [#1141](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1141) Cannot use read-only mode with stream
* [#1143](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1143) Hyperlinks always set on A1
* [#1151](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1151) Internal row counter not initialised when reading files
* [#1152](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1152) Exception raised on out of bounds date

# 2.6-a1 (2018-11-21)[](#a1-2018-11-21 "Link to this heading")

## Major changes[](#major-changes "Link to this heading")

* Implement robust for merged cells so that these can be formatted the way
  Excel does without confusion. Thanks to Magnus Schieder.

## Minor changes[](#minor-changes "Link to this heading")

* Add support for worksheet scenarios
* Add read support for chartsheets
* Add method for moving ranges of cells on a worksheet
* Drop support for Python 3.4
* Last version to support Python 2.7

## Deprecations[](#id155 "Link to this heading")

* Type inference and coercion for cell values

# 2.5.14 (2019-01-23)[](#id156 "Link to this heading")

## Bugfixes[](#id157 "Link to this heading")

* [#1150](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1150) Correct typo in LineProperties
* [#1142](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1142) Exception raised for unsupported image files
* [#1159](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1159) Exception raised when cannot find source for non-local cache object

## Pull Requests[](#id161 "Link to this heading")

* [PR301](https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/301/) Add support for nested brackets to the tokeniser
* [PR303](https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/301/) Improvements on handling nested brackets in the tokeniser

# 2.5.13 (brown bag)[](#id162 "Link to this heading")

# 2.5.12 (2018-11-29)[](#id163 "Link to this heading")

## Bugfixes[](#id164 "Link to this heading")

* [#1130](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1130) Overwriting default font in Normal style affects library default
* [#1133](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1133) Images not added to anchors.
* [#1134](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1134) Cannot read pivot table formats without dxId
* [#1138](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1138) Repeated registration of simple filter could lead to memory leaks

## Pull Requests[](#id169 "Link to this heading")

* [PR300](https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/300/) Use defusedxml if available

# 2.5.11 (2018-11-21)[](#id170 "Link to this heading")

## Pull Requests[](#id171 "Link to this heading")

* [PR295](https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/295) Improved handling of missing rows
* [PR296](https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/296) Add support for defined names to tokeniser

# 2.5.10 (2018-11-13)[](#id172 "Link to this heading")

## Bugfixes[](#id173 "Link to this heading")

* [#1114](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1114) Empty column dimensions should not be saved.

## Pull Requests[](#id175 "Link to this heading")

* [PR285](https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/285) Tokenizer failure for quoted sheet name in second half of range
* [PR289](https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/289) Improved error detection in ranges.

# 2.5.9 (2018-10-19)[](#id176 "Link to this heading")

## Bugfixes[](#id177 "Link to this heading")

* [#1000](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1000) Clean AutoFilter name definitions
* [#1106](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1106) Attribute missing from Shape object
* [#1109](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1109) Failure to read all DrawingML means workbook can’t be read

## Pull Requests[](#id181 "Link to this heading")

* [PR281](https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/281) Allow newlines in formulae
* [PR284](https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/284) Fix whitespace in front of infix operator in formulae

# 2.5.8 (2018-09-25)[](#id182 "Link to this heading")

* [#877](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/877) Cannot control how missing values are displayed in charts.
* [#948](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/948) Cell references can’t be used for chart titles
* [#1095](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1095) Params in iter\_cols and iter\_rows methods are slightly wrong.

# 2.5.7 (2018-09-13)[](#id186 "Link to this heading")

* [#954](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/954) Sheet title containing % need quoting in references
* [#1047](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1047) Cannot set quote prefix
* [#1093](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1093) Pandas timestamps raise KeyError

# 2.5.6 (2018-08-30)[](#id190 "Link to this heading")

* [#832](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/832) Read-only mode can leave find-handles open when reading dimensions
* [#933](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/933) Set a worksheet directly as active
* [#1086](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1086) Internal row counter not adjusted when rows are deleted or inserted

# 2.5.5 (2018-08-04)[](#id194 "Link to this heading")

## Bugfixes[](#id195 "Link to this heading")

* [#1049](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1049) Files with Mac epoch are read incorrectly
* [#1058](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1058) Cannot copy merged cells
* [#1066](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1066) Cannot access ws.active\_cell

## Pull Requests[](#id199 "Link to this heading")

* [PR267](https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/267/image-read) Introduce read-support for images

# 2.5.4 (2018-06-07)[](#id200 "Link to this heading")

## Bugfixes[](#id201 "Link to this heading")

* [#1025](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1025) Cannot read files with 3D charts.
* [#1030](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1030) Merged cells take a long time to parse

## Minor changes[](#id204 "Link to this heading")

* Improve read support for pivot tables and don’t always create a Filters child for filterColumn objects.
* Support folding rows <<https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/259/fold-rows>>`\_

# 2.5.3 (2018-04-18)[](#id205 "Link to this heading")

## Bugfixes[](#id206 "Link to this heading")

* [#983](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/983) Warning level too aggressive.
* [#1015](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1015) Alignment and protection values not saved for named styles.
* [#1017](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1017) Deleting elements from a legend doesn’t work.
* [#1018](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1018) Index names repeated for every row in dataframe.
* [#1020](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1020) Worksheet protection not being stored.
* [#1023](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1023) Exception raised when reading a tooltip.

# 2.5.2 (2018-04-06)[](#id213 "Link to this heading")

## Bugfixes[](#id214 "Link to this heading")

* [#949](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/949) High memory use when reading text-heavy files.
* [#970](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/970) Copying merged cells copies references.
* [#978](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/978) Cannot set comment size.
* [#985](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/895) Exception when trying to save workbooks with no views.
* [#995](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/995) Cannot delete last row or column.
* [#1002](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1002) Cannot read Drawings containing embedded images.

## Minor changes[](#id221 "Link to this heading")

* Support for dataframes with multiple columns and multiple indices.

# 2.5.1 (2018-03-12)[](#id222 "Link to this heading")

## Bugfixes[](#id223 "Link to this heading")

* [#934](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/934) Headers and footers not included in write-only mode.
* [#960](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/960) Deprecation warning raised when using ad-hoc access in read-only mode.
* [#964](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/964) Not all cells removed when deleting multiple rows.
* [#966](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/966) Cannot read 3d bar chart correctly.
* [#967](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/967) Problems reading some charts.
* [#968](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/968) Worksheets with SHA protection become corrupted after saving.
* [#974](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/974) Problem when deleting ragged rows or columns.
* [#976](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/976) GroupTransforms and GroupShapeProperties have incorrect descriptors
* Make sure that headers and footers in chartsheets are included in the file

# 2.5.0 (2018-01-24)[](#id232 "Link to this heading")

## Minor changes[](#id233 "Link to this heading")

* Correct definition for Connection Shapes. Related to # 958

# 2.5.0-b2 (2018-01-19)[](#b2-2018-01-19 "Link to this heading")

## Bugfixes[](#id234 "Link to this heading")

* [#915](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/915) TableStyleInfo has no required attributes
* [#925](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/925) Cannot read files with 3D drawings
* [#926](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/926) Incorrect version check in installer
* Cell merging uses transposed parameters
* [#928](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/928) ExtLst missing keyword for PivotFields
* [#932](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/932) Inf causes problems for Excel
* [#952](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/952) Cannot load table styles with custom names

## Major Changes[](#id241 "Link to this heading")

* You can now insert and delete rows and columns in worksheets

## Minor Changes[](#id242 "Link to this heading")

* pip now handles which Python versions can be used.

# 2.5.0-b1 (2017-10-19)[](#b1-2017-10-19 "Link to this heading")

## Bugfixes[](#id243 "Link to this heading")

* [#812](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/812) Explicitly support for multiple cell ranges in conditonal formatting
* [#827](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/827) Non-contiguous cell ranges in validators get merged
* [#837](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/837) Empty data validators create invalid Excel files
* [#860](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/860) Large validation ranges use lots of memory
* [#876](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/876) Unicode in chart axes not handled correctly in Python 2
* [#882](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/882) ScatterCharts have defective axes
* [#885](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/885) Charts with empty numVal elements cannot be read
* [#894](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/894) Scaling options from existing files ignored
* [#895](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/895) Charts with PivotSource cannot be read
* [#903](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/903) Cannot read gradient fills
* [#904](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/904) Quotes in number formats could be treated as datetimes

## Major Changes[](#id255 "Link to this heading")

worksheet.cell() no longer accepts a coordinate parameter. The syntax is now ws.cell(row, column, value=None)

## Minor Changes[](#id256 "Link to this heading")

Added CellRange and MultiCellRange types (thanks to Laurent LaPorte for the
suggestion) as a utility type for things like data validations, conditional
formatting and merged cells.

## Deprecations[](#id257 "Link to this heading")

ws.merged\_cell\_ranges has been deprecated because MultiCellRange provides sufficient functionality

# 2.5.0-a3 (2017-08-14)[](#a3-2017-08-14 "Link to this heading")

## Bugfixes[](#id258 "Link to this heading")

* [#848](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/848) Reading workbooks with Pie Charts raises an exception
* [#857](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/857) Pivot Tables without Worksheet Sources raise an exception

# 2.5.0-a2 (2017-06-25)[](#a2-2017-06-25 "Link to this heading")

## Major Changes[](#id261 "Link to this heading")

* Read support for charts

## Bugfixes[](#id262 "Link to this heading")

* [#833](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/833) Cannot access chartsheets by title
* [#834](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/834) Preserve workbook views
* [#841](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/841) Incorrect classification of a datetime

# 2.5.0-a1 (2017-05-30)[](#a1-2017-05-30 "Link to this heading")

## Compatibility[](#compatibility "Link to this heading")

* Dropped support for Python 2.6 and 3.3. openpyxl will not run with Python 2.6

## Major Changes[](#id266 "Link to this heading")

* Read/write support for pivot tables

## Deprecations[](#id267 "Link to this heading")

* Dropped the anchor method from images and additional constructor arguments

## Bugfixes[](#id268 "Link to this heading")

* [#779](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/779) Fails to recognise Chinese date format`
* [#828](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/828) Include hidden cells in charts`

## Pull requests[](#id271 "Link to this heading")

* [163](https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/163) Improved GradientFill

## Minor changes[](#id273 "Link to this heading")

* Remove deprecated methods from Cell
* Remove deprecated methods from Worksheet
* Added read/write support for the datetime type for cells

# 2.4.11 (2018-01-24)[](#id274 "Link to this heading")

* #957 <https://foss.heptapod.net/openpyxl/openpyxl/-/issues/957> Relationship type for tables is borked

# 2.4.10 (2018-01-19)[](#id275 "Link to this heading")

## Bugfixes[](#id276 "Link to this heading")

* #912 <https://foss.heptapod.net/openpyxl/openpyxl/-/issues/912> Copying objects uses shallow copy
* #921 <https://foss.heptapod.net/openpyxl/openpyxl/-/issues/921> API documentation not generated automatically
* #927 <https://foss.heptapod.net/openpyxl/openpyxl/-/issues/927> Exception raised when adding coloured borders together
* #931 <https://foss.heptapod.net/openpyxl/openpyxl/-/issues/931> Number formats not correctly deduplicated

## Pull requests[](#id277 "Link to this heading")

* 203 <https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/203/> Correction to worksheet protection description
* 210 <https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/210/> Some improvements to the API docs
* 211 <https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/211/> Improved deprecation decorator
* 218 <https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/218/> Fix problems with deepcopy

# 2.4.9 (2017-10-19)[](#id278 "Link to this heading")

## Bugfixes[](#id279 "Link to this heading")

* [#809](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/809) Incomplete documentation of copy\_worksheet method
* [#811](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/811) Scoped definedNames not removed when worksheet is deleted
* [#824](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/824) Raise an exception if a chart is used in multiple sheets
* [#842](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/842) Non-ASCII table column headings cause an exception in Python 2
* [#846](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/846) Conditional formats not supported in write-only mode
* [#849](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/849) Conditional formats with no sqref cause an exception
* [#859](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/859) Headers that start with a number conflict with font size
* [#902](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/902) TableStyleElements don’t always have a condtional format
* [#908](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/908) Read-only mode sometimes returns too many cells

## Pull requests[](#id289 "Link to this heading")

* [#179](https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/179) Cells kept in a set
* [#180](https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/180) Support for Workbook protection
* [#182](https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/182) Read support for page breaks
* [#183](https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/183) Improve documentation of copy\_worksheet method
* [#198](https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/198) Fix for #908

# 2.4.8 (2017-05-30)[](#id295 "Link to this heading")

## Bugfixes[](#id296 "Link to this heading")

* AutoFilter.sortState being assignd to the ws.sortState
* [#766](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/666) Sheetnames with apostrophes need additional escaping
* [#729](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/729) Cannot open files created by Microsoft Dynamics
* [#819](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/819) Negative percents not case correctly
* [#821](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/821) Runtime imports can cause deadlock
* [#855](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/855) Print area containing only columns leads to corrupt file

## Minor changes[](#id302 "Link to this heading")

* Preserve any table styles

# 2.4.7 (2017-04-24)[](#id303 "Link to this heading")

## Bugfixes[](#id304 "Link to this heading")

* [#807](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/807) Sample files being included by mistake in sdist

# 2.4.6 (2017-04-14)[](#id306 "Link to this heading")

## Bugfixes[](#id307 "Link to this heading")

* [#776](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/776) Cannot apply formatting to plot area
* [#780](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/780) Exception when element attributes are Python keywords
* [#781](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/781) Exception raised when saving files with styled columns
* [#785](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/785) Number formats for data labels are incorrect
* [#788](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/788) Worksheet titles not quoted in defined names
* [#800](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/800) Font underlines not read correctly

# 2.4.5 (2017-03-07)[](#id314 "Link to this heading")

## Bugfixes[](#id315 "Link to this heading")

* [#750](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/750) Adding images keeps file handles open
* [#772](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/772) Exception for column-only ranges
* [#773](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/773) Cannot copy worksheets with non-ascii titles on Python 2

## Pull requests[](#id319 "Link to this heading")

* [161](https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/161) Support for non-standard names for Workbook part.
* [162](https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/162) Documentation correction

# 2.4.4 (2017-02-23)[](#id322 "Link to this heading")

## Bugfixes[](#id323 "Link to this heading")

* [#673](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/673) Add close method to workbooks
* [#762](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/762) openpyxl can create files with invalid style indices
* [#729](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/729) Allow images in write-only mode
* [#744](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/744) Rounded corners for charts
* [#747](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/747) Use repr when handling non-convertible objects
* [#764](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/764) Hashing function is incorrect
* [#765](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/765) Named styles share underlying array

## Minor Changes[](#id331 "Link to this heading")

* Add roundtrip support for worksheet tables.

## Pull requests[](#id332 "Link to this heading")

* [160](https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/160) Don’t init mimetypes more than once.

# 2.4.3 (unreleased)[](#unreleased "Link to this heading")

bad release

# 2.4.2 (2017-01-31)[](#id334 "Link to this heading")

## Bug fixes[](#id335 "Link to this heading")

* [#727](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/727) DeprecationWarning is incorrect
* [#734](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/734) Exception raised if userName is missing
* [#739](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/739) Always provide a date1904 attribute
* [#740](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/740) Hashes should be stored as Base64
* [#743](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/743) Print titles broken on sheetnames with spaces
* [#748](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/748) Workbook breaks when active sheet is removed
* [#754](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/754) Incorrect descriptor for Filter values
* [#756](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/756) Potential XXE vulerability
* [#758](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/758) Cannot create files with page breaks and charts
* [#759](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/759) Problems with worksheets with commas in their titles

## Minor Changes[](#id346 "Link to this heading")

* Add unicode support for sheet name incrementation.

# 2.4.1 (2016-11-23)[](#id347 "Link to this heading")

## Bug fixes[](#id348 "Link to this heading")

* [#643](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/643) Make checking for duplicate sheet titles case insensitive
* [#647](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/647) Trouble handling LibreOffice files with named styles
* [#687](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/682) Directly assigned new named styles always refer to “Normal”
* [#690](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/690) Cannot parse print titles with multiple sheet names
* [#691](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/691) Cannot work with macro files created by LibreOffice
* Prevent duplicate differential styles
* [#694](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/694) Allow sheet titles longer than 31 characters
* [#697](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/697) Cannot unset hyperlinks
* [#699](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/699) Exception raised when format objects use cell references
* [#703](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/703) Copy height and width when copying comments
* [#705](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/705) Incorrect content type for VBA macros
* [#707](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/707) IndexError raised in read-only mode when accessing individual cells
* [#711](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/711) Files with external links become corrupted
* [#715](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/715) Cannot read files containing macro sheets
* [#717](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/717) Details from named styles not preserved when reading files
* [#722](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/722) Remove broken Print Title and Print Area definitions

## Minor changes[](#id364 "Link to this heading")

* Add support for Python 3.6
* Correct documentation for headers and footers

## Deprecations[](#id365 "Link to this heading")

Worksheet methods get\_named\_range() and get\_sqaured\_range()

## Bug fixes[](#id366 "Link to this heading")

# 2.4.0 (2016-09-15)[](#id367 "Link to this heading")

## Bug fixes[](#id368 "Link to this heading")

* [#652](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/652) Exception raised when epoch is 1904
* [#642](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/642) Cannot handle unicode in headers and footers in Python 2
* [#646](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/646) Cannot handle unicode sheetnames in Python 2
* [#658](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/658) Chart styles, and axis units should not be 0
* [#663](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/663) Strings in external workbooks not unicode

## Major changes[](#id374 "Link to this heading")

* Add support for builtin styles and include one for Pandas

## Minor changes[](#id375 "Link to this heading")

* Add a keep\_links option to load\_workbook. External links contain cached
  copies of the external workbooks. If these are big it can be advantageous to
  be able to disable them.
* Provide an example for using cell ranges in DataValidation.
* PR 138 - add copy support to comments.

# 2.4.0-b1 (2016-06-08)[](#b1-2016-06-08 "Link to this heading")

## Minor changes[](#id376 "Link to this heading")

* Add an the alias hide\_drop\_down to DataValidation for showDropDown because that is how Excel works.

## Bug fixes[](#id377 "Link to this heading")

* [#625](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/625) Exception raises when inspecting EmptyCells in read-only mode
* [#547](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/547) Functions for handling OOXML “escaped” ST\_XStrings
* [#629](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/629) Row Dimensions not supported in write-only mode
* [#530](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/530) Problems when removing worksheets with charts
* [#630](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/630) Cannot use SheetProtection in write-only mode

## Features[](#features "Link to this heading")

* Add write support for worksheet tables

# 2.4.0-a1 (2016-04-11)[](#a1-2016-04-11 "Link to this heading")

## Minor changes[](#id383 "Link to this heading")

* Remove deprecated methods from DataValidation
* Remove deprecated methods from PrintPageSetup
* Convert AutoFilter to Serialisable and extend support for filters
* Add support for SortState
* Removed use\_iterators keyword when loading workbooks. Use read\_only instead.
* Removed optimized\_write keyword for new workbooks. Use write\_only instead.
* Improve print title support
* Add print area support
* New implementation of defined names
* New implementation of page headers and footers
* Add support for Python’s NaN
* Added iter\_cols method for worksheets
* ws.rows and ws.columns now always return generators and start at the top of the worksheet
* Add a values property for worksheets
* Default column width changed to 8 as per the specification

## Deprecations[](#id384 "Link to this heading")

* Cell anchor method
* Worksheet point\_pos method
* Worksheet add\_print\_title method
* Worksheet HeaderFooter attribute, replaced by individual ones
* Flatten function for cells
* Workbook get\_named\_range, add\_named\_range, remove\_named\_range, get\_sheet\_names, get\_sheet\_by\_name
* Comment text attribute
* Use of range strings deprecated for ws.iter\_rows()
* Use of coordinates deprecated for ws.cell()
* Deprecate .copy() method for StyleProxy objects

## Bug fixes[](#id385 "Link to this heading")

* [#152](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/152) Hyperlinks lost when reading files
* [#171](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/171) Add function for copying worksheets
* [#386](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/386) Cells with inline strings considered empty
* [#397](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/397) Add support for ranges of rows and columns
* [#446](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/446) Workbook with definedNames corrupted by openpyxl
* [#481](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/481) “safe” reserved ranges are not read from workbooks
* [#501](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/501) Discarding named ranges can lead to corrupt files
* [#574](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/574) Exception raised when using the class method to parse Relationships
* [#579](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/579) Crashes when reading defined names with no content
* [#597](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/597) Cannot read worksheets without coordinates
* [#617](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/617) Customised named styles not correctly preserved

# 2.3.5 (2016-04-11)[](#id397 "Link to this heading")

## Bug fixes[](#id398 "Link to this heading")

* [#618](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/618) Comments not written in write-only mode

# 2.3.4 (2016-03-16)[](#id400 "Link to this heading")

## Bug fixes[](#id401 "Link to this heading")

* [#594](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/594) Content types might be missing when keeping VBA
* [#599](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/599) Cells with only one cell look empty
* [#607](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/607) Serialise NaN as ‘’

## Minor changes[](#id405 "Link to this heading")

* Preserve the order of external references because formualae use numerical indices.
* Typo corrected in cell unit tests (PR 118)

# 2.3.3 (2016-01-18)[](#id406 "Link to this heading")

## Bug fixes[](#id407 "Link to this heading")

* [#540](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/540) Cannot read merged cells in read-only mode
* [#565](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/565) Empty styled text blocks cannot be parsed
* [#569](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/569) Issue warning rather than raise Exception raised for unparsable definedNames
* [#575](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/575) Cannot open workbooks with embdedded OLE files
* [#584](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/584) Exception when saving borders with attributes

## Minor changes[](#id413 "Link to this heading")

* [PR 103](https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/103/) Documentation about chart scaling and axis limits
* Raise an exception when trying to copy cells from other workbooks.

# 2.3.2 (2015-12-07)[](#id414 "Link to this heading")

## Bug fixes[](#id415 "Link to this heading")

* [#554](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/554) Cannot add comments to a worksheet when preserving VBA
* [#561](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/561) Exception when reading phonetic text
* [#562](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/562) DARKBLUE is the same as RED
* [#563](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/563) Minimum for row and column indexes not enforced

## Minor changes[](#id420 "Link to this heading")

* [PR 97](https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/97/) One VML file per worksheet.
* [PR 96](https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/96/) Correct descriptor for CharacterProperties.rtl
* [#498](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/498) Metadata is not essential to use the package.

# 2.3.1 (2015-11-20)[](#id422 "Link to this heading")

## Bug fixes[](#id423 "Link to this heading")

* [#534](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/534) Exception when using columns property in read-only mode.
* [#536](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/536) Incorrectly handle comments from Google Docs files.
* [#539](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/539) Flexible value types for conditional formatting.
* [#542](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/542) Missing content types for images.
* [#543](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/543) Make sure images fit containers on all OSes.
* [#544](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/544) Gracefully handle missing cell styles.
* [#546](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/546) ExternalLink duplicated when editing a file with macros.
* [#548](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/548) Exception with non-ASCII worksheet titles
* [#551](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/551) Combine multiple LineCharts

## Minor changes[](#id433 "Link to this heading")

* [PR 88](https://foss.heptapod.net/openpyxl/openpyxl/-/merge_requests/88/) Fix page margins in parser.

# 2.3.0 (2015-10-20)[](#id434 "Link to this heading")

## Major changes[](#id435 "Link to this heading")

* Support the creation of chartsheets

## Bug fixes[](#id436 "Link to this heading")

* [#532](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/532) Problems when cells have no style in read-only mode.

## Minor changes[](#id438 "Link to this heading")

* PR 79 Make PlotArea editable in charts
* Use graphicalProperties as the alias for spPr

# 2.3.0-b2 (2015-09-04)[](#b2-2015-09-04 "Link to this heading")

## Bug fixes[](#id439 "Link to this heading")

* [#488](https://bitbucket.org/openpyxl/openpyxl/issue/488) Support hashValue attribute for sheetProtection
* [#493](https://bitbucket.org/openpyxl/openpyxl/issue/493) Warn that unsupported extensions will be dropped
* [#494](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/494/) Cells with exponentials causes a ValueError
* [#497](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/497/) Scatter charts are broken
* [#499](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/499/) Inconsistent conversion of localised datetimes
* [#500](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/500/) Adding images leads to unreadable files
* [#509](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/509/) Improve handling of sheet names
* [#515](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/515/) Non-ascii titles have bad repr
* [#516](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/516/) Ignore unassigned worksheets

## Minor changes[](#id449 "Link to this heading")

* Worksheets are now iterable by row.
* Assign individual cell styles only if they are explicitly set.

# 2.3.0-b1 (2015-06-29)[](#b1-2015-06-29 "Link to this heading")

## Major changes[](#id450 "Link to this heading")

* Shift to using (row, column) indexing for cells. Cells will at some point *lose* coordinates.
* New implementation of conditional formatting. Databars now partially preserved.
* et\_xmlfile is now a standalone library.
* Complete rewrite of chart package
* Include a tokenizer for fomulae to be able to adjust cell references in them. PR 63

## Minor changes[](#id451 "Link to this heading")

* Read-only and write-only worksheets renamed.
* Write-only workbooks support charts and images.
* [PR76](https://bitbucket.org/openpyxl/openpyxl/pull-request/76) Prevent comment images from conflicting with VBA

## Bug fixes[](#id452 "Link to this heading")

* [#81](https://bitbucket.org/openpyxl/openpyxl/issue/81) Support stacked bar charts
* [#88](https://bitbucket.org/openpyxl/openpyxl/issue/88) Charts break hyperlinks
* [#97](https://bitbucket.org/openpyxl/openpyxl/issue/97) Pie and combination charts
* [#99](https://bitbucket.org/openpyxl/openpyxl/issue/99) Quote worksheet names in chart references
* [#150](https://bitbucket.org/openpyxl/openpyxl/issue/150) Support additional chart options
* [#172](https://bitbucket.org/openpyxl/openpyxl/issue/172) Support surface charts
* [#381](https://bitbucket.org/openpyxl/openpyxl/issue/381) Preserve named styles
* [#470](https://bitbucket.org/openpyxl/openpyxl/issue/470) Adding more than 10 worksheets with the same name leads to duplicates sheet names and an invalid file

# 2.2.6 (unreleased)[](#id461 "Link to this heading")

## Bug fixes[](#id462 "Link to this heading")

* [#502](https://bitbucket.org/openpyxl/openpyxl/issue/502) Unexpected keyword “mergeCell”
* [#503](https://bitbucket.org/openpyxl/openpyxl/issue/503) tostring missing in dump\_worksheet
* [#506](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/506) Non-ASCII formulae cannot be parsed
* [#508](https://foss.heptapod.net/openpyxl/openpyxl/-/issues/508) Cannot save files with coloured tabs
* Regex for ignoring named ranges is wrong (character class instead of prefix)

# 2.2.5 (2015-06-29)[](#id467 "Link to this heading")

## Bug fixes[](#id468 "Link to this heading")

* [#463](https://bitbucket.org/openpyxl/openpyxl/issue/463) Unexpected keyword “mergeCell”
* [#484](https://bitbucket.org/openpyxl/openpyxl/issue/484) Unusual dimensions breaks read-only mode
* [#485](https://bitbucket.org/openpyxl/openpyxl/issue/485) Move return out of loop

# 2.2.4 (2015-06-17)[](#id472 "Link to this heading")

## Bug fixes[](#id473 "Link to this heading")

* [#464](https://bitbucket.org/openpyxl/openpyxl/issue/464) Cannot use images when preserving macros
* [#465](https://bitbucket.org/openpyxl/openpyxl/issue/465) ws.cell() returns an empty cell on read-only workbooks
* [#467](https://bitbucket.org/openpyxl/openpyxl/issue/467) Cannot edit a file with ActiveX components
* [#471](https://bitbucket.org/openpyxl/openpyxl/issue/471) Sheet properties elements must be in order
* [#475](https://bitbucket.org/openpyxl/openpyxl/issue/475) Do not redefine class \_\_slots\_\_ in subclasses
* [#477](https://bitbucket.org/openpyxl/openpyxl/issue/477) Write-only support for SheetProtection
* [#478](https://bitbucket.org/openpyxl/openpyxl/issue/477) Write-only support for DataValidation
* Improved regex when checking for datetime formats

# 2.2.3 (2015-05-26)[](#id481 "Link to this heading")

## Bug fixes[](#id482 "Link to this heading")

* [#451](https://bitbucket.org/openpyxl/openpyxl/issue/451) fitToPage setting ignored
* [#458](https://bitbucket.org/openpyxl/openpyxl/issue/458) Trailing spaces lost when saving files.
* [#459](https://bitbucket.org/openpyxl/openpyxl/issue/459) setup.py install fails with Python 3
* [#462](https://bitbucket.org/openpyxl/openpyxl/issue/462) Vestigial rId conflicts when adding charts, images or comments
* [#455](https://bitbucket.org/openpyxl/openpyxl/issue/455) Enable Zip64 extensions for all versions of Python

# 2.2.2 (2015-04-28)[](#id488 "Link to this heading")

## Bug fixes[](#id489 "Link to this heading")

* [#447](https://bitbucket.org/openpyxl/openpyxl/issue/447) Uppercase datetime number formats not recognised.
* [#453](https://bitbucket.org/openpyxl/openpyxl/issue/453) Borders broken in shared\_styles.

# 2.2.1 (2015-03-31)[](#id492 "Link to this heading")

## Minor changes[](#id493 "Link to this heading")

* [PR54](https://bitbucket.org/openpyxl/openpyxl/pull-request/54) Improved precision on times near midnight.
* [PR55](https://bitbucket.org/openpyxl/openpyxl/pull-request/55) Preserve macro buttons

## Bug fixes[](#id494 "Link to this heading")

* [#429](https://bitbucket.org/openpyxl/openpyxl/issue/429) Workbook fails to load because header and footers cannot be parsed.
* [#433](https://bitbucket.org/openpyxl/openpyxl/issue/433) File-like object with encoding=None
* [#434](https://bitbucket.org/openpyxl/openpyxl/issue/434) SyntaxError when writing page breaks.
* [#436](https://bitbucket.org/openpyxl/openpyxl/issue/436) Read-only mode duplicates empty rows.
* [#437](https://bitbucket.org/openpyxl/openpyxl/issue/437) Cell.offset raises an exception
* [#438](https://bitbucket.org/openpyxl/openpyxl/issue/438) Cells with pivotButton and quotePrefix styles cannot be read
* [#440](https://bitbucket.org/openpyxl/openpyxl/issue/440) Error when customised versions of builtin formats
* [#442](https://bitbucket.org/openpyxl/openpyxl/issue/442) Exception raised when a fill element contains no children
* [#444](https://bitbucket.org/openpyxl/openpyxl/issue/442) Styles cannot be copied

# 2.2.0 (2015-03-11)[](#id504 "Link to this heading")

## Bug fixes[](#id505 "Link to this heading")

* [#415](https://bitbucket.org/openpyxl/openpyxl/issue/415) Improved exception when passing in invalid in memory files.

# 2.2.0-b1 (2015-02-18)[](#b1-2015-02-18 "Link to this heading")

## Major changes[](#id507 "Link to this heading")

* Cell styles deprecated, use formatting objects (fonts, fills, borders, etc.) directly instead
* Charts will no longer try and calculate axes by default
* Support for template file types - PR21
* Moved ancillary functions and classes into utils package - single place of reference
* [PR 34](https://bitbucket.org/openpyxl/openpyxl/pull-request/34/) Fully support page setup
* Removed SAX-based XML Generator. Special thanks to Elias Rabel for implementing xmlfile for xml.etree
* Preserve sheet view definitions in existing files (frozen panes, zoom, etc.)

## Bug fixes[](#id508 "Link to this heading")

* [#103](https://bitbucket.org/openpyxl/openpyxl/issue/103) Set the zoom of a sheet
* [#199](https://bitbucket.org/openpyxl/openpyxl/issue/199) Hide gridlines
* [#215](https://bitbucket.org/openpyxl/openpyxl/issue/215) Preserve sheet view setings
* [#262](https://bitbucket.org/openpyxl/openpyxl/issue/262) Set the zoom of a sheet
* [#392](https://bitbucket.org/openpyxl/openpyxl/issue/392) Worksheet header not read
* [#387](https://bitbucket.org/openpyxl/openpyxl/issue/387) Cannot read files without styles.xml
* [#410](https://bitbucket.org/openpyxl/openpyxl/issue/410) Exception when preserving whitespace in strings
* [#417](https://bitbucket.org/openpyxl/openpyxl/issue/417) Cannot create print titles
* [#420](https://bitbucket.org/openpyxl/openpyxl/issue/420) Rename confusing constants
* [#422](https://bitbucket.org/openpyxl/openpyxl/issue/422) Preserve color index in a workbook if it differs from the standard

## Minor changes[](#id519 "Link to this heading")

* Use a 2-way cache for column index lookups
* Clean up tests in cells
* [PR 40](https://bitbucket.org/openpyxl/openpyxl/pull-request/40/) Support frozen panes and autofilter in write-only mode
* Use ws.calculate\_dimension(force=True) in read-only mode for unsized worksheets

# 2.1.5 (2015-02-18)[](#id520 "Link to this heading")

## Bug fixes[](#id521 "Link to this heading")

* [#403](https://bitbucket.org/openpyxl/openpyxl/issue/403) Cannot add comments in write-only mode
* [#401](https://bitbucket.org/openpyxl/openpyxl/issue/401) Creating cells in an empty row raises an exception
* [#408](https://bitbucket.org/openpyxl/openpyxl/issue/408) from\_excel adjustment for Julian dates 1 < x < 60
* [#409](https://bitbucket.org/openpyxl/openpyxl/issue/409) refersTo is an optional attribute

## Minor changes[](#id526 "Link to this heading")

* Allow cells to be appended to standard worksheets for code compatibility with write-only mode.

# 2.1.4 (2014-12-16)[](#id527 "Link to this heading")

## Bug fixes[](#id528 "Link to this heading")

* [#393](https://bitbucket.org/openpyxl/openpyxl/issue/393) IterableWorksheet skips empty cells in rows
* [#394](https://bitbucket.org/openpyxl/openpyxl/issue/394) Date format is applied to all columns (while only first column contains dates)
* [#395](https://bitbucket.org/openpyxl/openpyxl/issue/395) temporary files not cleaned properly
* [#396](https://bitbucket.org/openpyxl/openpyxl/issue/396) Cannot write “=” in Excel file
* [#398](https://bitbucket.org/openpyxl/openpyxl/issue/398) Cannot write empty rows in write-only mode with LXML installed

## Minor changes[](#id534 "Link to this heading")

* Add relation namespace to root element for compatibility with iWork
* Serialize comments relation in LXML-backend

# 2.1.3 (2014-12-09)[](#id535 "Link to this heading")

## Minor changes[](#id536 "Link to this heading")

* [PR 31](https://bitbucket.org/openpyxl/openpyxl/pull-request/31/) Correct tutorial
* [PR 32](https://bitbucket.org/openpyxl/openpyxl/pull-request/32/) See #380
* [PR 37](https://bitbucket.org/openpyxl/openpyxl/pull-request/37/) Bind worksheet to ColumnDimension objects

## Bug fixes[](#id537 "Link to this heading")

* [#379](https://bitbucket.org/openpyxl/openpyxl/issue/379) ws.append() doesn’t set RowDimension Correctly
* [#380](https://bitbucket.org/openpyxl/openpyxl/issue/379) empty cells formatted as datetimes raise exceptions

# 2.1.2 (2014-10-23)[](#id540 "Link to this heading")

## Minor changes[](#id541 "Link to this heading")

* [PR 30](https://bitbucket.org/openpyxl/openpyxl/pull-request/30/) Fix regex for positive exponentials
* [PR 28](https://bitbucket.org/openpyxl/openpyxl/pull-request/28/) Fix for #328

## Bug fixes[](#id542 "Link to this heading")

* [#120](https://bitbucket.org/openpyxl/openpyxl/issue/120), [#168](https://bitbucket.org/openpyxl/openpyxl/issue/168) defined names with formulae raise exceptions, [#292](https://bitbucket.org/openpyxl/openpyxl/issue/292)
* [#328](https://bitbucket.org/openpyxl/openpyxl/issue/328/) ValueError when reading cells with hyperlinks
* [#369](https://bitbucket.org/openpyxl/openpyxl/issue/369) IndexError when reading definedNames
* [#372](https://bitbucket.org/openpyxl/openpyxl/issue/372) number\_format not consistently applied from styles

# 2.1.1 (2014-10-08)[](#id549 "Link to this heading")

## Minor changes[](#id550 "Link to this heading")

* PR 20 Support different workbook code names
* Allow auto\_axis keyword for ScatterCharts

## Bug fixes[](#id551 "Link to this heading")

* [#332](https://bitbucket.org/openpyxl/openpyxl/issue/332) Fills lost in ConditionalFormatting
* [#360](https://bitbucket.org/openpyxl/openpyxl/issue/360) Support value=”none” in attributes
* [#363](https://bitbucket.org/openpyxl/openpyxl/issue/363) Support undocumented value for textRotation
* [#364](https://bitbucket.org/openpyxl/openpyxl/issue/364) Preserve integers in read-only mode
* [#366](https://bitbucket.org/openpyxl/openpyxl/issue/366) Complete read support for DataValidation
* [#367](https://bitbucket.org/openpyxl/openpyxl/issue/367) Iterate over unsized worksheets

# 2.1.0 (2014-09-21)[](#id558 "Link to this heading")

## Major changes[](#id559 "Link to this heading")

* “read\_only” and “write\_only” new flags for workbooks
* Support for reading and writing worksheet protection
* Support for reading hidden rows
* Cells now manage their styles directly
* ColumnDimension and RowDimension object manage their styles directly
* Use xmlfile for writing worksheets if available - around 3 times faster
* Datavalidation now part of the worksheet package

## Minor changes[](#id560 "Link to this heading")

* Number formats are now just strings
* Strings can be used for RGB and aRGB colours for Fonts, Fills and Borders
* Create all style tags in a single pass
* Performance improvement when appending rows
* Cleaner conversion of Python to Excel values
* PR6 reserve formatting for empty rows
* standard worksheets can append from ranges and generators

## Bug fixes[](#id561 "Link to this heading")

* [#153](https://bitbucket.org/openpyxl/openpyxl/issue/153) Cannot read visibility of sheets and rows
* [#181](https://bitbucket.org/openpyxl/openpyxl/issue/181) No content type for worksheets
* [241](https://bitbucket.org/openpyxl/openpyxl/issue/241) Cannot read sheets with inline strings
* [322](https://bitbucket.org/openpyxl/openpyxl/issue/322) 1-indexing for merged cells
* [339](https://bitbucket.org/openpyxl/openpyxl/issue/339) Correctly handle removal of cell protection
* [341](https://bitbucket.org/openpyxl/openpyxl/issue/341) Cells with formulae do not round-trip
* [347](https://bitbucket.org/openpyxl/openpyxl/issue/347) Read DataValidations
* [353](https://bitbucket.org/openpyxl/openpyxl/issue/353) Support Defined Named Ranges to external workbooks

# 2.0.5 (2014-08-08)[](#id570 "Link to this heading")

## Bug fixes[](#id571 "Link to this heading")

* [#348](https://bitbucket.org/openpyxl/openpyxl/issue/348) incorrect casting of boolean strings
* [#349](https://bitbucket.org/openpyxl/openpyxl/issue/349) roundtripping cells with formulae

# 2.0.4 (2014-06-25)[](#id574 "Link to this heading")

## Minor changes[](#id575 "Link to this heading")

* Add a sample file illustrating colours

## Bug fixes[](#id576 "Link to this heading")

* [#331](https://bitbucket.org/openpyxl/openpyxl/issue/331) DARKYELLOW was incorrect
* Correctly handle extend attribute for fonts

# 2.0.3 (2014-05-22)[](#id578 "Link to this heading")

## Minor changes[](#id579 "Link to this heading")

* Updated docs

## Bug fixes[](#id580 "Link to this heading")

* [#319](https://bitbucket.org/openpyxl/openpyxl/issue/319) Cannot load Workbooks with vertAlign styling for fonts

# 2.0.2 (2014-05-13)[](#id582 "Link to this heading")

# 2.0.1 (2014-05-13) brown bag[](#id583 "Link to this heading")

# 2.0.0 (2014-05-13) brown bag[](#id584 "Link to this heading")

## Major changes[](#id585 "Link to this heading")

* This is last release that will support Python 3.2
* Cells are referenced with 1-indexing: A1 == cell(row=1, column=1)
* Use jdcal for more efficient and reliable conversion of datetimes
* Significant speed up when reading files
* Merged immutable styles
* Type inference is disabled by default
* RawCell renamed ReadOnlyCell
* ReadOnlyCell.internal\_value and ReadOnlyCell.value now behave the same as Cell
* Provide no size information on unsized worksheets
* Lower memory footprint when reading files

## Minor changes[](#id586 "Link to this heading")

* All tests converted to pytest
* Pyflakes used for static code analysis
* Sample code in the documentation is automatically run
* Support GradientFills
* BaseColWidth set

## Pull requests[](#id587 "Link to this heading")

* #70 Add filterColumn, sortCondition support to AutoFilter
* #80 Reorder worksheets parts
* #82 Update API for conditional formatting
* #87 Add support for writing Protection styles, others
* #89 Better handling of content types when preserving macros

## Bug fixes[](#id588 "Link to this heading")

* [#46](https://bitbucket.org/openpyxl/openpyxl/issue/46) ColumnDimension style error
* [#86](https://bitbucket.org/openpyxl/openpyxl/issue/86) reader.worksheet.fast\_parse sets booleans to integers
* [#98](https://bitbucket.org/openpyxl/openpyxl/issue/98) Auto sizing column widths does not work
* [#137](https://bitbucket.org/openpyxl/openpyxl/issue/137) Workbooks with chartsheets
* [#185](https://bitbucket.org/openpyxl/openpyxl/issue/185) Invalid PageMargins
* [#230](https://bitbucket.org/openpyxl/openpyxl/issue/230) Using v in cells creates invalid files
* [#243](https://bitbucket.org/openpyxl/openpyxl/issue/243) - IndexError when loading workbook
* [#263](https://bitbucket.org/openpyxl/openpyxl/issue/263) - Forded conversion of line breaks
* [#267](https://bitbucket.org/openpyxl/openpyxl/issue/267) - Raise exceptions when passed invalid types
* [#270](https://bitbucket.org/openpyxl/openpyxl/issue/270) - Cannot open files which use non-standard sheet names or reference Ids
* [#269](https://bitbucket.org/openpyxl/openpyxl/issue/269) - Handling unsized worksheets in IterableWorksheet
* [#270](https://bitbucket.org/openpyxl/openpyxl/issue/270) - Handling Workbooks with non-standard references
* [#275](https://bitbucket.org/openpyxl/openpyxl/issue/275) - Handling auto filters where there are only custom filters
* [#277](https://bitbucket.org/openpyxl/openpyxl/issue/277) - Harmonise chart and cell coordinates
* [#280](https://bitbucket.org/openpyxl/openpyxl/issue/280)- Explicit exception raising for invalid characters
* [#286](https://bitbucket.org/openpyxl/openpyxl/issue/286) - Optimized writer can not handle a datetime.time value
* [#296](https://bitbucket.org/openpyxl/openpyxl/issue/296) - Cell coordinates not consistent with documentation
* [#300](https://bitbucket.org/openpyxl/openpyxl/issue/300) - Missing column width causes load\_workbook() exception
* [#304](https://bitbucket.org/openpyxl/openpyxl/issue/304) - Handling Workbooks with absolute paths for worksheets (from Sharepoint)

# 1.8.6 (2014-05-05)[](#id608 "Link to this heading")

## Minor changes[](#id609 "Link to this heading")

Fixed typo for import Elementtree

## Bugfixes[](#id610 "Link to this heading")

* [#279](https://bitbucket.org/openpyxl/openpyxl/issue/279) Incorrect path for comments files on Windows

# 1.8.5 (2014-03-25)[](#id612 "Link to this heading")

## Minor changes[](#id613 "Link to this heading")

* The ‘=’ string is no longer interpreted as a formula
* When a client writes empty xml tags for cells (e.g. <c r=’A1’></c>), reader will not crash

# 1.8.4 (2014-02-25)[](#id614 "Link to this heading")

## Bugfixes[](#id615 "Link to this heading")

* [#260](https://bitbucket.org/openpyxl/openpyxl/issue/260) better handling of undimensioned worksheets
* [#268](https://bitbucket.org/openpyxl/openpyxl/issue/268) non-ascii in formualae
* [#282](https://bitbucket.org/openpyxl/openpyxl/issue/282) correct implementation of register\_namepsace for Python 2.6

# 1.8.3 (2014-02-09)[](#id619 "Link to this heading")

## Major changes[](#id620 "Link to this heading")

Always parse using cElementTree

## Minor changes[](#id621 "Link to this heading")

Slight improvements in memory use when parsing

* [#256](https://bitbucket.org/openpyxl/openpyxl/issue/256) - error when trying to read comments with optimised reader
* [#260](https://bitbucket.org/openpyxl/openpyxl/issue/260) - unsized worksheets
* [#264](https://bitbucket.org/openpyxl/openpyxl/issue/264) - only numeric cells can be dates

# 1.8.2 (2014-01-17)[](#id625 "Link to this heading")

* [#247](https://bitbucket.org/openpyxl/openpyxl/issue/247) - iterable worksheets open too many files
* [#252](https://bitbucket.org/openpyxl/openpyxl/issue/252) - improved handling of lxml
* [#253](https://bitbucket.org/openpyxl/openpyxl/issue/253) - better handling of unique sheetnames

# 1.8.1 (2014-01-14)[](#id629 "Link to this heading")

* [#246](https://bitbucket.org/openpyxl/openpyxl/issue/246)

# 1.8.0 (2014-01-08)[](#id631 "Link to this heading")

## Compatibility[](#id632 "Link to this heading")

Support for Python 2.5 dropped.

## Major changes[](#id633 "Link to this heading")

* Support conditional formatting
* Support lxml as backend
* Support reading and writing comments
* pytest as testrunner now required
* Improvements in charts: new types, more reliable

## Minor changes[](#id634 "Link to this heading")

* load\_workbook now accepts data\_only to allow extracting values only from
  formulae. Default is false.
* Images can now be anchored to cells
* Docs updated
* Provisional benchmarking
* Added convenience methods for accessing worksheets and cells by key

# 1.7.0 (2013-10-31)[](#id635 "Link to this heading")

## Major changes[](#id636 "Link to this heading")

Drops support for Python < 2.5 and last version to support Python 2.5

## Compatibility[](#id637 "Link to this heading")

Tests run on Python 2.5, 2.6, 2.7, 3.2, 3.3

## Merged pull requests[](#merged-pull-requests "Link to this heading")

* 27 Include more metadata
* 41 Able to read files with chart sheets
* 45 Configurable Worksheet classes
* 3 Correct serialisation of Decimal
* 36 Preserve VBA macros when reading files
* 44 Handle empty oddheader and oddFooter tags
* 43 Fixed issue that the reader never set the active sheet
* 33 Reader set value and type explicitly and TYPE\_ERROR checking
* 22 added page breaks, fixed formula serialization
* 39 Fix Python 2.6 compatibility
* 47 Improvements in styling

## Known bugfixes[](#known-bugfixes "Link to this heading")

* [#109](https://bitbucket.org/openpyxl/openpyxl/issue/109)
* [#165](https://bitbucket.org/openpyxl/openpyxl/issue/165)
* [#209](https://bitbucket.org/openpyxl/openpyxl/issue/209)
* [#112](https://bitbucket.org/openpyxl/openpyxl/issue/112)
* [#166](https://bitbucket.org/openpyxl/openpyxl/issue/166)
* [#109](https://bitbucket.org/openpyxl/openpyxl/issue/109)
* [#223](https://bitbucket.org/openpyxl/openpyxl/issue/223)
* [#124](https://bitbucket.org/openpyxl/openpyxl/issue/124)
* [#157](https://bitbucket.org/openpyxl/openpyxl/issue/157)

## Miscellaneous[](#miscellaneous "Link to this heading")

Performance improvements in optimised writer

Docs updated

[![Logo](_static/logo.png)](index.html)

### [Table of Contents](index.html)

* [3.1.3 (2024-05-29)](#)
  + [Bugfixes](#bugfixes)
  + [Changes](#changes)
* [3.1.2 (2023-03-11)](#id18)
* [3.1.1 (2023-02-13)](#id21)
  + [Bugfixes](#id22)
* [3.1.0 (2023-01-31)](#id25)
  + [New Features](#new-features)
  + [Bugfixes](#id26)
  + [Pull Requests](#pull-requests)
  + [Deprecations](#deprecations)
  + [Removals](#removals)
* [3.0.10 (2022-05-19)](#id42)
  + [Bugfixes](#id43)
* [3.0.9 (2021-09-22)](#id48)
  + [Bugfixes](#id49)
* [3.0.8 (brown bag)](#brown-bag)
* [3.0.7 (2021-03-09)](#id57)
  + [Bugfixes](#id58)
  + [Pull Requests](#id63)
* [3.0.6 (2021-01-14)](#id64)
  + [Bugfixes](#id65)
  + [Pull Requests](#id75)
* [3.0.5 (2020-08-21)](#id76)
  + [Bugfixes](#id77)
* [3.0.4 (2020-06-24)](#id85)
  + [Bugfixes](#id86)
  + [Pull Requests](#id95)
* [3.0.3 (2020-01-20)](#id96)
  + [Bugfixes](#id97)
* [3.0.2 (2019-11-25)](#id101)
  + [Bug fixes](#bug-fixes)
  + [Pull Requests](#id107)
* [3.0.1 (2019-11-14)](#id108)
  + [Bugfixes](#id109)
  + [Pull Requests](#id111)
* [3.0.0 (2019-09-25)](#id112)
  + [Python 3.6+ only release](#python-3-6-only-release)
* [2.6.4 (2019-09-25)](#id113)
  + [Final release for Python 2.7 and 3.5](#final-release-for-python-2-7-and-3-5)
  + [Bugfixes](#id114)
* [2.6.3 (2019-08-19)](#id115)
  + [Bugfixes](#id116)
  + [Pull Requests](#id123)
* [2.6.2 (2019-03-29)](#id124)
  + [Bugfixes](#id125)
* [2.6.1 (2019-03-04)](#id132)
  + [Bugfixes](#id133)
* [2.6.0 (2019-02-06)](#id146)
  + [Bugfixes](#id147)
* [2.6.-b1 (2019-01-08)](#b1-2019-01-08)
  + [Bugfixes](#id150)
* [2.6-a1 (2018-11-21)](#a1-2018-11-21)
  + [Major changes](#major-changes)
  + [Minor changes](#minor-changes)
  + [Deprecations](#id155)
* [2.5.14 (2019-01-23)](#id156)
  + [Bugfixes](#id157)
  + [Pull Requests](#id161)
* [2.5.13 (brown bag)](#id162)
* [2.5.12 (2018-11-29)](#id163)
  + [Bugfixes](#id164)
  + [Pull Requests](#id169)
* [2.5.11 (2018-11-21)](#id170)
  + [Pull Requests](#id171)
* [2.5.10 (2018-11-13)](#id172)
  + [Bugfixes](#id173)
  + [Pull Requests](#id175)
* [2.5.9 (2018-10-19)](#id176)
  + [Bugfixes](#id177)
  + [Pull Requests](#id181)
* [2.5.8 (2018-09-25)](#id182)
* [2.5.7 (2018-09-13)](#id186)
* [2.5.6 (2018-08-30)](#id190)
* [2.5.5 (2018-08-04)](#id194)
  + [Bugfixes](#id195)
  + [Pull Requests](#id199)
* [2.5.4 (2018-06-07)](#id200)
  + [Bugfixes](#id201)
  + [Minor changes](#id204)
* [2.5.3 (2018-04-18)](#id205)
  + [Bugfixes](#id206)
* [2.5.2 (2018-04-06)](#id213)
  + [Bugfixes](#id214)
  + [Minor changes](#id221)
* [2.5.1 (2018-03-12)](#id222)
  + [Bugfixes](#id223)
* [2.5.0 (2018-01-24)](#id232)
  + [Minor changes](#id233)
* [2.5.0-b2 (2018-01-19)](#b2-2018-01-19)
  + [Bugfixes](#id234)
  + [Major Changes](#id241)
  + [Minor Changes](#id242)
* [2.5.0-b1 (2017-10-19)](#b1-2017-10-19)
  + [Bugfixes](#id243)
  + [Major Changes](#id255)
  + [Minor Changes](#id256)
  + [Deprecations](#id257)
* [2.5.0-a3 (2017-08-14)](#a3-2017-08-14)
  + [Bugfixes](#id258)
* [2.5.0-a2 (2017-06-25)](#a2-2017-06-25)
  + [Major Changes](#id261)
  + [Bugfixes](#id262)
* [2.5.0-a1 (2017-05-30)](#a1-2017-05-30)
  + [Compatibility](#compatibility)
  + [Major Changes](#id266)
  + [Deprecations](#id267)
  + [Bugfixes](#id268)
  + [Pull requests](#id271)
  + [Minor changes](#id273)
* [2.4.11 (2018-01-24)](#id274)
* [2.4.10 (2018-01-19)](#id275)
  + [Bugfixes](#id276)
  + [Pull requests](#id277)
* [2.4.9 (2017-10-19)](#id278)
  + [Bugfixes](#id279)
  + [Pull requests](#id289)
* [2.4.8 (2017-05-30)](#id295)
  + [Bugfixes](#id296)
  + [Minor changes](#id302)
* [2.4.7 (2017-04-24)](#id303)
  + [Bugfixes](#id304)
* [2.4.6 (2017-04-14)](#id306)
  + [Bugfixes](#id307)
* [2.4.5 (2017-03-07)](#id314)
  + [Bugfixes](#id315)
  + [Pull requests](#id319)
* [2.4.4 (2017-02-23)](#id322)
  + [Bugfixes](#id323)
  + [Minor Changes](#id331)
  + [Pull requests](#id332)
* [2.4.3 (unreleased)](#unreleased)
* [2.4.2 (2017-01-31)](#id334)
  + [Bug fixes](#id335)
  + [Minor Changes](#id346)
* [2.4.1 (2016-11-23)](#id347)
  + [Bug fixes](#id348)
  + [Minor changes](#id364)
  + [Deprecations](#id365)
  + [Bug fixes](#id366)
* [2.4.0 (2016-09-15)](#id367)
  + [Bug fixes](#id368)
  + [Major changes](#id374)
  + [Minor changes](#id375)
* [2.4.0-b1 (2016-06-08)](#b1-2016-06-08)
  + [Minor changes](#id376)
  + [Bug fixes](#id377)
  + [Features](#features)
* [2.4.0-a1 (2016-04-11)](#a1-2016-04-11)
  + [Minor changes](#id383)
  + [Deprecations](#id384)
  + [Bug fixes](#id385)
* [2.3.5 (2016-04-11)](#id397)
  + [Bug fixes](#id398)
* [2.3.4 (2016-03-16)](#id400)
  + [Bug fixes](#id401)
  + [Minor changes](#id405)
* [2.3.3 (2016-01-18)](#id406)
  + [Bug fixes](#id407)
  + [Minor changes](#id413)
* [2.3.2 (2015-12-07)](#id414)
  + [Bug fixes](#id415)
  + [Minor changes](#id420)
* [2.3.1 (2015-11-20)](#id422)
  + [Bug fixes](#id423)
  + [Minor changes](#id433)
* [2.3.0 (2015-10-20)](#id434)
  + [Major changes](#id435)
  + [Bug fixes](#id436)
  + [Minor changes](#id438)
* [2.3.0-b2 (2015-09-04)](#b2-2015-09-04)
  + [Bug fixes](#id439)
  + [Minor changes](#id449)
* [2.3.0-b1 (2015-06-29)](#b1-2015-06-29)
  + [Major changes](#id450)
  + [Minor changes](#id451)
  + [Bug fixes](#id452)
* [2.2.6 (unreleased)](#id461)
  + [Bug fixes](#id462)
* [2.2.5 (2015-06-29)](#id467)
  + [Bug fixes](#id468)
* [2.2.4 (2015-06-17)](#id472)
  + [Bug fixes](#id473)
* [2.2.3 (2015-05-26)](#id481)
  + [Bug fixes](#id482)
* [2.2.2 (2015-04-28)](#id488)
  + [Bug fixes](#id489)
* [2.2.1 (2015-03-31)](#id492)
  + [Minor changes](#id493)
  + [Bug fixes](#id494)
* [2.2.0 (2015-03-11)](#id504)
  + [Bug fixes](#id505)
* [2.2.0-b1 (2015-02-18)](#b1-2015-02-18)
  + [Major changes](#id507)
  + [Bug fixes](#id508)
  + [Minor changes](#id519)
* [2.1.5 (2015-02-18)](#id520)
  + [Bug fixes](#id521)
  + [Minor changes](#id526)
* [2.1.4 (2014-12-16)](#id527)
  + [Bug fixes](#id528)
  + [Minor changes](#id534)
* [2.1.3 (2014-12-09)](#id535)
  + [Minor changes](#id536)
  + [Bug fixes](#id537)
* [2.1.2 (2014-10-23)](#id540)
  + [Minor changes](#id541)
  + [Bug fixes](#id542)
* [2.1.1 (2014-10-08)](#id549)
  + [Minor changes](#id550)
  + [Bug fixes](#id551)
* [2.1.0 (2014-09-21)](#id558)
  + [Major changes](#id559)
  + [Minor changes](#id560)
  + [Bug fixes](#id561)
* [2.0.5 (2014-08-08)](#id570)
  + [Bug fixes](#id571)
* [2.0.4 (2014-06-25)](#id574)
  + [Minor changes](#id575)
  + [Bug fixes](#id576)
* [2.0.3 (2014-05-22)](#id578)
  + [Minor changes](#id579)
  + [Bug fixes](#id580)
* [2.0.2 (2014-05-13)](#id582)
* [2.0.1 (2014-05-13) brown bag](#id583)
* [2.0.0 (2014-05-13) brown bag](#id584)
  + [Major changes](#id585)
  + [Minor changes](#id586)
  + [Pull requests](#id587)
  + [Bug fixes](#id588)
* [1.8.6 (2014-05-05)](#id608)
  + [Minor changes](#id609)
  + [Bugfixes](#id610)
* [1.8.5 (2014-03-25)](#id612)
  + [Minor changes](#id613)
* [1.8.4 (2014-02-25)](#id614)
  + [Bugfixes](#id615)
* [1.8.3 (2014-02-09)](#id619)
  + [Major changes](#id620)
  + [Minor changes](#id621)
* [1.8.2 (2014-01-17)](#id625)
* [1.8.1 (2014-01-14)](#id629)
* [1.8.0 (2014-01-08)](#id631)
  + [Compatibility](#id632)
  + [Major changes](#id633)
  + [Minor changes](#id634)
* [1.7.0 (2013-10-31)](#id635)
  + [Major changes](#id636)
  + [Compatibility](#id637)
  + [Merged pull requests](#merged-pull-requests)
  + [Known bugfixes](#known-bugfixes)
  + [Miscellaneous](#miscellaneous)

#### Previous topic

[Parsing Formulas](formula.html "previous chapter")

### This Page

* [Show Source](_sources/changes.rst.txt)

### Quick search

### Navigation

* [index](genindex.html "General Index")
* [modules](py-modindex.html "Python Module Index") |
* [previous](formula.html "Parsing Formulas") |
* [openpyxl 3.1.3 documentation](index.html) »
* 3.1.3 (2024-05-29)

© Copyright 2010 - 2024, See AUTHORS.
Created using [Sphinx](https://www.sphinx-doc.org/) 7.3.7.