import tkinter as tk
import tkinter.ttk as ttk

win=tk.Tk()
win.title("CommunicationTool")
win.rowconfigure(1, weight=1)
win.columnconfigure(0, weight=1)
#setting
setFrame = tk.LabelFrame(win,text="Setting")
setFrame.columnconfigure(2, weight=1)
comLable = tk.Label(setFrame,text="COM Port: ").grid(row=0,column=0)
comSpiner = tk.Spinbox(setFrame,text="COM1").grid(row=0,column=1,sticky=tk.EW)
refrashButton = ttk.Button(setFrame,text="Refresh").grid(row=0,column=2,sticky=tk.W)
inputLable = tk.Label(setFrame,text="Command: ").grid(row=1,column=0)
inputEntry = tk.Entry(setFrame).grid(row=1,column=1,sticky=tk.EW,columnspan=2)
sendButton = ttk.Button(setFrame,text="Send").grid(row=1,column=3)
setFrame.grid(row=0,sticky=tk.EW)
#output
outputFrame = tk.LabelFrame(win,text="Output")
outputFrame.rowconfigure(0,weight=1)
outputFrame.columnconfigure(0,weight=1)
area = tk.Text(outputFrame).grid(row=0,sticky=tk.NSEW)
outputFrame.grid(row=1,sticky=tk.NSEW)

win.mainloop()