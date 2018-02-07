#!/usr/bin/python

import argparse
import Tkinter as tk
import tkFont
import numpy as np
import operator

color = "#%02x%02x%02x" % (255, 51, 102)

operations = {
    'multiply' : 'X',
    'divide' : '/',
    'add' : '+', 
    'subtract' : '-'
    }

operators = {
    'multiply': operator.mul,
    'divide': operator.mul,
    'add': operator.add,
    'subtract': operator.add
    }


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
                Q = '{} {} {} = '.format(y, op, x)
                A = '{} {} {} = {}'.format(y, op, x, result)
                problems.append((Q, A))
            else:
                if j >= i:
                    Q = '{} {} {} = '.format(result, op, x)
                    A = '{} {} {} = {}'.format(result, op, x, y)
                    problems.append((Q, A))
    return problems

class FlashCard(tk.Frame):

    def __init__(self, parent, text):
        tk.Frame.__init__(self, master=parent, bg='white')

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
        

def main(args):
    root = tk.Tk()
    root.title('')

    ## Full screen and set focus
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    root.focus_set()  # <-- move focus to this widget
    ## background color
    root.configure(background='white')

    problems = get_problems(args)
    if args.shuffle:
        np.random.shuffle(problems)
    for i in range(len(problems)):
        Q = FlashCard(root, problems[i][0])
        A = FlashCard(root, problems[i][1])

    root.mainloop()



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Avery's Flash Cards")
    parser.add_argument('--fact_type', type=str,
                        help='multiply, divide, subtract, add',
                        default='add'
                        )
    parser.add_argument('--focus', type=int,
                        help='Restrict all facts to this integer',
                        default=0
                        )
    parser.add_argument('--max_int', type=int,
                        help='Maximum integer for facts',
                        default=12
                        )
    parser.add_argument('--shuffle', type=int,
                        help='1 or 0 (shuffle or not)',
                        default=1
                        )
    
    args = parser.parse_args()
    
    main(args)


