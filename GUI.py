# VIP, if any of the libraries used here not installed for you
# then open cmd and type "pip install <library name>"
import re
import math
import sympy as sym
from tkinter import *
from utils import *
from tkinter.filedialog import askopenfile

DEFAULT_BACKGROUND = "#424949"
DEFAULT_FONT_COLOR = "#9F1723"
FIELD_BACKGROUND = "#85C1E9"
result = 0
methodChoice = 0
xl = 0
xu = 0
es = 0.00001
no_iter = 50
eqn = ""
is_file = False

def methodCallback(*args):
    global methodChoice
    for idx,val in methodDic.items():
        if val == menu.get():
            methodChoice = idx
    print(methodChoice)
    if methodChoice==2 or methodChoice==3:
        xlLabel.config(text="X0")
        # hide the grid
        xuLabel.grid_remove()
        xuEntry.grid_remove()
    else:
        xlLabel.config(text="XL")
        # show it again
        xuLabel.grid()
        xuEntry.grid()

def open_file():
    global methodChoice, result, xl, xu, es, iter_max, eqn, is_file
    file = askopenfile(mode='r', filetypes=[('Text Files', '*.txt')])
    if file:
        is_file = True
        methodChoice = int(file.readline())
        eqn = file.readline()
        if methodChoice in(0, 1, 4): 
            (xl, xu, es, iter_max) = re.split(',', file.readline())
            xu = float(xu)
        elif methodChoice in (2, 3):
            (xl, es, iter_max) = re.split(',', file.readline())
        xl = float(xl)
        es = float(es)
        iter_max = int(iter_max)
        file.close()

def displayResult():
    global result, xl, xu, es, iter_max, eqn
    if(not is_file):
        try:
            xl = float(xlEntry.get())
        except:
            print("ERORR")
        try:
            xu = float(xuEntry.get())
        except:
            print("ERORR")
        try:
            es = float(esEntry.get())
        except:
            es = 0.00001
        try:
            iter_max = int(iter_maxEntry.get())
        except:
            iter_max = 50
        try:
            eqn = eqnEntry.get()
        except:
            print("ERORR")
   
    singleStepArray = []
    if methodChoice == 0:
        (result, ea, no_iter, singleStepArray) = bisection(eqn, xl, xu, es, iter_max)
    elif methodChoice == 1: 
        (result, ea, no_iter, singleStepArray) = falsePosition(eqn, xl, xu, es, iter_max)
    elif methodChoice == 2:  
        (result, ea, no_iter, singleStepArray) = fixedPoint(eqn, xl, es, iter_max)
    elif methodChoice == 3: 
        (result, ea, no_iter, singleStepArray) = newtonRaphson(eqn, xl, es, iter_max)
    elif methodChoice == 4:
        (result, ea, no_iter, singleStepArray) = secant(eqn, xl, xu, es, iter_max)
    else:
        result = ""   
    answerLabel.config(text=result)
    result = str(result) +'\n'
    for tup in singleStepArray:
        result = result +'\n'
        for elem in tup:
            result = result + str(elem)[:7] +'\t'
    answerLabel.config(text=result)
def set_text(ch):
    eqnEntry.insert(END,ch)
    return
def del_text():
    eqnEntry.delete(len(eqnEntry.get())-1, END)
    return
window = Tk()
window.geometry("1000x500")
# make window responsive
window.columnconfigure(0, weight=1, minsize=75)
window.rowconfigure(0, weight=1, minsize=50)
# create a frame
frame = Frame(width=1000, height=500, background=DEFAULT_BACKGROUND)
frame.pack(anchor=W, fill='both', expand=True)
# title label
titleLabel = Label(master=frame,
                        text="Root Finder",
                        foreground=DEFAULT_FONT_COLOR,
                        background=DEFAULT_BACKGROUND,
                        font=("Times",26,"bold italic"))
titleLabel.grid(row=0, column=11, sticky='n')
# method label
methodLabel = Label(master=frame,
                        text="Method",
                        foreground=DEFAULT_FONT_COLOR,
                        background=DEFAULT_BACKGROUND,
                        font=("Helvetica",26,"bold"))
methodLabel.grid(row=4, column=0, sticky='w')
# method drop down menu
menu = StringVar(frame)
menu.set("Choose A Method")
menu.trace_add('write',methodCallback)
methodDic={0:"Bisection", 1:"False-position", 2:"Fixed point", 3:"Newton-Raphson", 4:"Secant"}
methodMenu= OptionMenu(frame, menu,*methodDic.values())
methodMenu.config(background=FIELD_BACKGROUND)
methodMenu.grid(row=4, column=2, sticky='w')
# equation label
eqnLabel = Label(master=frame,
                        text="Equation",
                        foreground=DEFAULT_FONT_COLOR,
                        background=DEFAULT_BACKGROUND,
                        font=("Helvetica",26,"bold"))
eqnLabel.grid(row=6, column=0, sticky='w')
# equation entry
eqnEntry = Entry(master=frame, background=FIELD_BACKGROUND)
eqnEntry.grid(row=6, column=2, sticky='w')
# create buttons
buttonOne = Button(master=frame, text="1", background=FIELD_BACKGROUND, width=3, command=lambda:set_text("1"))
buttonOne.grid(row=8, column=0, sticky='w')
buttonTwo = Button(master=frame, text="2", background=FIELD_BACKGROUND, width=3, command=lambda:set_text("2"))
buttonTwo.grid(row=8, column=0)
buttonThree = Button(master=frame, text="3", background=FIELD_BACKGROUND, width=3, command=lambda:set_text("3"))
buttonThree.grid(row=8, column=0, sticky='e')
buttonFour = Button(master=frame, text="4", background=FIELD_BACKGROUND, width=3, command=lambda:set_text("4"))
buttonFour.grid(row=9, column=0, sticky='w')
buttonFive = Button(master=frame, text="5", background=FIELD_BACKGROUND, width=3, command=lambda:set_text("5"))
buttonFive.grid(row=9, column=0)
buttonSix = Button(master=frame, text="6", background=FIELD_BACKGROUND, width=3, command=lambda:set_text("6"))
buttonSix.grid(row=9, column=0, sticky='e')
buttonSeven = Button(master=frame, text="7", background=FIELD_BACKGROUND, width=3, command=lambda:set_text("7"))
buttonSeven.grid(row=10, column=0, sticky='w')
buttonEight = Button(master=frame, text="8", background=FIELD_BACKGROUND, width=3, command=lambda:set_text("8"))
buttonEight.grid(row=10, column=0)
buttonNine = Button(master=frame, text="9", background=FIELD_BACKGROUND, width=3, command=lambda:set_text("9"))
buttonNine.grid(row=10, column=0, sticky='e')
buttonZero = Button(master=frame, text="0", background=FIELD_BACKGROUND, width=3, command=lambda:set_text("0"))
buttonZero.grid(row=11, column=0, sticky='w')
buttonPlus = Button(master=frame, text="+", background=FIELD_BACKGROUND, width=3, command=lambda:set_text("+"))
buttonPlus.grid(row=11, column=0, sticky='e')
buttonMinus = Button(master=frame, text="-", background=FIELD_BACKGROUND, width=3, command=lambda:set_text("-"))
buttonMinus.grid(row=11, column=0)
buttonMul = Button(master=frame, text="*", background=FIELD_BACKGROUND, width=3, command=lambda:set_text("*"))
buttonMul.grid(row=12, column=0, sticky='w')
buttonDiv = Button(master=frame, text="/", background=FIELD_BACKGROUND, width=3, command=lambda:set_text("/"))
buttonDiv.grid(row=12, column=0)
buttonPower = Button(master=frame, text="^", background=FIELD_BACKGROUND, width=3, command=lambda:set_text("^"))
buttonPower.grid(row=12, column=0, sticky='e')
buttonDel = Button(master=frame, text="Del", background=FIELD_BACKGROUND, width=3, command=del_text)
buttonDel.grid(row=13, column=0, sticky='w')
buttonLeftBracket = Button(master=frame, text="(", background=FIELD_BACKGROUND, width=3, command=lambda:set_text("("))
buttonLeftBracket.grid(row=13, column=0)
buttonRightBracket = Button(master=frame, text=")", background=FIELD_BACKGROUND, width=3, command=lambda:set_text(")"))
buttonRightBracket.grid(row=13, column=0, sticky='e')

buttonSin = Button(master=frame, text="sin", background=FIELD_BACKGROUND, width=3, command=lambda:set_text("sin"))
buttonSin.grid(row=8, column=2)
buttonCos = Button(master=frame, text="cos", background=FIELD_BACKGROUND, width=3, command=lambda:set_text("cos"))
buttonCos.grid(row=9, column=2)
buttonTan = Button(master=frame, text="tan", background=FIELD_BACKGROUND, width=3, command=lambda:set_text("tan"))
buttonTan.grid(row=10, column=2)
buttonExp = Button(master=frame, text="e", background=FIELD_BACKGROUND, width=3, command=lambda:set_text("e"))
buttonExp.grid(row=11, column=2)
buttonPoint = Button(master=frame, text=".", background=FIELD_BACKGROUND, width=3, command=lambda:set_text("."))
buttonPoint .grid(row=12, column=2)
buttonVar = Button(master=frame, text="X", background=FIELD_BACKGROUND, width=3, command=lambda:set_text("x"))
buttonVar.grid(row=13, column=2)

# get parameters
parametersLabel = Label(master=frame,
                        text="Parameters",
                        foreground=DEFAULT_FONT_COLOR,
                        background=DEFAULT_BACKGROUND,
                        font=("Helvetica",26,"bold"))
parametersLabel.grid(row=4, column=12, sticky='w')

# get x lower
xlLabel = Label(master=frame,
                text="XL",
                foreground=DEFAULT_FONT_COLOR,
                background=DEFAULT_BACKGROUND,
                font=("Helvetica",16,"bold"))
xlLabel.grid(row=6, column=12, sticky='w')
xlEntry = Entry(master=frame, background=FIELD_BACKGROUND)
xlEntry.grid(row=6, column=12, sticky='e')
# get x upper
xuLabel = Label(master=frame,
                text="XU",
                foreground=DEFAULT_FONT_COLOR,
                background=DEFAULT_BACKGROUND,
                font=("Helvetica",16,"bold"))
xuLabel.grid(row=7, column=12, sticky='w')
xuEntry = Entry(master=frame, background=FIELD_BACKGROUND)
xuEntry.grid(row=7, column=12, sticky='e')
# get es
esLabel = Label(master=frame,
                text="es",
                foreground=DEFAULT_FONT_COLOR,
                background=DEFAULT_BACKGROUND,
                font=("Helvetica",16,"bold"))
esLabel.grid(row=8, column=12, sticky='w')
esEntry = Entry(master=frame, background=FIELD_BACKGROUND)
esEntry.grid(row=8, column=12, sticky='e')
# get iter_max
iter_maxLabel = Label(master=frame,
                text="Iters",
                foreground=DEFAULT_FONT_COLOR,
                background=DEFAULT_BACKGROUND,
                font=("Helvetica",16,"bold"))
iter_maxLabel.grid(row=9, column=12, sticky='w')
iter_maxEntry = Entry(master=frame, background=FIELD_BACKGROUND)
iter_maxEntry.grid(row=9, column=12, sticky='e')
# get file
fileLabel = Label(master=frame,
                text="Choose A File",
                foreground=DEFAULT_FONT_COLOR,
                background=DEFAULT_BACKGROUND,
                font=("Helvetica",16,"bold"))
fileLabel.grid(row=8, column=10, sticky='w')
fileButton = Button(master=frame, text="Browse", background=FIELD_BACKGROUND ,command=open_file)
fileButton.grid(row=9, column=10)

# find roots button
FRButton = Button(master=frame, text="Find Roots", background=FIELD_BACKGROUND ,command=displayResult)
FRButton.grid(row=11, column=12)
# answer label
answerTextLabel = Label(master=frame,
                        text="ANSWER:",
                        foreground=DEFAULT_FONT_COLOR,
                        background=DEFAULT_BACKGROUND,
                        font=("Times",26,"bold italic"))
answerTextLabel.grid(row=14, column=11, sticky='n')
answerLabel = Label(master=frame,
                        text="",
                        foreground="cyan",
                        background=DEFAULT_BACKGROUND,
                        font=("Helvetica",12,"bold"))
answerLabel.grid(row=14, column=12, sticky='w')
window.mainloop()
