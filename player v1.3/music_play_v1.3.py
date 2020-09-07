"""
player v1.3 2020/3/14
在player v1.2版本上修正音乐播放卡顿的问题, 但进度条固定不动"""
from tkinter import *
import pygame
import os, time
import threading
from random import choice
from mutagen.mp3 import MP3
# from pymediainfo import MediaInfo
from tkinter.filedialog import askdirectory, askopenfilename # , askopenfilenames


pygame.mixer.init()

root = Tk()
root.geometry('1000x650+183+50')
root.title('音乐播放器 v1.3')
root.resizable(False,False)
path='D:/文件/python代码/Programs/Pwormppp/网易云音乐下载/music_files'
pathn = StringVar()
music_name = ''
index = 0
judge_name = 0
switch_num = 0
judge2 = 0
# time_add = 0
# time_jd = 0
time_ = 0
music_long = 200


def find():
    """导入文件夹音乐"""
    # 本地音乐文件地址
    global judge2
    global folder_path
    global music_list
    global judge_name

    if not judge2:  # 第一次打开(开启tk会自动打开一次，即默认)
        folder_path = r"D:\Document\pythonCode\Programs\Pwormppp\网易云音乐下载\music_files"
        judge2 = 1
    else:
        folder_path_fu = callback1()
        if folder_path_fu:
            folder_path = folder_path_fu
            pause_resume.set('播放')
            judge_name = -1
        else:
            pass
    folder_list = os.listdir(folder_path)  # 遍历文件夹里面每个文件
    music_list = []
    # count = 0
    o1.delete(0,END) # 清除之前listbox列表
    for i in folder_list:  # 将文件夹里的文件按顺序传提给变量i  此处区别os.walk()
        # os.path.splitext(i)[1]
        if os.path.splitext(i)[1] == '.mp3':  # 提取i文件特定后缀'.***'
            music_list.append(i)
            o1.insert("end",i.split('.mp3')[0])
    print(music_list)

def callback1():  # 搜索并选择文件夹
    path_ = askdirectory()
    return path_

def callback2():  # 搜索本地文件
    path_ = askopenfilename(filetypes=[("mp3 file", "*.mp3"),("all","*.*")]) #   askdirectory()
    return path_

def alone_play():  # 播放音乐
    """播放选择的单个文件"""
    f = callback2()  # 选择制定文件
    try:
        pygame.mixer.music.load(f)
        pygame.mixer.music.play()
    except:
        pass
    pathn.set(f)

def order_play():
    """顺序播放"""
    global index
    nextMusic = music_list[index]
    if not pygame.mixer.music.get_busy():
        # 按顺序播放一首歌曲
        jdt.set(value=0)
        nextMusic = music_list[index]
        print(nextMusic)
        print(index)
        global judge_name
        judge_name = index
        pygame.mixer.music.load(folder_path+'\\'+nextMusic)
        # 播放一次
        pygame.mixer.music.play(1)
        if len(music_list)-1 == index:
            index = 0
        else:
            index = index + 1
        musicName.set('playing...' +nextMusic)
    else:
        time.sleep(0.1)
        global time_from
        global current_long
        time_from = jdt.get()
        current_long = pygame.mixer.music.get_pos()/1000
        time_jd = float(current_long+time_)
        musicTime.set('已播放 {:0>2d}:{:0>2d}'.format(int(time_jd//60),int(time_jd%60)))

def select_play():
    """随机播放"""
    if not pygame.mixer.music.get_busy():
        # 随机播放一首歌曲
        global index
        nextMusic = music_list[index]
        print(nextMusic)
        print(index)
        global judge_name
        judge_name = index
        pygame.mixer.music.load(folder_path+'\\'+nextMusic)
        # 播放一次
        pygame.mixer.music.play(1)
        index = choice(list(range(len(music_list))))
        musicName.set('playing...' + nextMusic)
    else:
        time.sleep(0.1)
        global time_from
        global current_long
        time_from = jdt.get()
        current_long = pygame.mixer.music.get_pos()/1000
        time_jd = float(current_long+time_)
        musicTime.set('已播放 {:0>2d}:{:0>2d}'.format(int(time_jd//60),int(time_jd%60)))

def switch_j():
    global switch_num
    if switch_judge.get() == '顺序':
        switch_num = 1
        switch_judge.set('随机')
    elif switch_judge.get() == '随机':
        switch_num = 0
        switch_judge.set('顺序')

def play():
    # 初始化混音器设备
    global folder_path
    global switch_num
    
    if len(music_list):
        pygame.mixer.init()
        try:
            pygame.mixer.music.stop()
        except:
            pass
        while playing:
            if switch_num:
                select_play()
            else:
                order_play()
            
def click_play():
    """点击播放按钮"""
    global index
    global judge_name
    music_name=o1.get(o1.curselection())+'.mp3'
    index = music_list.index(music_name)
    if pause_resume.get() == '播放' and index != judge_name:
        pause_resume.set(value='暂停')

        global playing
        playing = True

        a_thread = threading.Thread(target=play, daemon=True)
        a_thread.start()

    elif pause_resume.get() == '暂停':
        pause_resume.set(value='播放')
        pygame.mixer.music.pause()

    elif pause_resume.get() == '播放':
        pause_resume.set(value='暂停')
        pygame.mixer.music.unpause()

def click_two_play(self):   # listbox内的鼠标左键单两次点击事件(不带参)
    """双击listbox内歌曲名"""
    global index
    music_name=o1.get(o1.curselection())+'.mp3'
    index = music_list.index(music_name)
    global playing
    playing = True

    a_thread = threading.Thread(target=play, daemon=True)
    a_thread.start()

def click_one_play(self):  # listbox内的鼠标左键单次点击事件
    """根据listbox内歌曲名判断播放暂停"""
    global judge_name
    music_name = o1.get(o1.curselection())+'.mp3'
    music_name_j = music_list[judge_name]
    # print(music_name_j, music_name)
    if music_name != music_name_j :  # and pause_resume.get() == '暂停'
        pause_resume.set(value='播放')
    elif music_name == music_name_j : # and pause_resume.get() == '播放'
        pause_resume.set(value='暂停')
    else:
        pass

def control_volume(value=0.5):
    """滑块控制声音"""
    pygame.mixer.music.set_volume(float(value))

def volume_increase_click():
    """增大音量"""
    value = pygame.mixer.music.get_volume()
    if value <= 1:
        value += 0.1
    pygame.mixer.music.set_volume(float(value))
    s.set(float(value))  # 控制滑块及音量

def volume_decrease_click():
    """降低音量"""
    value = pygame.mixer.music.get_volume()
    if value >= 0:
        value -= 0.1
    pygame.mixer.music.set_volume(float(value))
    s.set(float(value))   # 控制滑块及音量

def progress_bar(value=0):
    """进度条"""
    global folder_path
    global judge_name
    global time_
    global time_from
    global current_long
    
    music_name = music_list[judge_name]
    pat = folder_path+'\\'+music_name
    audio=MP3(pat)
    music_long=audio.info.length
    time_to = jdt.get()

    time_jd = float(time_to/100)*music_long
    time_ = time_jd
    if time_to < time_from:
        time_ = time_jd-current_long
    
    try:
        pygame.mixer.music.set_pos(float(time_jd))  # 设置播放的位置gl
    except:
        pass

def next_one_music():
    """下一首"""
    global playing
    playing = False
    pygame.mixer.music.stop()
    playing = True

    a_thread = threading.Thread(target=play, daemon=True)
    a_thread.start()

def previous_one_music():
    """上一首"""
    global playing
    playing = False
    pygame.mixer.music.stop()
    global index
    if index == 0:
        index = len(music_list)-2
    elif index == 1:
        index = len(music_list)-1
    else:
        index -= 2
    
    playing = True

    a_thread = threading.Thread(target=play, daemon=True)
    a_thread.start()

def re_play():
    """重新播放"""
    pygame.mixer.music.rewind()

def stop():
    """暂停音乐"""
    global playing
    playing = False
    try:
        pygame.mixer.music.stop()
    except:
        pass
    
def closeWindow():
    """关闭窗口"""
    global playing
    playing = False
    time.sleep(0.3)
    try:
        pygame.mixer.music.stop()
        pygame.mixer.quit()
    except:
        pass

    root.destroy() # 退出root


# 关闭窗口
root.protocol('WM_DELETE_WINDOW', closeWindow)

#歌单
o1=Listbox(root,width=25, heigh=25, font=("楷书", 15), bd=4, selectmode=BROWSE) # 
o1.grid(row=4, column=0, columnspan=2)
find()
# selectmode=tkinter.MULTIPLE 不用ctrl/shift就能多选
o1.bind("<Double-Button-1>",click_two_play)  # 双击
o1.bind("<ButtonRelease-1>", click_one_play) # 单击释放时的动作

m1 = Button(root, text='播放歌单', command=find,width=10,heigh=2, font=("黑体", 12), bg="sky blue")
m1.grid(row=0, rowspan=4, column=0)

# 选择文件
Button(root, text="选择文件/播放", command=alone_play, width=10, bg="sky blue").grid(row=0, column=2, columnspan=3)
Entry(root, text=pathn, width=25, state='readonly', bd=2).grid(row=0, column=5, columnspan=2) # 只能写入
# 转换播放模式
switch_judge = StringVar(root, value='顺序')
switch_play = Button(root, textvariable=switch_judge,
    width=5, bg="sky blue", command=switch_j)
switch_play.grid(row=0, rowspan=4, column=1)
# 音量调节
s = Scale(root, label='音量', from_=0, to=1, orient=HORIZONTAL,  # VERTICAL         
    length=240, tickinterval=2, resolution=0.1, command=control_volume) # 
s.grid(row=3, column=7, rowspan=1)        # , showvalue=0   
s.set(0.5)   
volume_increase = Button(root, text='+', bg="sky blue", width=5, command=volume_increase_click)
volume_increase.grid(row=1, rowspan=2, column=3, columnspan=1)
volume_decrease = Button(root, text='-', bg="sky blue", width=5, command=volume_decrease_click)
volume_decrease.grid(row=3, rowspan=1, column=3, columnspan=1, pady=(10,30)) # sticky
# 进度条
# time_var = StringVar(value=0)
jdt = Scale(root, from_=0, to=100, orient="horizontal", length=240,
    sliderrelief='flat', sliderlength=10, activebackground='black',
     repeatinterval=100, command=progress_bar,resolution=1, label="进度")# variable=time_var,
jdt.grid(row=2, column=7)
# 上下首
next_one = Button(root, text='>', bg="sky blue", command=next_one_music)  # 下一首
next_one.grid(row=1, rowspan=3, column=4, columnspan=1)
previous_one = Button(root, text='<', bg="sky blue", command=previous_one_music)  # 上一首
previous_one.grid(row=1, rowspan=3, column=2, columnspan=1)
# 点击播放
pause_resume = StringVar(root, value='播放')
pause = Button(root, textvariable=pause_resume,command=click_play, bg="sky blue")  # lambda:click_play(music_name)
pause.grid(row=1, column=3, columnspan=1, rowspan=3)
# pause['state']='disable'
# 重新播放
contiplay = Button(root, text='重新播放', command=re_play, bg="sky blue")
contiplay.grid(row=1, rowspan=3, column=5, columnspan=1)
contiplay = Button(root, text='停止播放', command=stop, bg="sky blue")
contiplay.grid(row=1, rowspan=3, column=6, columnspan=1)
# 播放显示
musicName = StringVar(value='暂无播放')
kong = Label(root, textvariable=musicName, width=55,heigh=1, font=("Helvetica", 12))
kong.grid(row=0, rowspan=1, column=7, columnspan=1)
musicTime = StringVar(value='')
music_time = Label(root, textvariable=musicTime, width=55,heigh=1, font=("Helvetica", 12))
music_time.grid(row=1, rowspan=1, column=7, columnspan=1)

songs = Listbox(root, bg="white", width=110, heigh=29, bd=5)
songs.grid(row=4, rowspan=1, column=2, columnspan=6)

# 开启循环
root.mainloop()