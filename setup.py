#! python3

from cx_Freeze import setup, Executable

include_files = [
    './NBTUtil/',
    './big book templates/',
    './README.md',
    ]

build_exe_options = {
    'include_files' : include_files,
    }

executables = [
    Executable('bibliocraft_book_formatter.py'),
    Executable('formatter_gui.py'),
    ]

setup(
    name = 'bibliocraft_book_formatter',
    version = '1.1',
    description = 'Write BiblioCraft compatible books from plain text.',
    options = {'build_exe' : build_exe_options},
    executables = executables,
    )
