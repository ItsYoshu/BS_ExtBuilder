import os
import tkinter
from tkinter import filedialog, messagebox
from tkinter.messagebox import showinfo
from zipfile import ZipFile
import sys
import pathlib


def select_file():
    filetypes = (
        ('vassal module files', '*.vmod'),
        ('All files', '*.*')
    )

    filename = filedialog.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    showinfo(title='Selected File', message=filename)
    return filename


def askDirectoryGUI(debug=None, message=None):
    if debug is None: debug = False
    if message is None: message = 'Please select a directory'

    root = tkinter.Tk()
    root.withdraw()  # use to hide tkinter window

    currdir = os.getcwd()
    tempdir = filedialog.askdirectory(parent=root, initialdir=currdir, title=message)
    if len(tempdir) > 0:
        if debug: print("You chose %s" % tempdir)

        if os.path.isdir(tempdir):
            return tempdir
        else:
            messagebox.showerror("Vassal Constructor Error", "Please select a folder containing all your images.")
            return askDirectoryGUI()
    else:
        return None


def file_savezip(zipfile):
    f = filedialog.asksaveasfile(mode='w', defaultextension=".vmdx")
    if f is None:
        return
    f.write(zipfile)
    f.close()


def zip_directory(name=None, path=None, savepath=None):
    if name is None:
        name = "Custom Battle Spirits Ext.zip"
    if not name.endswith(".zip"):
        name += ".zip"

    if path is None:
        raise Exception("Error: No source directory to zip specified.")

    if savepath is None:
        raise Exception("Error: No destination directory specified.")

    length = len(path.__str__())
    save_dest = os.path.join(savepath, name)

    with ZipFile(save_dest, 'w') as zipObj:
        for root, dirs, files in os.walk(path):
            folder = root[length:]  # path without "parent"
            for file in files:
                zipObj.write(os.path.join(root, file), os.path.join(folder, file))
    return name


def get_datadir() -> pathlib.Path:

    """
    Returns a parent directory path
    where persistent application data can be stored.

    # linux: ~/.local/share
    # macOS: ~/Library/Application Support
    # windows: C:/Users/<USER>/AppData/Roaming
    """

    home = pathlib.Path.home()

    if sys.platform == "win32":
        return home / "AppData/Roaming"
    elif sys.platform == "linux":
        return home / ".local/share"
    elif sys.platform == "darwin":
        return home / "Library/Application Support"
