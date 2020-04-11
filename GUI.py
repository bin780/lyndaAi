import speech_recognition as sr
import Lynda as m
import Train as t



try:
    from Tkinter import *
except ImportError:
    from tkinter import *

try:
    import ttk

    py3 = False
except ImportError:
    import tkinter.ttk as ttk

    py3 = True

def callback(recognizer, audio):                                          # this is called from the background thread
    try:
        #global model
        audio=recognizer.recognize_google(audio).lower()
        print(audio)# received audio data, now need to recognize it
        l.assistant(audio)
        gui.Message1.configure(text="say something.....")
    except sr.UnknownValueError:
        print("Oops! Didn't catch that")
    except sr.RequestError as r:
        print(r)
        l.lyndaResponse("please make sure you have a working internet connection for me to work")

def fun(self):
    self.Button1.config(state=DISABLED)
    try:
        global gui,l
        gui=self
        l=m.Lynda(gui)
        r = sr.Recognizer()                                         # callback function when the button is pushed
        print("listening now")
        r.listen_in_background(sr.Microphone(), callback)
    except:
        self.Message1.configure(text="plaease make sure there is internet connection")


import sys




def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = Tk()
    top = lynda(root)                                                                 # function to launch gui

    root.mainloop()


w = None





def destroy_lynda():
    global w
    w.destroy()
    w = None


class lynda:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'                                                       # tkinter gui class
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#d9d9d9'  # X11 color: 'gray85'

        top.geometry("422x760+650+150")
        top.title("lynda")
        top.configure(background="#2bd8d2")

        self.Frame1 = Frame(top)
        self.Frame1.place(relx=0.047, rely=0.053, relheight=0.586
                          , relwidth=0.912)
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(background="#d9d9d9")
        self.Frame1.configure(width=385)

        self.Message1 = Message(self.Frame1)
        self.Message1.place(relx=0.026, rely=0.112, relheight=0.517
                            , relwidth=0.925)
        self.Message1.configure(background="#d9d9d9")
        self.Message1.configure(foreground="#000000")
        self.Message1.configure(highlightbackground="#d9d9d9")
        self.Message1.configure(highlightcolor="black")
        self.Message1.configure(text='''Lynda''')
        self.Message1.configure(width=356)

        self.Button1 = Button(top)
        self.Button1.place(relx=0.474, rely=0.75, height=33, width=41)
        self.Button1.configure(activebackground="#d9d9d9")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''start''')
        self.Button1.configure(command=lambda :fun(self))


if __name__ == '__main__':                              #launching the gui
    vp_start_gui()


