from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory
import numpy as np


# exponential decay function
def decay(x, offset, factor, alpha):
    return factor * np.exp(-alpha * x) + offset


# open file from a window dialog
def open_file(file_type, prompt):
    root = Tk()
    if file_type == 'cts':
        text = 'Counts data file'
    elif file_type == 'kin':
        text = 'Kinetics data file'
    elif file_type == 'csv':
        text = 'CSV file'
    elif file_type == 'dat':
        text = 'Data file'
    else:
        raise ValueError
    name = askopenfilename(filetypes=((text, '*.' + file_type), ("All Files", "*.*")), title=prompt)
    root.withdraw()
    return name


# open directory from a window dialog
def open_dir(prompt):
    root = Tk()
    name = askdirectory(title=prompt)
    root.withdraw()
    return name


# decorating bar to separate different sections when program is run
def decorating_bar(symbol, *args):
    try:
        text = args[0]
        length = len(text)
        assert length <= 70
        n = (70 - len(text)) // 2
        m = 70 - len(text) - n
        print(n * symbol + text + m * symbol)
    except IndexError:
        print(70 * symbol)
    except AssertionError:
        print(args[0])
