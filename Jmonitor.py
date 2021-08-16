#!/usr/bin/env python3
import tkinter as tk
import tkinter.ttk
from tkinter import N, W, E, S
from tkinter import StringVar
import os
import time
import threading



class Message(tk.Toplevel):
    def __init__(self, message):
        tk.Toplevel.__init__(self)
        tk.Label(self, text=message).grid(row=0, column=0)
        tk.Button(self, command=self.destroy, text="OK").grid(row=1, column=0)
        self.lift()  # Puts Window on top
        self.grab_set()  # Prevents other Tkinter windows from being used


def tracing(value, last_time):
    new_time = last_time
    while new_time == last_time:
        time.sleep(1)
        new_time = os.path.getmtime(value)
    Message(value + ":" + time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(new_time)))
    tracing_date.set(time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(new_time)))

    tracing_set.remove(value)
    update_tracing_state()




def trace(*args):
    try:
        value = tracing_name_input.get()
        if os.path.isfile(value):
            tracing_file_name.set("Now tracing:" + value)
            last_time = os.path.getmtime(value)
            tracing_date.set(time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(last_time)))
            if value in tracing_set:
                return
            tracing_set.add(value)
            update_tracing_state()
            # l tracing_thread
            tracing_thread = threading.Thread(target=tracing, args=(value, last_time))
            tracing_thread.daemon = True
            tracing_thread.start()
        else:
            tracing_date.set("0000/00/00 00:00:00")
            tracing_file_name.set("illegal name or FileNotExist")
    except ValueError:
        pass


def update_tracing_state():
    tracing_count.set("Tracing files count %d" % len(tracing_set))
    tracing_files.set("\n".join(list(tracing_set)))

if __name__ == "__main__":
    root = tk.Tk()
    tracing_set = set()
    default_val = ""
    mainframe = tk.ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(row=0, column=0, sticky=tk.W)
    tracing_name_input = StringVar()
    tracing_name_input.set(default_val)
    tracing_file_name = StringVar()
    tracing_date = StringVar()
    tracing_count = StringVar()
    tracing_files = StringVar()
    tracing_name_entry = tk.ttk.Entry(mainframe, width=88, textvariable=tracing_name_input)
    tracing_name_entry.grid(row=1, column=1, sticky=(W, S))
    buttonframe = tk.ttk.Frame(mainframe)
    buttonframe.grid(column=1, row=2)
    button = tk.ttk.Button(buttonframe, text="To trace change", command=trace).grid(column=1, row=1)
    tk.ttk.Label(mainframe, textvariable=tracing_file_name).grid(column=1, row=3, sticky=(W, S, N, E))
    tk.ttk.Label(mainframe, textvariable=tracing_date).grid(column=1, row=4, sticky=(W, S, N, E))
    tk.ttk.Label(mainframe, textvariable=tracing_count).grid(column=1, row=5, sticky=(W, S, N, E))
    tk.ttk.Label(mainframe, textvariable=tracing_files).grid(column=1, row=6, sticky=(W, S, N, E))
    tracing_name_entry.focus()
    for child in mainframe.winfo_children():
        child.grid_configure(padx=15, pady=15)
    root.bind("<Return>", trace)
    root.mainloop()
