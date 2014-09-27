#! python3

"""A basic GUI using tkinter for bibliocraft_book_formatter.py"""

import bibliocraft_book_formatter as bbf
from pathlib import Path

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

class FormatterApp(ttk.Frame):
    """Main app window"""

    helptexts = {
        'input file' : 'Text file to write books from. (required)',
        'output dir' : 'Book(s) will be written into this directory. (default: "./")',
        'title' : 'Title of written book. (required)',
        'author' : 'Author of written book. (required)',
        'text-only' : 'Wraps input text to fit specified book type, then outputs it as a plain text file.',
        'vanilla' : 'Write a Vanilla type book.',
        'big book' : 'Write a BiblioCraft Big Book type book (takes longer).',
        'signed' : 'Signed books are not editable in MC. This setting only effects Big Books. (default: "on")',
        }
    
    def __init__(self, master=None, **kwds):
        super().__init__(master, **kwds)

        framekwds = {'padding' : '3 3 12 12'}
        
        # Input file selection
        self.inputfilepathvar = StringVar()
        self.inputfilepathvar.set('')

        inputfileframe = ttk.LabelFrame(self, text='Input File:', **framekwds)
        self._bind_display_help(inputfileframe, 'input file')
        ttk.Entry(inputfileframe, textvariable=self.inputfilepathvar, width=20).grid(column=0, row=0, sticky=(W,E))
        ttk.Button(inputfileframe, text='Browse',
                   command=lambda *args : self.inputfilepathvar.set(filedialog.askopenfilename())
                   ).grid(column=1, row=0, sticky=(E,W))

        inputfileframe.columnconfigure(0, weight=1)
        inputfileframe.columnconfigure(1, weight=1)
        inputfileframe.rowconfigure(0, weight=1)

        # Book info
        self.bookinfovars = {
            'title' : StringVar(),
            'author' : StringVar(),
            }

        for info in self.bookinfovars.values():
            info.set('')

        bookinfoframe = ttk.LabelFrame(self, text='Book Info:', **framekwds)

        w = ttk.Label(bookinfoframe, text='Title:')
        w.grid(column=0, row=0, sticky=E)
        self._bind_display_help(w, 'title')

        w = ttk.Entry(bookinfoframe, textvariable=self.bookinfovars['title'], width=32)
        w.grid(column=1, row=0, sticky=W)
        self._bind_display_help(w, 'title')

        w = ttk.Label(bookinfoframe, text='Author:')
        w.grid(column=2, row=0, sticky=E)
        self._bind_display_help(w, 'author')

        w = ttk.Entry(bookinfoframe, textvariable=self.bookinfovars['author'], width=32)
        w.grid(column=3, row=0, sticky=W)
        self._bind_display_help(w, 'author')

        bookinfoframe.columnconfigure(0, weight=1)
        bookinfoframe.columnconfigure(1, weight=1)
        bookinfoframe.columnconfigure(2, weight=1)
        bookinfoframe.columnconfigure(3, weight=1)
        bookinfoframe.rowconfigure(0, weight=1)

        # Book type selection
        self.booktypevar = StringVar()
        self.booktypevar.set('')

        booktypeframe = ttk.LabelFrame(self, text='Book Type:', **framekwds)

        w = ttk.Radiobutton(booktypeframe, text='Vanilla', value='vanilla', variable=self.booktypevar)
        w.grid(column=0,row=0)
        self._bind_display_help(w, 'vanilla')
        
        w = ttk.Radiobutton(booktypeframe, text='Big Book', value='big book', variable=self.booktypevar)
        w.grid(column=0, row=1)
        self._bind_display_help(w, 'big book')

        booktypeframe.columnconfigure(0, weight=1)
        booktypeframe.rowconfigure(0, weight=1)
        booktypeframe.rowconfigure(1, weight=1)
        
        # Option Selection
        self.optionvars = {
            'text-only' : StringVar(),
            'signed' : StringVar(),
            }
        for option in self.optionvars.values():
            option.set('0')

        self.optionvars['signed'].set('1')

        optionframe = ttk.LabelFrame(self, text='Options:', **framekwds)

        w = ttk.Checkbutton(optionframe, text='Text-Only', variable=self.optionvars['text-only'])
        w.grid(column=0, row=0)
        self._bind_display_help(w, 'text-only')
        
        w = ttk.Checkbutton(optionframe, text='Signed', variable=self.optionvars['signed'])
        w.grid(column=0, row=1)
        self._bind_display_help(w, 'signed')

        optionframe.columnconfigure(0, weight=1)
        optionframe.rowconfigure(0, weight=1)
        optionframe.rowconfigure(1, weight=1)

        # Output dir selection
        self.outputdirvar = StringVar()
        self.outputdirvar.set('./')

        outputdirframe = ttk.LabelFrame(self, text='Output Dir:', **framekwds)
        self._bind_display_help(outputdirframe, 'output dir')

        ttk.Entry(outputdirframe, textvariable=self.outputdirvar, width=20).grid(column=0, row=0, sticky=(W,E))
        ttk.Button(outputdirframe, text='Browse',
                   command=lambda *args : self.outputdirvar.set(filedialog.askdirectory())
                   ).grid(column=1, row=0, sticky=(W,E))

        outputdirframe.columnconfigure(0, weight=1)
        outputdirframe.columnconfigure(1, weight=1)
        outputdirframe.rowconfigure(0, weight=1)

        doitbutton = ttk.Button(self, text='Do it', command=self.write_some_books)

        self.helptextvar = StringVar()
        self.helptextvar.set('')

        statusframe = ttk.Frame(self, relief='sunken', **framekwds)

        ttk.Label(statusframe, textvariable=self.helptextvar).grid(column=0, row=0, sticky=E)

        statusframe.columnconfigure(0, weight=1)
        statusframe.rowconfigure(0, weight=1)
        statusframe.rowconfigure(1, weight=1)

        # Grid 'em
        kwds = {
            'sticky' : NSEW,
            'padx':3,
            'pady':3,
            }
        inputfileframe.grid(column=0, row=0, columnspan=2, **kwds)
        bookinfoframe.grid(column=0, row=1, columnspan=2, **kwds)
        booktypeframe.grid(column=0, row=2, **kwds)
        optionframe.grid(column=1, row=2, **kwds)
        outputdirframe.grid(column=0, row=3, columnspan=2, **kwds)
        doitbutton.grid(column=0, row=4, columnspan=2, sticky=N, pady=kwds['pady'])
        statusframe.grid(column=0, row=5, columnspan=2, sticky=(S,W,E))

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)

    def write_some_books(self):
        """Do the actual work here"""
        
        inputfilepath = Path(self.inputfilepathvar.get())
        outputdirpath = Path(self.outputdirvar.get())
        if not inputfilepath.is_file():
            messagebox.showerror(title='Invalid input', message='Input file "%s" not found.' % inputfilepath)
            return
        if not all(map(lambda x: x.get(), self.bookinfovars.values())):
            messagebox.showerror(title='Invalid input', message='Book title and author must be given.')
            return
        if self.booktypevar.get() not in ['vanilla', 'big book']:
            messagebox.showerror(title='Invalid input', message='Book type must be choosen.')
            return
        if not outputdirpath.is_dir():
            answer = messagebox.askyesno(title='Create new directory?',
                                         message='Output dir "%s" does not exist. Should I create it?' % outputdirpath)
            if answer == 'yes':
                outputdirpath.mkdir()
            else:
                return

        bookinfo = {k : v.get() for k,v in self.bookinfovars.items()}

        with inputfilepath.open('r') as f:
            book = f.read()

        if self.booktypevar.get() == 'big book':
            lines = bbf.big_book_wrap(book)
        else:
            lines = bbf.book_wrap(book)

        if int(self.optionvars['text-only'].get()):
            with outputdirpath.joinpath('{} {author}, {title}.txt'.format(self.booktypevar.get(), **bookinfo)).open('w') as b:
                b.write('\n'.join(lines))
        elif self.booktypevar.get() == 'big book':
            bbf.big_book_write(lines, output_dir=outputdirpath,
                               signed = bool(int(self.optionvars['signed'].get())), **bookinfo)
        else:
            bbf.book_write(lines, output_dir=outputdirpath, **bookinfo)

        self.helptextvar.set('{} {}file written ({})'.format(
            self.booktypevar.get(),
            'formatted ' if int(self.optionvars['text-only'].get()) else '',
            'copy-paste into Minecraft ' if int(self.optionvars['text-only'].get()) else 'move file to \'minecraft\\config\\books\'',
            ))
        

    def _bind_display_help(self, widget, itemname):
        """Displays help text in status bar for item, if it is available"""
        helptext = self.helptexts.get(itemname, '')
        if helptext != '':
            def show_help(e):
                self.helptextvar.set(helptext)
            def clear_help(e):
                self.helptextvar.set('')
            widget.bind('<Enter>', show_help)
            widget.bind('<Leave>', clear_help)

if __name__ == '__main__':
    root = Tk()
    root.title('Bibliocraft Book Formatter')
    
    # Main background frame
    mainframe = FormatterApp(root)
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    
    root.mainloop()
