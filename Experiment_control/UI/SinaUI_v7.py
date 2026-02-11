#####################################
#UI for recording human trial responses
#####################################

import tkinter as tk
import tkinter.font as font
import csv
import os
import datetime
import time

same_diff = []
participantID = []
ChangeAllow = False

class ChoicePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        titleFont = font.Font(size=25)
        buttonFont = font.Font(size=30)

        label = tk.Label(self, text = "Same or Different?")
        label["font"] = titleFont

        label.pack()

        self.ticker = 1
        self.label2 = tk.Label(self, text="Simulation #1")
        self.label2["font"] = titleFont

        self.label2.pack()

        button = tk.Button(self, text = "Same (s)",
                           command = lambda:[controller.show_frame("MainView"), self.sameAppend(same_diff), self.ChangeName()])
        button["font"] = buttonFont
        self.bind('s', lambda event: [controller.show_frame("MainView"), self.sameAppend(same_diff), self.ChangeName()])
        button.place(x=25, y=200)
        
        button2 = tk.Button(self, text="Different (d)",
                           command=lambda: [controller.show_frame("MainView"), self.differentAppend(same_diff), self.ChangeName()])
        button2["font"] = buttonFont
        self.bind('d', lambda event: [controller.show_frame("MainView"), self.differentAppend(same_diff), self.ChangeName()])
        button2.place(x=250, y=200)
        
        button3 = tk.Button(self, text="Slightly Same (f)",
                           command=lambda: [controller.show_frame("MainView"), self.slightlySameAppend(same_diff), self.ChangeName()])
        button3["font"] = buttonFont
        self.bind('f', lambda event: [controller.show_frame("MainView"), self.slightlySameAppend(same_diff), self.ChangeName()])
        button3.place(x=85, y=300)

    def differentAppend(self, list):
        global ChangeAllow
        same_diff.append(["different", 1.0, self.ticker])
        ChangeAllow = True

    def sameAppend(self, list):
        global ChangeAllow
        same_diff.append(["same", 0.0, self.ticker])
        ChangeAllow = True
        
    def slightlySameAppend(self, list):
        global ChangeAllow
        same_diff.append(["slightly same", 0.5, self.ticker])
        ChangeAllow = True
        
    def ChangeName(self):
        self.ticker += 1
        self.label2["text"] = "Simulation #" + str(self.ticker)


class ParticipantPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        titleFont = font.Font(size=25)
        buttonFont = font.Font(size=30)

        title = tk.Message(self, text="Please enter Participant ID Number", justify="center", width=400)
        title["font"] = titleFont
        B = tk.Button(self, text="Enter", command=lambda: [controller.show_frame("MainView"), partIDGet(self)])
        B["font"] = buttonFont
        E = tk.Entry(self, width = "15")
        E["font"] = buttonFont

        E.place(x=100, y=150)
        B.place(x=190, y=250)
        title.pack()
        
        def partIDGet(self):
            participantID.append(E.get())


class MainView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.ticker = 0

        titleFont = font.Font(size=25)
        buttonFont = font.Font(size=30)



        title = tk.Message(self, text="Electrotactile Response Trials Program", justify = "center", width = 400)
        title["font"] = titleFont
        B = tk.Button(self, text="Ready? (space)", command = lambda: [controller.show_frame("ChoicePage"), MistakeAppear()])
        self.bind("<space>", lambda event: [controller.show_frame("ChoicePage"), MistakeAppear()] )
        B["font"] = buttonFont
        
        MistakeButton = tk.Button(self, text="Mistake?", command = lambda: [MistakeFixOnce(), MistakeGone()])
        
            

        title.pack()
        B.place(x=100, y=200)
        MistakeButton.place(x=100, y = 1000)
        
        def MistakeGone():
            MistakeButton.place(x=100, y = 1000)
            
        def MistakeAppear():
            MistakeButton.place(x=100, y = 400)
        
        def MistakeFixOnce():
            global ChangeAllow
            if ChangeAllow == True:
                if same_diff[-1][1] == 0.0 or same_diff[-1][1] == 0.5:
                    same_diff[-1][0] = "different"
                    same_diff[-1][1] = 1.0
                    
                elif same_diff[-1][1] == 1.0:
                    same_diff[-1][0] = "same"
                    same_diff[-1][1] = 0.0
                    
            ChangeAllow = False
            
class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (MainView, ParticipantPage, ChoicePage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("ParticipantPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        frame.focus_set()



if __name__ == "__main__":

    app = App()
    app.title("Electrotactile Response Trials Program")
    app.geometry("500x500")
    app.resizable(width=False, height=False)

    app.mainloop()

    os.chdir(os.path.dirname(os.path.abspath("SinaUI.py")))

    file = open('HumanTrialsForSina.csv', 'a+', newline = '')
    timestamp = str(datetime.datetime.now())
    timestamp2 = time.strftime('%d-%m-%Y %H:%M:%S')
    headers = [["S/D (words)", "S/D (Binary)", "Simulation #"]]
    with file:
        write = csv.writer(file)
        write.writerows([["Participant #:", participantID[0]]])
        write.writerows([[timestamp2]])
        write.writerows(headers)
        write.writerows(same_diff)

    file.close()
