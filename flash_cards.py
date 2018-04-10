#!/usr/bin/python

import argparse
import Tkinter as tk
import tkFont
import numpy as np
import operator

color = "#%02x%02x%02x" % (255, 51, 102)

operations = {
    'multiply' : u'\u00D7',
    'divide' : u'\u00F7',
    'add' : '+', 
    'subtract' : u'\u2212'
    }

operators = {
    'multiply': operator.mul,
    'divide': operator.mul,
    'add': operator.add,
    'subtract': operator.add
    }


class Args:
    def __init__(self):
        pass

    def add_argument(self, name, value):
        setattr(self, name, value)

def get_problems(args):
    problems = []
    if args.focus:
        a, b = args.focus - 1, args.focus
    else:
        a, b = 0, args.max_int
    for i in range(a, b):
        for j in range(args.max_int):
            x, y = i + 1, j + 1
            op = operations[args.fact_type]
            result = operators[args.fact_type](x, y)
            if args.fact_type == 'add' or args.fact_type == 'multiply':
                Q = u'{} {} {} = '.format(y, op, x)
                A = u'{} {} {} = {}'.format(y, op, x, result)
                problems.append((Q, A))
            else:
                if j >= i:
                    Q = u'{} {} {} = '.format(result, op, x)
                    A = u'{} {} {} = {}'.format(result, op, x, y)
                    problems.append((Q, A))
    return problems

class FlashCard(tk.Frame):

    def __init__(self, parent, text):
        tk.Frame.__init__(self, master=parent)

        font = tkFont.Font(family='Arial', size=120)
        self.button = tk.Button(self, text=text, font=font,
                                fg=color,
                                bg='white',
                                bd=0,
                                activeforeground=color,
                                activebackground='white',
                                highlightthickness=0)

        self.button.bind('<Return>',self.send)
        self.button.pack()
        self.place(anchor='c', relx=.5, rely=.5)
        self.button.focus()
        parent.wait_window(self.button)

    def send(self,event=None):
        self.destroy()

class Options:
    def __init__(self, parent):
        #tk.Frame.__init__(self, master=parent)
    
        self.frame = tk.Frame(parent)

        self.shuffle = 1
        self.fact_type = 'add'
        self.focus = 0
        self.max_int = tk.IntVar()
        self.max_int.set(12)

        pady = 30
        padx = 30

        shuffle_frame = tk.Frame(self.frame)
        shuffle_label = tk.Label(shuffle_frame, 
                                 text='Shuffle Facts?')
        self.shuffle_b1 = tk.Button(shuffle_frame, 
                               text='Yes',
                               state=tk.DISABLED,
                               disabledforeground='blue',
                               command=lambda: self.set_shuffle(0))
        self.shuffle_b2 = tk.Button(shuffle_frame, 
                               text='No',
                               disabledforeground='blue',
                               command=lambda: self.set_shuffle(1))

        shuffle_label.grid(row=0, column=0, columnspan=2)
        self.shuffle_b1.grid(row=1, column=0)
        self.shuffle_b2.grid(row=1, column=1)
        shuffle_frame.grid(row=0, column=1, padx=padx)

        type_frame = tk.Frame(self.frame)
        type_label = tk.Label(type_frame, 
                                 text='Fact Type')
        self.type_buttons = [0 for i in range(4)]
        self.type_buttons[0] = tk.Button(type_frame, 
                               text='+',
                               state=tk.DISABLED,
                               disabledforeground='blue',
                               command=lambda: self.set_type(0))
        self.type_buttons[1] = tk.Button(type_frame, 
                               text=u'\u2212',
                               disabledforeground='blue',
                               command=lambda: self.set_type(1))
        self.type_buttons[2] = tk.Button(type_frame, 
                               text=u'\u00D7',
                               disabledforeground='blue',
                               command=lambda: self.set_type(2))
        self.type_buttons[3] = tk.Button(type_frame, 
                               text=u'\u00F7',
                               disabledforeground='blue',
                               command=lambda: self.set_type(3))

        type_label.grid(row=0, column=0, columnspan=2)
        self.type_buttons[0].grid(row=1, column=0)
        self.type_buttons[1].grid(row=1, column=1)
        self.type_buttons[2].grid(row=2, column=0)
        self.type_buttons[3].grid(row=2, column=1)
        type_frame.grid(row=0, column=0)


        max_frame = tk.Frame(self.frame)
        max_text = tk.Label(max_frame, 
                            text='Max Number')
        max_entry = tk.Entry(max_frame, 
                                justify='left',
                                width=3,
                                textvariable=self.max_int)
        max_text.grid(row=0, column=0)
        max_entry.grid(row=1, column=0)
        max_frame.grid(row=1, column=0, pady=pady)

        focus_frame = tk.Frame(self.frame)
        focus_text = tk.Label(focus_frame, 
                            text='Focus')
        self.focus_entry = tk.Entry(focus_frame, 
                                justify='left',
                                width=3)
        focus_text.grid(row=0, column=0)
        self.focus_entry.grid(row=1, column=0)
        focus_frame.grid(row=1, column=1, padx=padx, pady=pady)

        self.advance = tk.Button(self.frame, text='Continue', command=self.start)
        self.advance.grid(row=2, column=0, columnspan=2)

        self.frame.place(anchor='c', relx=0.5, rely=0.5)

    def set_shuffle(self, val):
        if val == 0:
            self.shuffle_b1['state'] = tk.DISABLED
            self.shuffle_b2['state'] = tk.NORMAL
            self.shuffle = 1
        else:
            self.shuffle_b1['state'] = tk.NORMAL
            self.shuffle_b2['state'] = tk.DISABLED
            self.shuffle = 0
    
    def set_type(self, val):
        convert = ['add', 
                   'subtract',
                   'multiply',
                   'divide']
        self.fact_type = convert[val]
        for i in range(4):
            if i != val:
                self.type_buttons[i]['state'] = tk.NORMAL
            else:
                self.type_buttons[i]['state'] = tk.DISABLED
    def start(self):
        try:
            max_int = int(self.max_int.get())
            focus = self.focus_entry.get()
            if focus != '':
                self.focus = int(focus)
            if self.focus <= max_int:
                self.max_int = max_int
                self.frame.destroy()
        except (AttributeError, ValueError):
            pass
        

def main():
    root = tk.Tk()
    root.title('')

    root.option_add('*Background', 'white')
    root.option_add('*Foreground', 'black')
    root.option_add('*Font', 'Arial 40')


    ## Full screen and set focus
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    root.focus_set()  # <-- move focus to this widget
    ## background color
    root.configure(background='white')

    while True:
        options = Options(root)
        root.wait_window(options.frame)

        problems = get_problems(options)
        if options.shuffle:
            np.random.shuffle(problems)
        for i in range(len(problems)):
            Q = FlashCard(root, problems[i][0])
            A = FlashCard(root, problems[i][1])

    root.mainloop()



if __name__ == '__main__':
    

    main()


