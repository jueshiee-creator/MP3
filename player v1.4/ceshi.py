from tkinter import *

window = Tk()

value = StringVar()
def s_print(text):		#注意，Scale的回调函数需要给定形参，当触发时会将Scale的值传给函数
    print(value.get())
    print(text)			#两者同样的效果
Scale(window,label='sss',
      from_=0,to=100,
      resolution=1,show=0,
      variable=value,command=s_print
      ).pack()

window.mainloop()
# ————————————————
# 版权声明：本文为CSDN博主「geeknuo」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https://blog.csdn.net/u014663232/article/details/88890801