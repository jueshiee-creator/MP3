"""
player v1.1 2020/3/11
Author: jue
player v1.1 最基础的播放器版本"""
from tkinter import *
import pygame
import os, time
import threading
from random import choice
from mutagen.mp3 import MP3
# from pymediainfo import MediaInfo
from tkinter.filedialog import askdirectory, askopenfilename # , askopenfilenames



judge1 = 1
def main():
    pygame.mixer.init()

    root = Tk()
    root.geometry('1000x600+183+84')
    root.title('音乐播放器 v1.1')
    root.resizable(False,False)
    path='D:\Document\pythonCode\Programs\Pwormppp\网易云音乐下载\music_files'
    # paths = StringVar()
    pathn = StringVar()
    judge2 = 0

    
    def find():
        # 本地音乐文件地址
        nonlocal judge2
        global folder_path
        global music_list

        if not judge2:
            folder_path = r"D:\Document\pythonCode\Programs\Pwormppp\网易云音乐下载\music_files"
            judge2 = 1
        else:
            folder_path_fu = callback1()
            if not folder_path_fu:
                folder_path = folder_path_fu
            else:
                pass
        folder_list = os.listdir(folder_path)  # 遍历文件夹里面每个文件
        music_list = []
        # count = 0
        o1.delete(0,END) # 清除之前listbox列表
        for i in folder_list:  # 将文件夹里的文件按顺序传提给变量i  此处区别os.walk()
            # os.path.splitext(i)[1]
            if os.path.splitext(i)[1] in '.mp3':  # 提取i文件特定后缀'.***'
                music_list.append(i)
                o1.insert("end",i.split('.mp3')[0])
        print(music_list)

    def getmu(self):   # 据我推测，o1.bind("<Double-Button-1>",getmu)要加参数args
        # dir = 'D:/文件/python代码/Programs/Pwormppp/网易云音乐下载/music_files'
        music_name=o1.get(o1.curselection())+'.mp3'
        file=os.path.join(folder_path,music_name)
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        print('正在播放 {}'.format(music_name))

    def callback1():
        path_ = askdirectory()
        return path_

    def callback2():  # 搜索本地文件
        path_ = askopenfilename(filetypes=[("mp3 file", "*.mp3"),("all","*.*")]) #   askdirectory()
        return path_

    def alone_play():  # 播放音乐
        f = callback2()  # 选择制定文件
        print(type(f))
        pygame.mixer.music.load(f)
        pygame.mixer.music.play()
        # global path
        # path=f
        pathn.set(f)

    def play():
        pass

    def music_pause():
        global judge1
        if judge1 == 1:
            pygame.mixer.music.pause()
            judge1 = 2
        else:
            pygame.mixer.music.unpause()
            judge1 = 1

    def re_play():
        pygame.mixer.music.rewind()  # 重新播放

    def stop():
        pygame.mixer.music.stop()

    def close_window():
        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except:
            pass
        root.destroy()


    root.protocol('WM_DELETE_WINDOW', close_window) # 设置窗口关闭的运行事件
    
    #歌单
    o1=Listbox(root,width=25, heigh=25, font=("楷书", 15), bd=4)
                        #selectmode="brose", 
                        #selectmode=tkinter.BROWSE
                        #设置下拉列表框listbox数据项的选中模式为:
                        #当左击鼠标并移动时,可以选中列表项
                        #selectmode=tkinter.SINGLE
                        #设置通过左击鼠标的方式选中数据项
    o1.grid(row=2, column=0)
    find()
    # Button(root,text='添加歌曲',command=musicadd,bg="sky blue").place(x=740,y=330)
    o1.bind("<Double-Button-1>",getmu)  # 双击

    m1 = Button(root, text='播放歌单', command=find,width=10,heigh=2, font=("黑体", 12), bg="sky blue")
    m1.grid(row=0, rowspan=2, column=0)

    # 选择文件
    Button(root, text="选择文件/播放", command=alone_play, width=10, bg="sky blue").grid(row=0, column=1)
    Entry(root, text=pathn, width=25, state='readonly', bd=2).grid(row=0, column=2, columnspan=2)

    pause = Button(root, text='暂停/继续', command=music_pause, bg="sky blue")
    pause.grid(row=1, column=1)
    contiplay = Button(root, text='重新播放', command=re_play, bg="sky blue")
    contiplay.grid(row=1, column=2)
    contiplay = Button(root, text='停止播放', command=stop, bg="sky blue")
    contiplay.grid(row=1, column=3)

    kong = Label(root, text='此处为空', width=55,heigh=4, font=("Helvetica", 12))
    kong.grid(row=0, rowspan=2, column=4)

    songs = Listbox(root, bg="white", width=104, heigh=29, bd=5)
    songs.grid(row=2,column=1,columnspan=4, sticky=W)
    # sb = Scrollbar(root)
    # sb.grid(row=2,column=4)
    #关联滚动条
    # songwords.config(yscrollcommand=sb.set)
    # sb.configure(command=songwords.yview)
    root.mainloop()
    

if __name__ == '__main__':
    main()