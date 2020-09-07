from tkinter import scrolledtext as scr
import tkinter as tk


root = tk.Tk()
root.geometry('500x600+50+50')
root.resizable(False, False)
widget1 = scr.ScrolledText(root)
widget2 = tk.Text(root)
# widget1.pack()

# print(dir(tk.Text.insert))


for i in (widget1,widget2):
    i.pack()
    widget1.insert('end', '世界\n')
    widget1.insert('end', '世界')
    print('------------->')
    widget2.insert('end', '世界\n')
    widget2.insert('end', '世界')
    for j in range(50):
        i.insert('end', '我爱你\n')
    # print(i.info)

root.mainloop()