"""
————2020/3/17
添加了两组背景,并支持歌曲删除操作(点亮后右击歌名)
————2020/3/14
在player v1.2版本上修正音乐播放卡顿的问题, 但进度条固定不动---------------
已修正众多进度条拖动bug，以及在播放键上的展现效果的完善，基本上算是完成了自己的一个小小
要求，plus版仍需努力，仅满足最基本的需求与展示效果.
音乐播放器 player v1.4 
Author : jue
"""

from tkinter import *
import pygame
import os, time
import threading
from random import choice
from mutagen.mp3 import MP3
# from pymediainfo import MediaInfo
import tkinter.messagebox as msg
from tkinter.filedialog import askdirectory, askopenfilename # , askopenfilenames


root = Tk()
root.geometry('1000x650+183+10')
root.title('音乐播放器 v1.4')
root.resizable(False,False)
path=r'D:\Document\pythonCode\Programs\Pwormppp\网易云音乐下载\music_files'
pathn = StringVar()
index = 0
default_loading = 0  # 开启tk默认加载foldpath
switch_num = 0
current_index = None
previous_index = None
time_ = 0


def find():         
    """导入文件夹音乐"""
    # 本地音乐文件地址
    global default_loading
    global folder_path
    global music_list
    global current_index

    if not default_loading:  # 第一次打开(开启tk会自动打开一次，即默认)
        folder_path = r"D:\Document\pythonCode\Programs\Pwormppp\网易云音乐下载\music_files"
        default_loading = 1
    else:
        folder_path_fu = callback1()
        if folder_path_fu:
            folder_path = folder_path_fu
            pause_resume.set('播放')
            current_index = -1
        else:
            pass
    folder_list = os.listdir(folder_path)  # 遍历文件夹里面每个文件
    music_list = []
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
    """播放单个文件"""
    f = callback2()  # 选择制定文件
    pygame.mixer.init()
    try:
        pygame.mixer.music.load(f)
        pygame.mixer.music.play()
        musicName.set("playing "+f.split('/')[-1])
    except:
        pass
    pathn.set(f)

def order_play():
    """顺序播放"""
    global index
    global previous_index
    global current_index
    previous_index = current_index
    nextMusic = music_list[index]
    
    if not pygame.mixer.music.get_busy():
        # 按顺序播放一首歌曲
        jdt.set(value=0)
        print(nextMusic)
        print(index)
        current_index = index   # 对现在正在播放歌曲的存储
        pygame.mixer.music.load(folder_path+'\\'+nextMusic)
        # 播放一次
        pygame.mixer.music.play(1)

        global time_
        if previous_index != current_index:  # 让滑块不动的情况，换首歌=0
            time_ =0

        o1.select_clear(0,END)
        o1.select_set(current_index)   # 播放哪一首，就标那一首
        o1.activate(current_index)

        if len(music_list)-1 == index:
            index = 0                            # 下一首歌的预选
        else:
            index = index + 1
        musicName.set('playing ' +nextMusic)
    else:
        time.sleep(0.1)
        global time_from
        global current_long
        time_from = jdt.get()  # jdt读数，要传到progress_bar
        current_long = pygame.mixer.music.get_pos()/1000
        time_jd = float(current_long+time_) # 自带的一首歌播放时间
                                    # time_为 进度条所指的时间 - 之前一首歌播放的时间
        musicTime.set('已播放 {:0>2d}:{:0>2d}'.format(int(time_jd//60),int(time_jd%60)))

def select_play():
    """随机播放"""
    global index
    global previous_index
    global current_index
    previous_index = current_index
    nextMusic = music_list[index]

    if not pygame.mixer.music.get_busy():
        # 随机播放一首歌曲
        jdt.set(value=0)
        print(nextMusic)
        print(index)
        current_index = index   # 对现在正在播放歌曲的存储
        pygame.mixer.music.load(folder_path+'\\'+nextMusic)
        # 播放一次
        pygame.mixer.music.play(1)

        global time_
        if previous_index != current_index:  # 让滑块不动的情况，换首歌=0
            time_ =0

        o1.select_clear(0,END)
        o1.select_set(current_index)   # 播放哪一首，就光标那一首
        o1.activate(current_index)

        index = choice(list(range(len(music_list))))  # 下一首歌的预选
        musicName.set('playing ' + nextMusic)
    else:
        time.sleep(0.1)
        global time_from
        global current_long
        time_from = jdt.get()
        current_long = pygame.mixer.music.get_pos()/1000
        time_jd = float(current_long+time_)

        musicTime.set('已播放 {:0>2d}:{:0>2d}'.format(int(time_jd//60),int(time_jd%60)))

def switch_j():
    """用于判断顺序随机"""
    global switch_num
    if switch_judge.get() == '顺序':
        switch_num = 1
        switch_judge.set('随机')
    elif switch_judge.get() == '随机':
        switch_num = 0
        switch_judge.set('顺序')

def play():
    """点击播放后运行该函数"""
    global folder_path
    global switch_num
    
    if len(music_list):
        # 初始化混音器设备
        pygame.mixer.init()
        try:
            pygame.mixer.music.stop()
            pause_resume.set(value='暂停')
        except:
            pass

        while playing:
            if switch_num:
                select_play()
            else:
                order_play()
        musicTime.set('已停止播放')
        pause_resume.set('播放')
            
def click_play():
    """点击播放按钮"""
    global index
    global current_index
    if pause_resume.get() == '暂停':
        pause_resume.set(value='继续')
        pygame.mixer.music.pause()
        return

    elif pause_resume.get() == '继续':
        pause_resume.set(value='暂停')
        pygame.mixer.music.unpause()
        return
    try:
        music_name=o1.get(o1.curselection())+'.mp3'
        index = music_list.index(music_name)
    except:
        pass

    if  index != current_index:
        pause_resume.set(value='暂停')

        global playing
        playing = True

        a_thread = threading.Thread(target=play, daemon=True)
        a_thread.start()

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
    global current_index
    try:
        music_name = o1.get(o1.curselection())+'.mp3'
        music_name_j = music_list[current_index]
        # print(music_name_j, music_name)

        if music_name != music_name_j:   # and pause_resume.get() == '暂停'
            pause_resume.set(value='播放')
        elif music_name == music_name_j and pause_resume.get() == '播放':
            pause_resume.set(value='暂停')
        else:
            pass
    except:
        pass

def volume_popup_click(event):
    """音量滑块弹出"""
    s.grid(row=2, column=7, rowspan=3, sticky=S, padx=(30,0),pady=(0,30)) 
def volume_hide(event):
    """滑块隐藏"""
    s.grid_forget()

def control_volume(value=0.5):  # 参数为scale的值
    """滑块控制声音"""
    pygame.mixer.music.set_volume(float(value))  # 设置声音大小(pygame内声音最大值为1)
    s.set(float(value))

def volume_increase_click():
    """增大音量"""
    value = pygame.mixer.music.get_volume()
    if value < 1:
        value += 0.02
    pygame.mixer.music.set_volume(float(value)) # 控制音量
    s.set(float(value))  # 控制滑块

def volume_decrease_click():
    """降低音量"""
    value = pygame.mixer.music.get_volume()
    if value > 0:
        value -= 0.02
    pygame.mixer.music.set_volume(float(value)) # 控制音量
    s.set(float(value))   # 控制滑块

def progress_bar(value=0):
    """进度条"""
    global folder_path
    global current_index
    global previous_index
    global time_from
    global time_
    
    music_name = music_list[current_index]
    pat = folder_path+'\\'+music_name
    audio=MP3(pat)
    music_long=audio.info.length
    time_to = jdt.get()

    time_jd = float(time_to/100)*music_long
    time_ = time_jd
    # print('ju:{},cur:{}'.format(previous_index, current_index))

    if previous_index != current_index:  # 做滑块拉回的判断
        time_ = time_jd                   # 对play下的顺序随机播放改变
    elif time_to < time_from:
        time_ = time_jd-current_long

    try:
        pygame.mixer.music.set_pos(float(time_jd))  # 设置播放的位置gl
    except:
        pass

def next_one_music():
    """下一首"""
    if music_list:
        global playing
        playing = False
        try:
            pygame.mixer.music.stop()
        except:
            pass
        pause_resume.set('暂停')
        playing = True

        a_thread = threading.Thread(target=play, daemon=True)
        a_thread.start()

def previous_one_music():
    """上一首"""
    if music_list:
        global playing
        playing = False
        pygame.mixer.music.stop()
        pause_resume.set('暂停')
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
    pygame.mixer.music.stop()
    
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

# 菜单栏---------------------------------------------
def introduce():
    msg.showinfo('v1.4版本功能介绍', 
    message= '在music player v1.4中功能不算太全,\n'
        '但能满足基本使用需求,播放暂停随机\n'
        '播放等等，缺陷即进度条不会随着拉长,\n'
        '但能控制进度条到的地方,在功能帮助\n'
        '中详细说明。经测试，不连续点击至崩\n'
        ',能正常平稳运行,未遇到非常严重的bug\n'
        ',请放心使用本产品。')
def ss_intro():
    texts = '默认为顺序播放,随时可切换成随机播放'
    msg.showinfo('顺序/随机 功能介绍', texts)
def play_menu_intro():
    msg.showinfo('播放歌单 功能介绍', 
    message = '文件夹默认为music_files内MP3文件\n'
            ',单击播放歌单可自行选择文件夹所在\n'
            '绝对地址,然后在左框中会展示出文件\n'
            '夹的所有MP3文件,支持双击进行播放。')
def select_intro():
    msg.showinfo('选择文件 功能介绍', 
    message = '选择文件并进行播放只针对单个\n'
        '的文件进行播放,也是选择本地的\n'
        '某个MP3文件进行播放,暂时不支持\n'
        '顺序与随机播放')
def scale_intro():
    texts = '可拖动滑块进行进度的控制及音量的大小改变'
    msg.showinfo('scale 功能介绍', texts)
def other_intro():
    texts = '可下一首/上一首进行音乐的切换\n\
,对音量大小由+-控制。新增功能：\n\
附加功能中能进行背景设置。'
    msg.showinfo('其他 功能介绍', texts)
def bomb():
    msg.showwarning('BOMB','炸弹即将被引爆')

# 背景set
 #FFD99B 浅橙  
 #FFC465 深橙
 #85FFBB 深绿
 #99FFCC 浅绿
def bg1_set():
    lable1.config(image=bg1)
    module_list = [m1,sel_file,switch_play,volume_popup,volume_increase,
    volume_decrease,next_one,previous_one,music_name,music_time,contiplay
    ,stoplay,pause]
    for i in module_list:
        i.config(bg='#8DFCDD')
    for j in [jdt, s]:
        j.config(troughcolor='#CCFCEF', bg='#33FF99')
    o1.config(bg='#B4F4CB')
    songs.config(bg='#85F0AC')

def bg2_set():
    lable1.config(image=bg2)
    module_list1 = [m1,sel_file,music_name,music_time]
    module_list2 = [switch_play,volume_popup,volume_increase,
    volume_decrease,next_one,previous_one,contiplay,stoplay,pause]

    for i in module_list1:
        i.config(bg='#99FFCC') # 浅绿(去饱和)
    for k in module_list2:
        k.config(bg='#85FFBB') # 深绿(加饱和)
    for j in [jdt, s]:
        j.config(troughcolor='#99FFCC', bg='#33FF99')
    o1.config(bg='#85FFBB')           
    songs.config(bg='#99FFCC')

# def next_one_m():
#     global playing
#     playing = True

#     a_thread = threading.Thread(target=play, daemon=True)
#     a_thread.start()

def delete():
    global music_list
    global current_index
    try:
        if music_list:
            music_get = o1.get(o1.curselection()) + '.mp3'
            de_index = music_list.index(music_get)
            o1.delete(de_index)
            music_list.pop(de_index)
            o1.select_set(de_index)  # 删除操作后设置原来的下一个光标   
            if de_index < current_index:
                current_index -= 1

            # if pygame.mixer.music.get_busy():
            #     if de_index == current_index:
                    # if index == len(music_list):
                    #     index -= 1
                    # next_one_m()
    except:
        pass

def copy():
    pass

def caidan(root, o1):
    menu = Menu(root)

    # 查看栏
    submenu1 = Menu(menu, tearoff=0)
    submenu1.add_command(label='版本介绍', command=introduce)
            # submenu1.add_command(label='版本介绍')
    submenu1_1 = Menu(menu, tearoff=0)
    submenu1_1.add_command(label='music_player v1.4')
    submenu1.add_cascade(menu=submenu1_1, label='版本介绍')
            # submenu1.add_command(label='关于作者')
    submenu1_2 = Menu(menu, tearoff=0)
    submenu1_2.add_command(label='author: jue')
    submenu1.add_cascade(menu=submenu1_2, label='关于作者')
    menu.add_cascade(menu=submenu1, label='查看')

    # 帮助栏
    submenu2 = Menu(menu, tearoff=0)
    submenu2_1 = Menu(menu, tearoff=0)
    submenu2_1.add_command(label='顺序/随机', command=ss_intro)
    submenu2_1.add_command(label='播放歌单', command=play_menu_intro)
    submenu2_1.add_command(label='选择文件', command=select_intro)
    submenu2_1.add_command(label='进度/音量', command=scale_intro)
    submenu2_1.add_command(label='其他', command=other_intro)
    submenu2_2 = Menu(menu, tearoff=0)
    submenu2_2.add_command(label='恁这么聪明,肯定会用哈!')
    submenu2.add_cascade(menu=submenu2_1, label='功能帮助')
    submenu2.add_cascade(menu=submenu2_2, label='使用帮助')
    menu.add_cascade(menu=submenu2, label='帮助')

    # 附加功能栏
    submenu3=Menu(menu,tearoff=0)
    submenu3_1 = Menu(menu, tearoff=0)
    submenu3_1.add_command(label='深绿湖纹', command=bg1_set)
    submenu3_1.add_command(label='浅绿湖纹', command=bg2_set)
    submenu3.add_cascade(menu=submenu3_1, label='背景set')
    submenu3.add_command(label='福利',command=bomb)
    menu.add_cascade(menu=submenu3,label='附加功能')

    root.config(menu=menu)

    menu2 = Menu(root, tearoff=False)
    # 歌名栏o1中右键菜单
    menu2.add_command(label="删除", command=delete)
    menu2.add_command(label="复制", command=copy)
    def popup(event):
        menu2.post(event.x_root, event.y_root)
    o1.bind("<Button-3>", popup)

# 菜单栏---------------------------------------------

if __name__ == "__main__":

    # 关闭窗口
    root.protocol('WM_DELETE_WINDOW', closeWindow) # x掉窗口并运行closeWindow

    # tk背景设置
    file1 = 'images/bg1.png'
    file2 = 'images/bg2.png'
    bg1 = PhotoImage(file=file1)
    bg2 = PhotoImage(file=file2)
    lable1 = Label(image=bg1, bd=0)
    lable1.grid(rowspan=6, columnspan=9)

    #歌单
    o1=Listbox(root,width=25, heigh=24, font=("楷书", 15), bd=3, selectmode=BROWSE,bg="#B4F4CB") # 
    o1.grid(row=2, column=0, columnspan=4)  # selectmode=tkinter.MULTIPLE 不用ctrl/shift就能多选
    find()  # 运行第一次默认加载foldpath
    o1.bind("<Double-Button-1>",click_two_play)  # 绑定双击
    o1.bind("<ButtonRelease-1>", click_one_play) # 绑定单击释放时的动作

    # 打开菜单
    caidan(root, o1)

    # 播放歌单
    m1 = Button(root, text='播放歌单', command=find,width=10,heigh=2, font=("黑体", 12), bg="#8DFCDD")
    m1.grid(row=0, rowspan=2, column=0, columnspan=4)

    # 选择文件
    sel_file = Button(root, text="选择文件/播放", command=alone_play, width=10, bg="#8DFCDD")
    sel_file.grid(row=0,rowspan=2, column=4, columnspan=1,sticky=E)
    entry1 = Entry(root, text=pathn, width=25, state='readonly', bd=2,bg="#8DFCDD")
    entry1.grid(row=0,rowspan=2, column=5, columnspan=1,sticky=W) # 只能写入

    # 转换播放模式  
    switch_judge = StringVar(root, value='顺序')
    switch_play = Button(root, textvariable=switch_judge,
        width=5, bg="#8DFCDD", command=switch_j)
    switch_play.grid(row=3, rowspan=3, column=8)

    # 音量弹出键
    volume_popup = Label(root, text='音量', bg="#8DFCDD", width=5)
    volume_popup.grid(row=3, rowspan=3, column=7, padx=(30,0)) # , command=volume_popup_click
    volume_popup.bind("<Enter>", volume_popup_click) 

    # 音量大小设置
    volume_increase = Button(root, text='+', bg="#8DFCDD", width=5, command=volume_increase_click)
    volume_increase.grid(row=3, rowspan=1, column=2, columnspan=1)
    volume_decrease = Button(root, text='-', bg="#8DFCDD", width=5, command=volume_decrease_click)
    volume_decrease.grid(row=5, rowspan=1, column=2, columnspan=1) #, pady=(10,30) sticky

    # 进度条
    # time_var = StringVar(value=0)
    jdt = Scale(root, from_=0, to=100, orient="horizontal", length=550,relief=GROOVE,
    sliderrelief=GROOVE, sliderlength=10, activebackground='black',bg="#33FF99",width=10,
        repeatinterval=100, command=progress_bar,resolution=1,show=0,troughcolor="#CCFCEF")# variable=time_var,, label="进度"
    jdt.grid(row=3,rowspan=3, column=4, columnspan=3)

    # 上下首
    next_one = Button(root, text='>', bg="#8DFCDD", command=next_one_music)  # 下一首
    next_one.grid(row=3, rowspan=3, column=3, columnspan=1, sticky=W)
    previous_one = Button(root, text='<', bg="#8DFCDD", command=previous_one_music)  # 上一首
    previous_one.grid(row=3, rowspan=3, column=1, columnspan=1, sticky=E)

    # 点击播放
    pause_resume = StringVar(root, value='播放')
    pause = Button(root, textvariable=pause_resume, width=5,command=click_play, bg="#8DFCDD")  # lambda:click_play(music_name)
    pause.grid(row=4, column=2, columnspan=1, rowspan=1)
    # pause['state']='disable'

    # 重新播放 停止播放
    contiplay = Button(root, text='重新播放', command=re_play, bg="#8DFCDD")
    contiplay.grid(row=3, rowspan=2, column=0, columnspan=1)
    stoplay = Button(root, text='停止播放', command=stop, bg="#8DFCDD")
    stoplay.grid(row=4, rowspan=2, column=0, columnspan=1)

    # 播放显示
    musicName = StringVar(value='暂无播放')
    music_name = Label(root, textvariable=musicName, width=22,heigh=1, font=("楷书", 12),
    bd=4,bg="#8DFCDD")  # 
    music_name.grid(row=0, rowspan=1, column=7, columnspan=2)
    musicTime = StringVar(value='')
    music_time = Label(root, textvariable=musicTime, width=20,heigh=1, font=("Helvetica", 12),
    bg="#8DFCDD",bd=2, )
    music_time.grid(row=1, rowspan=1, column=7, columnspan=2)
    musicTime.set('00:00')

    # songs listbox
    songs = Listbox(root, bg="#85F0AC", width=104, heigh=28, bd=5,)
    songs.grid(row=2, rowspan=1, column=4, columnspan=5)

    # kong
    kong = Button(root, width=5,heigh=1, font=("Helvetica", 12),bd=0,image=bg1,bg='blue')  # 暂时隐藏在背景下
    kong.grid(row=0, rowspan=2, column=6, columnspan=1)  # 

    # 音量控制
    #注意，Scale的回调函数需要给定形参，当触发时会将Scale的值传给函数
    # , orient=HORIZONTAL # VERTICAL # , showvalue=0 , label='音量'
    s = Scale(root, from_=1, to=0,length=100, width=9, sliderlength=10,borderwidth=0.5,      # tickinterval=2, 
    resolution=0.02, command=control_volume, showvalu=0, troughcolor="#CCFCEF",bg="#33FF99",
    sliderrelief=GROOVE, activebackground="black") 
    s.grid_forget()   # 隐藏音量
    s.bind("<Leave>", volume_hide)
    pygame.mixer.init()
    pygame.mixer.music.set_volume(float(0.5))
    s.set(0.5)

    # 开启循环
    root.mainloop()
