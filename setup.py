#! python3

from cx_Freeze import setup, Executable

include_files = [
    './NBTUtil/',
    './big book templates/',
    ]

build_exe_options = {
    'include_files' : include_files,
    }

setup(
    name = 'bibliocraft_book_formatter',
    version = '0.1',
    description = 'Write BiblioCraft compatible books from plain text.',
    options = {'build_exe' : build_exe_options},
    executables = [Executable('bibliocraft_book_formatter.py')],
    )
