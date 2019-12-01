#! python3

"""
    Format a text file into either kind of BiblioCraft compatible book,
    one in Big Book Format and one in Vanilla.
"""

import argparse
import textwrap
import shutil
import subprocess
from pathlib import Path
import re
from math import ceil
from bisect import bisect_left

# Constants
bookAndQuillProperties = {
    'avg line width' : 19,
    'max page length' : 256,
    'max number of lines per page' : 13,
    'max number of pages' : 50,
    'info filename template' : '{author}, {title}',
    }
bigBookProperties = {
    'max line width' : 70,
    'max number of lines per page' : 44,
    'max number of pages' : 256,
    'info filename template' : '{author}, {title}',
    'dat filename template' : '{author}, {title}.dat',
    }

possibleSpecialSymbols = set(['@', '#', '$', '%', '^', '&', '*', '-', '_', '~', '¶', '|'])

reDatTemplateFilename = re.compile(r'dat template (?P<size>\d+)\.dat')

templateDir = Path('./big book templates')

bigBookTW = textwrap.TextWrapper(
    width=bigBookProperties['max line width'] - 1)
bookTW = textwrap.TextWrapper(
    width=bookAndQuillProperties['avg line width'] - 1)

class TooManyPagesError(Exception):
    """Simple Exception class to handle case of overflow of pages into one big book."""
    pass

def _get_special_symbols(usedText):
    """Find which special symbols are unused in the text."""
    return list(possibleSpecialSymbols - set(usedText))

def _get_template_sizes(path=templateDir):
    """Check file system for available dat template sizes"""
    templateSizeList = list()
    templatedir = Path(path)
    for filepath in templatedir.iterdir():
        m = reDatTemplateFilename.match(filepath.name)
        if m:
            templateSizeList.append(int(m.group('size')))
    return sorted(templateSizeList)

def _set_NBT_value(filename, tagpath, newvalue):
    """quick helper function to call NBTUtil.exe concisely"""
    path = Path(filename) / Path(*tagpath)
    return subprocess.check_output(
        ['NBTUtil/NBTUtil.exe', '--path=%s' % path, '--setvalue=%s' % newvalue],
        timeout=5,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        )

# TODO Minecraft raises error when .dat file is > 32KB, and a 46 page book was > 100KB.
# A full blank book is 74.7KB
def big_book_write(lines, author='author', title='title', allowMultipleBooks=False,
                   signed=True, output_dir=Path('./'), outputfunc=print):
    """Write a big book info and dat file using NBTUtil."""

    booksizes = _get_template_sizes()
    
    totalpages = ceil(len(lines) / bigBookProperties['max number of lines per page'])
    totalbooks = ceil(totalpages / bigBookProperties['max number of pages'])
    
    if totalpages > bigBookProperties['max number of pages'] and not allowMultipleBooks:
        raise TooManyPagesError()

    maxLinesPerBook = (bigBookProperties['max number of pages']
                       * bigBookProperties['max number of lines per page'])

    # grab info file template
    with templateDir.joinpath('info template').open('r') as f:
        infoTemplate = f.read()
    
    # for every book needed
    for booknum, startline in enumerate(range(0, len(lines), maxLinesPerBook)):
        outputfunc('\twriting book %s' % booknum)
        # calculate properties
        linesslice = slice(startline, startline + min(maxLinesPerBook, len(lines) - startline))

        bookinfo = {
            'author' : author,
            'title' : title if totalbooks == 1 else title + str(booknum),
            'numpages' : min(
               bigBookProperties['max number of pages'],
                totalpages - booknum * bigBookProperties['max number of pages'],
                ),
            }
        infoFilename = output_dir.joinpath(
            bigBookProperties['info filename template'].format(**bookinfo))
        datFilename = output_dir.joinpath(
            bigBookProperties['dat filename template'].format(**bookinfo))
        outputfunc('\tcreating info file "%s"' % infoFilename)
        with infoFilename.open('w') as info:
            info.write(infoTemplate.format(**bookinfo))

        outputfunc('\tcopying dat file "%s"' % datFilename)
        shutil.copy(
            str(templateDir.joinpath(
                'dat template %s.dat' %
                booksizes[ bisect_left(booksizes, bookinfo['numpages']) ]
                )),
            str(datFilename),
            )

        outputfunc('\twriting dat file "%s"' % datFilename)
        outputfunc(_set_NBT_value(datFilename, ['author'], bookinfo['author']))
        outputfunc(_set_NBT_value(datFilename, ['display', 'Name'], bookinfo['title']))
        if not signed:
            outputfunc(_set_NBT_value(datFilename, ['signed'], int(signed)))
        outputfunc(_set_NBT_value(datFilename, ['pagesTotal'], bookinfo['numpages']))
        # call NBTUtil.exe to write everything in .dat file
        for i, text in enumerate(lines[linesslice]):
            pagenum, linenum = divmod(i, bigBookProperties['max number of lines per page'])
            if text:
                outputfunc(_set_NBT_value(datFilename, ['pages', 'page%s' % pagenum, '%s' % linenum], text))
        

def big_book_wrap(book):
    """Word wrap given book's text to fit a BiblioCraft Big Book's lines."""
    paragraphs = book.splitlines()
    lines = list()
    for paragraph in paragraphs:
        newlines = bigBookTW.wrap(paragraph)
        if len(newlines) == 0:
            newlines.append('')
        lines.extend(newlines)
    return lines

def book_wrap(book):
    """Word wrap given book's text to fit a vanilla Book's lines."""
    paragraphs = book.splitlines()
    lines = list()
    for paragraph in paragraphs:
        newlines = bookTW.wrap(paragraph)
        if len(newlines) == 0:
            newlines.append('')
        lines.extend(newlines)
    return lines

def book_write(lines, author='author', title='title', output_dir=Path('./')):
    """Output a valid vanilla book, given properly sized lines of text."""
    book = '\n'.join([title, author, 'public'])
    for firstline in range(0,len(lines),bookAndQuillProperties['max number of lines per page']):
        pagenum = firstline // bookAndQuillProperties['max number of lines per page']
        book += '\n'.join(
            ['\n#pgx%s' % pagenum]
            + lines[
                firstline :
                firstline + min(bookAndQuillProperties['max number of lines per page'], len(lines) - firstline)
                ]
            )
    with output_dir.joinpath('{}, {}'.format(author, title)).open('w') as b:
        b.write(book)
    
def create_arg_parser():
    parser = argparse.ArgumentParser(
        description='Format a text file to either of the BiblioCraft ' \
        + 'compatible book files, Vanilla or Big book. Can also output a text only' \
        + ' version to preview or for manual copy-paste into Minecraft.')
    parser.add_argument('file', help='text file to write books from')
    parser.add_argument('-t', '--title', required=True, help='set the title of the book')
    parser.add_argument('-a', '--author', required=True, help='set the author of the book')
    parser.add_argument('-x', '--textonly', action='store_true',
                            help='output only as properly wrapped, read-able text files')
    parser.add_argument('-o', '--output-dir', default='./',  type=Path,
                        help='Specify output directory, will ask to create it if it does not exist.')
    
    formatgroup = parser.add_mutually_exclusive_group(required=True)
    formatgroup.add_argument('-v', '--vanilla', action="store_true",
                       help="write a vanilla type book")
    formatgroup.add_argument('-b', '--bigbook', action="store_true",
                       help="write a big type book")

    bigbookgroup = parser.add_argument_group('Big Book Only flags',
                                      'These flags really only make a difference on big books.')
    bigbookgroup.add_argument('--unsigned', action='store_true',
                              help='set book to unsigned (aka editable)')

    return parser

if __name__ == '__main__':

    parser=create_arg_parser()

    args = parser.parse_args()

    with open(args.file, mode='r') as f:
        book = f.read()

    if not args.output_dir.is_dir():
        print('Output dir "%s" does not exist, should I create it?' % args.output_dir)
        answer = input('(y/n)> ')
        if answer.lower() in ['y', 'yes', 'yep', 'ye']:
            args.output_dir.mkdir()
            print('"%s" created.' % args.output_dir)
        else:
            raise FileNotFoundError(args.output_dir)
    
    if args.vanilla:
        lines = book_wrap(book)
        if args.textonly:
            with args.output_dir.joinpath('vanilla {}, {}.txt'.format(args.author, args.title)).open('w') as b:
                b.write('\n'.join(lines))
            print('Vanilla book formatted file written (copy-paste into Minecraft)')
        else:
            book_write(lines, title=args.title, author=args.author, output_dir=args.output_dir)
            print('Vanilla book file written (move file to \'minecraft\\config\\books\')')
    elif args.bigbook:
        lines = big_book_wrap(book)
        if args.textonly:
            with args.output_dir.joinpath('big book {}, {}.txt'.format(args.author, args.title)).open('w') as b:
                b.write('\n'.join(lines))
            print('Big book formatted file written (copy-paste into Minecraft)')
        else:
            big_book_write(lines, title=args.title, author=args.author,
                           signed=not args.unsigned, output_dir=args.output_dir)
            print('Big book file written (move file to \'minecraft\\config\\books\')')
