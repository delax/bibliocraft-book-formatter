bibliocraft-book-formatter
==========================

Write [BiblioCraft](http://www.bibliocraftmod.com/) compatible books from plain text.

Uses [Python 3.4+](http://python.org/) and NBTUtil from [NBTExplorer](https://github.com/jaquadro/NBTExplorer)

NBTUtil uses .NET/Mono, for more info read its own page.

## Running:

### Built version:
* Usage:
  * To run gui: use `formatter_gui.exe`
  * To run terminal: `bibliocraft_book_formatter.exe`
    * For terminal's built-in help: `bibliocraft_book_formatter.exe --help`

### Unbuilt version:
* Requires:
  * Python 3.4+
* Usage:
  * To run gui: `formatter_gui.py`
  * To run terminal: `bibliocraft_book_formatter.py`
    * For terminal's built-in help: `bibliocraft_book_formatter.py --help`

## Building
* Requires:
  * Python 3.4+
  * [cx_Freeze](http://cx-freeze.sourceforge.net/)
* Usage:
  * To build: `setup.py build`
