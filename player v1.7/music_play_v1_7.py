"""
——2020/5/21——
# 支持对.MP3 .ogg格式音乐的播放
——2020/5/20——
# 对线程问题进行了解决，暂未发现严重bug

@ -*- coding:utf-8 -*-
@Name   : 音乐播放器 player v1.7.1
@Author : jue
@Time   : 2020/3/24
@Note   : play musics
"""

import os, sys
import time
from random import choice
from threading import Thread , Lock
from urllib import request
from selenium import webdriver
import pygame
from mutagen.mp3 import MP3
from tkinter import *
import tkinter.messagebox as msg
import tkinter.scrolledtext as scr
from tkinter.filedialog import askdirectory, askopenfilename # , askopenfilenames


class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
 
    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, _cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 30
        y = y + cy + self.widget.winfo_rooty() +30
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
 
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "10", "normal"))
        label.grid()
 
    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def createToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)  # copy 的


path = os.path.dirname(os.path.abspath(__file__))
path_m = path+'\\songs\\music_files'

default_loading = 0  # 开启tk默认加载foldpath
switch_num = 0
index = 0
current_index = None
previous_index = None
music_l = None
time_ = 0
time_from = 0
push_scale = True
volume_popup_judge = True # volume popup judge
thread_judge = 0
num = 1
MUSIC_FORMAT = None


def music_download():
    id_name = entry2.get()
    if id_name:
        try:
            option = webdriver.ChromeOptions()
            option.add_argument('--headless')
            driver = webdriver.Chrome(chrome_options=option)
            driver.get('https://music.163.com/#/search/m/?s={}&type=1'.format(id_name))
            print(driver.title)
            time.sleep(1)

            driver.switch_to.frame('g_iframe')
            req = driver.find_elements_by_id('m-search')
            # href = req[0].find_element_by_xpath('.//div[@class="item f-cb h-flag even "]/div[2]//a').get_attribute('href')
            # .//div[@class="srchsongst"]/div[1]/div[2]//a
            href = req[0].find_element_by_xpath('.//div[@class="srchsongst"]/div[1]/div[2]//a')
            # print(href)
            id_ = href.get_attribute('href').split('id=')[-1]
            id_name = href.find_element_by_xpath('./b').get_attribute('title')
            # print(id_name)
            singer_name = req[0].find_element_by_xpath('.//div[@class="srchsongst"]/div[1]/div[4]/div[1]').text
            print(singer_name)

            item = {}
            item['id'] = id_
            item['id_name'] = id_name
            item['singer_name'] = singer_name

            if id_name+'.mp3' not in music_list:
                music_save(item)
            
            s_path = os.path.dirname(os.path.abspath('__file__'))+r'\songs\lyrics\{}.txt'.format(id_name)
            if not os.path.exists(s_path):
                lyrics_get(driver, item)
            else:
                driver.quit()
            
        except Exception as err:
            print('异常错误：{}'.format(err))
    else:
        pass
    
    entry2.delete(0,END)

def music_save(item):
    global music_list

    try:
        id = item['id']
        id_name = item['id_name']
        url = 'http://music.163.com/song/media/outer/url?id={}.mp3'.format(id)

        os.makedirs(path_m,exist_ok=True)
        request.urlretrieve(url,path_m+'/{}.mp3'.format(id_name))
        o1.insert(END, id_name)
        music_list.append(id_name+'.mp3')   
    except:
        print('歌曲下载错误')

def lyrics_get(driver, item):

    try:
        id_ = item['id']
        id_name = item['id_name']
        singer_name = item['singer_name']
        driver.get('https://music.163.com/#/song?id={}'.format(id_))
        print(driver.title, '-------------')
        time.sleep(0.5)

        driver.switch_to.frame('g_iframe')
        req = driver.find_elements_by_id('lyric-content')

        driver.execute_script("window.scrollBy(0, 500)")  # "window.scrollBy(0,1200)"

        click_extend = driver.find_element_by_id('flag_ctrl').find_element_by_tag_name('i')
        click_extend.click()

        # print(req[0].text)
        with open('songs/lyrics/{}.txt'.format(id_name), 'w', encoding='utf-8') as f:
            f.write('演唱 : {}\n'.format(singer_name))
            f.write(req[0].text)

    except:
        print('歌词下载错误')
    
    finally:
        driver.quit()

def music_get():
    a_thread = Thread(target=music_download, daemon=True)
    a_thread.start()


def find():         
    """导入文件夹音乐"""
    # 本地音乐文件地址
    global default_loading
    global folder_path
    global music_list
    global current_index
    global index

    if not default_loading:  # 第一次打开(开启tk会自动打开一次，即默认)
        folder_path = path_m
        default_loading = 1
    else:
        folder_path_fu = callback1()
        if folder_path_fu:
            folder_path = folder_path_fu
            # pause_resume.set('ID')  暂定
            current_index, index = None, 0
        else:
            return
    folder_list = os.listdir(folder_path)  # 遍历文件夹里面每个文件
    music_list = []
    o1.delete(0,END) # 清除之前listbox列表
    for i in folder_list:  # 将文件夹里的文件按顺序传提给变量i  此处区别os.walk()

        if os.path.splitext(i)[1] == '.mp3' or '.ogg':  # 提取i文件特定后缀'.***'
            music_list.append(i)
            o1.insert("end",i.split('.')[0])
    print(music_list)

def callback1():  # 搜索并选择文件夹
    path_ = askdirectory()
    return path_

def callback2():  # 搜索本地文件
    path_ = askopenfilename(filetypes=[("mp3 file", "*.mp3"),("ogg file", "*.ogg"),("all","*.*")]) #   askdirectory()
    return path_


def alone_play():  # 播放音乐
    """播放单个文件"""

    f = callback2()  # 选择制定文件
    pygame.mixer.init()
    try:
        pygame.mixer.music.load(f)
        pygame.mixer.music.play()
        musicName.set(f.split('/')[-1])
    except:
        pass
    pathn.set(f)

def order_play():
    """顺序播放"""
    global index

    try:
        if len(music_list)-1 == index:
            index = 0                            # 下一首歌的预选
        else:
            index = index + 1
    except:
        pass
    finally:
        print(previous_index, current_index, index)

def select_play():
    """随机播放"""
    global index

    try:
        index = choice(list(range(len(music_list))))  # 下一首歌的预选
    except:
        pass
    finally:
        print(previous_index, current_index, index)

def single_cycle_play():
    """单曲循环"""
    global index
    try:
        index = current_index
    except:
        pass
    finally:
        print(previous_index, current_index, index)

def scale_auto_go(time_jd, music_l):
    # print(time_jd)
    time_auto_to = int(time_jd / float(music_l)*200)
    jdt.set(time_auto_to)

def switch_j():
    """用于判断顺序随机"""

    global switch_num
    if switch_judge.get() == '顺序':
        switch_num = 1
        select_play()
        switch_judge.set('随机')

    elif switch_judge.get() == '随机':
        switch_num = 2
        single_cycle_play()
        switch_judge.set('单曲循环')

    elif switch_judge.get() == '单曲循环':
        switch_num = 0
        order_play()
        switch_judge.set('顺序')

def play_options():
    """select playing method"""

    if music_list:
        global index
        global previous_index
        global current_index
        global music_l
        global thread_judge

        if thread_judge:
            print('爱你O')
            raise TypeError('线程销毁')
        
        previous_index = current_index
        nextMusic = music_list[index]

        if not pygame.mixer.music.get_busy():
            # 随机播放一首歌曲
            jdt.set(value=0)
            pause_resume.set('| |')
            print(nextMusic)
            print(index)
            current_index = index   # 对现在正在播放歌曲的存储

            o1.select_clear(0,END)
            o1.select_set(current_index)   # 播放哪一首，就光标那一首
            o1.activate(current_index)
            musicName.set(nextMusic.split(' - (')[0].split('.')[0])

            if nextMusic.split('.')[1] == 'ogg':
                jdt['state'] = 'disable'
                music_l = 0
                musicLong.set('00:00')
            else:
                music_l = MP3(folder_path+'\\'+music_list[current_index]).info.length
                musicLong.set('{:0>2d}:{:0>2d}'.format(int(music_l//60),int(music_l%60)))

            m_name=nextMusic.split('.')[0]
            s_path = os.path.dirname(os.path.abspath('__file__'))+r'\songs\lyrics\{}.txt'.format(m_name)
            if os.path.exists(s_path):
                lyrics_display(m_name)
            else:
                songs.delete(0, END)
                songs.insert(0, '暂无歌词')

            global time_
            time_ = 0
            # if previous_index != current_index:  # 让滑块不动的情况，换首歌=0
            #     time_ =0

            try:
                pygame.mixer.music.load(folder_path+'\\'+nextMusic)
                pygame.mixer.music.play(1) # 播放一次
            except Exception as err:
                print('err','请充值vip会员')
                songs.delete(0,END)
                songs.insert('请充值vip会员')
                return

            if switch_num == 0:
                order_play()
            elif switch_num == 1:
                select_play()
            elif switch_num  == 2:
                single_cycle_play()
            
        else:
            time.sleep(0.1)
            global time_from
            global current_long
            
            
            time_from = jdt.get()  # jdt读数，要传到progress_bar
            current_long = float(pygame.mixer.music.get_pos()/1000)
            time_jd = float(current_long+time_) # 自带的一首歌播放时间
                                        # time_为 (进度条所指的时间 - 之前一首歌播放的时间)
            if time_jd < 0:
                time_jd = 0
            musicTime.set('已播放 {:0>2d}:{:0>2d}'.format(int(time_jd//60),int(time_jd%60)))
            if music_l:
                scale_auto_go(time_jd, music_l)

    else:
        musicName.set('暂无播放')
        musicTime.set('00:00')

class Music(object):

    def __init__(self):
        pygame.mixer.init()
        self._lock = Lock()

    def stop_music(self):

        global thread_judge
        thread_judge = 1
        time.sleep(0.2)

        try:
            pygame.mixer.music.stop()
        finally:
            self._lock.release()

    def play_music(self):

        global folder_path
        global switch_num
        global thread_judge
        
        if len(music_list):
            self._lock.acquire()
            self.stop_music()

            jdt['state'] = NORMAL
            thread_judge = 0
            while playing:
                play_options()
            
            # raise TypeError('线程销毁')

class MusicThread(Thread):

    def __init__(self, music):
        super().__init__(daemon=True)
        self._music = music

    def run(self):
        self._music.play_music()


def lyrics_display(m_name):
    """display the lyrics of the song"""

    songs.delete(0, END)
    file = 'songs/lyrics/{}.txt'.format(m_name)

    codedFormat = ['utf-8', 'gbk']
    codedIndex = 0

    while True:
        try:
            with open(file, 'r', encoding=codedFormat[codedIndex]) as f:
                
                songlines = f.readlines()
                if songlines[-1] == '收起':
                    songlines = songlines[:-1]
                conum = diffrent_value(m_name)
                songs.insert(0, '{:^{}}'.format(m_name, conum))
                songs.insert(END, '')

                for i in [c.strip() for c in songlines]:
                    conum = diffrent_value(i)
                    # print('{:^{}}\n'.format(i, conum))
                    songs.insert(END, '{:^{}}\n'.format(i, conum))
                    songs.insert(END, '')

            print('歌词加载成功')
            return
        except:
            codedIndex += 1
            
def diffrent_value(charString, columns=72):
    """差值减少误差"""
    dif = len(bytes(charString.encode('gbk'))) - len(charString)
    if dif//5 > 0:
        dif -= dif//5
    conum = columns - dif

    return conum


def click_play():
    """点击播放按钮"""

    global index
    global current_index

    if pause_resume.get() == '| |':
        pause_resume.set(value='D')
        pygame.mixer.music.pause()
        return  # debug

    elif pause_resume.get() == 'D':
        pause_resume.set(value='| |')
        pygame.mixer.music.unpause()
        return

    try:
        music_name=o1.get(o1.curselection())+MUSIC_FORMAT
        index = music_list.index(music_name)
    except:
        pass

    if  index != current_index:
        pause_resume.set(value='| |')

        global playing
        playing = True

        music = Music()
        t = MusicThread(music)
        t.start()

def next_one_music():
    """下一首"""

    # jdt.set(200)
    if music_list:

        pause_resume.set('| |')
        
        music = Music()
        t = MusicThread(music)
        t.start()

def previous_one_music():
    """上一首"""

    if music_list:
        
        global index
        if index == 0:
            index = len(music_list)-2
        elif index == 1:
            index = len(music_list)-1
        else:
            index -= 2

        pause_resume.set('| |')

        music = Music()
        t = MusicThread(music)
        t.start()

def rewind_play():
    """重新播放"""
    pygame.mixer.music.rewind()
    scale_auto_go(0, music_l)


def stop_play():
    """| |音乐"""
    global playing
    global current_index
    
    playing = False
    pygame.mixer.music.stop()
    current_index = None


def click_two_play(self):   # listbox内的鼠标左键单两次点击事件(不带参)
    """双击listbox内歌曲名"""

    global index

    # music_name=o1.index(o1.curselection())+'.mp3'
    # print(o1.get(o1.curselection()))
    index = o1.index(o1.curselection())

    global playing
    playing = True
    
    music = Music()
    t = MusicThread(music)
    t.start()


def click_one_play(self):  # listbox内的鼠标左键单次点击事件
    """根据listbox内歌曲名判断播放| |"""

    global current_index
 
    try:
        music_name = o1.get(o1.curselection())+'.mp3'
        music_name_j = music_list[current_index]
        # print(music_name_j, music_name)

        if music_name != music_name_j:   # and pause_resume.get() == '| |'
            pause_resume.set(value='ID')
        elif music_name == music_name_j and pause_resume.get() == 'ID':
            pause_resume.set(value='| |')
        else:
            pass
    except:
        pass


def volume_popup_click():
    """音量滑块弹出"""

    global volume_popup_judge

    if volume_popup_judge:
        s.grid(row=2, column=7, rowspan=3, sticky=S, padx=(99,0),pady=(0,30))
        # 在音量键上也能滚动滑块(显示时)
        volume_popup.bind("<MouseWheel>", control_volume_)
        volume_popup_judge = False

    else:
        s.grid_forget()
        volume_popup_judge = True
    
def volume_hide(event):
    """滑块隐藏"""

    global volume_popup_judge

    s.grid_forget()
    volume_popup_judge = True

def control_volume(value=0.5):  # 参数为scale的值
    """滑块控制声音"""
    # 控制音量
    pygame.mixer.music.set_volume(float(value))  # 设置声音大小(pygame内声音最大值为1)
    s.set(float(value))

def volume_increase_click():
    """增大音量"""
    s.grid(row=2, column=7, rowspan=3, sticky=S, padx=(99,0),pady=(0,30))
    value = pygame.mixer.music.get_volume()
    if value < 1:
        value += 0.1
        s.set(float(value))  # 控制滑块

def volume_decrease_click():
    """降低音量"""
    s.grid(row=2, column=7, rowspan=3, sticky=S, padx=(99,0),pady=(0,30))
    value = pygame.mixer.music.get_volume()
    if value > 0:
        value -= 0.1
        s.set(float(value))   # 控制滑块

def control_volume_(e):  # 参数为scale的值
    """滑块控制声音"""
    # .delta：用于描述鼠标滚动事件，表示滚轮滚动的距离。
    if not volume_popup_judge:
        if e.delta > 0:
            s.set(s.get()+0.05)
        else:
            s.set(s.get()-0.05)
    else: # 滑块未显示时滚动无效
        pass


def progress_bar(value=0):
    """进度条"""
    global current_index
    global previous_index
    global time_
    global push_scale

    time_to = jdt.get()
    if abs(time_to - time_from) > 1:
        push_scale = True
    else:
        push_scale = False

    if push_scale:
        # print('jdt起作用')
        time_jd = float(time_to/200*music_l) # music_l 从order_play全局变量而来
        time_ = time_jd
        # print('ju:{},cur:{}'.format(previous_index, current_index))
        if previous_index != current_index:  # 做滑块自动到0的判断(换了首歌)
            time_ = time_jd
        else:                  # 滑块往回拉(或往后)
            time_ = time_jd-current_long

        try:
            pygame.mixer.music.set_pos(float(time_jd))  # 设置播放的位置gl
        except:
            pass

        push_scale = False
    

def closeWindow():
    """关闭窗口"""
    global playing
    playing = False
    time.sleep(0.3)
    try:
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.quit()
    except:
        pass

    root.destroy() # 退出root

# 菜单栏---------------------------------------------
def introduce():
    msg.showinfo('v1.7.1版本功能介绍', 
    message= '在music player v1.7.1中功能不算太全,\n'
            '但能满足基本使用需求,播放|随机播放等\n'
            '等，能控制进度条，其在功能帮助中详细\n'
            '说明。经测试，能正常切歌,正常平稳运行\n'
            ',未遇到非常严重的bug,请放心使用本产品。'
            )

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
    texts = '可拖动滑块进行进度条的控制及\n\
        音量的大小改变。'
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
def bg1_set(): # 深绿湖纹
    lable1.config(image=bg1)
    module_list = [m1,sel_file,search_file,switch_play,volume_popup,
    volume_increase,volume_decrease,next_one,previous_one,music_name,
    music_time,contiplay,music_long,stoplay,pause]
    for i in module_list:
        i.config(bg='#8DFCDD', fg='#000000')
    for j in [jdt, s]:
        j.config(troughcolor='#CCFCEF', bg='#33FF99', activebackground='black')
    o1.config(bg='#B4F4CB', fg='#000000', selectbackground="#008D63")
    songs.config(bg='#85F0AC', fg='#000000', selectbackground="#008D63")
    kong.config(image=bg1)

def bg2_set(): # 浅绿湖纹
    lable1.config(image=bg2)
    module_list1 = [m1,sel_file,search_file,music_name,music_time]
    module_list2 = [switch_play,volume_popup,volume_increase,music_long,
    volume_decrease,next_one,previous_one,contiplay,stoplay,pause]

    for i in module_list1:
        i.config(bg='#99FFCC', fg='#000000') # 浅绿(去饱和)
    for k in module_list2:
        k.config(bg='#85FFBB', fg='#000000') # 深绿(加饱和)
    for j in [jdt, s]:
        j.config(troughcolor='#99FFCC', bg='#00CC66', activebackground='black')
    o1.config(bg='#85FFBB', fg='#000000', selectbackground="#00CC66")           
    songs.config(bg='#99FFCC', fg='#000000', selectbackground="#00CC66")
    kong.config(image=bg2)

def bg3_set(): # 酷雅黑
    lable1.config(image=bg3)
    module_list = [m1,sel_file,search_file,switch_play,volume_popup,
    volume_increase,volume_decrease,next_one,previous_one,music_name,
    music_time,contiplay,stoplay,pause,music_long]
    for i in module_list:
        i.config(bg='#000000', fg='white')
    for j in [jdt, s]:
        j.config(troughcolor='#E7E6E6', bg='#4F5353', activebackground='black')
    o1.config(bg='#FFFFFF', fg='#000000', selectbackground="blue")
    songs.config(bg='#191919', fg='#FFFFFF', selectbackground="blue")
    kong.config(image=bg3)

def bg3_1_set(): # 酷雅黑红
    lable1.config(image=bg3)
    module_list = [m1,sel_file,search_file,switch_play,volume_popup,
    volume_increase,volume_decrease,next_one,previous_one,music_name,
    music_time,contiplay,stoplay,pause,music_long]
    for i in module_list:
        i.config(bg='#990000', fg='white')
    for j in [jdt, s]:
        j.config(troughcolor='#FF4040', bg='#4F5353', activebackground='black')
    o1.config(bg='white', fg='#191919', selectbackground="#E62121")
    songs.config(bg='#191919', fg='#FFFFFF', selectbackground="#E62121")
    kong.config(image=bg3)

def bg4_set(): # 酷狗蓝
    lable1.config(image=bg4)
    module_list1 = [m1,sel_file,search_file,music_name,music_time]
    module_list2 = [switch_play,volume_popup,volume_increase,music_long,
    volume_decrease,next_one,previous_one,contiplay,stoplay,pause]

    for i in module_list1:
        i.config(bg='#A9CFFF', fg='#000000')
    for k in module_list2:
        k.config(bg='#4799FF', fg='white')
    for j in [jdt, s]:
        j.config(troughcolor='#FFFFFF', bg='#509EFF', activebackground='black')
    o1.config(bg='#4789E8', fg='#FFFFFF', selectbackground="#1D64A8")
    songs.config(bg='#59A3FF', fg='#FFFFFF', selectbackground="#1D64A8")
    kong.config(image=bg4)

def bg5_set(): # 网易云红(1)
    lable1.config(image=bg5)
    module_list = [m1,sel_file,search_file,switch_play,volume_popup,
    volume_increase,volume_decrease,next_one,previous_one,music_name,
    music_time,contiplay,stoplay,pause,music_long]
    for i in module_list:
        i.config(bg='#E62121', fg='white')  #CC0000
    for j in [jdt, s]:
        j.config(troughcolor='#242424', bg='#FFFFFF', activebackground='red')
    o1.config(bg='#242424', fg='#FFFFFF', selectbackground="#F54448")
    songs.config(bg='#242424', fg='#FFFFFF', selectbackground="#F54448")
    kong.config(image=bg5)

def bg6_set(): # 网易云红(2)
    lable1.config(image=bg6)
    module_list = [m1,sel_file,search_file,switch_play,volume_popup,
    volume_increase,volume_decrease,next_one,previous_one,music_name,
    music_time,contiplay,stoplay,pause,music_long]
    for i in module_list:
        i.config(bg='#E62121', fg='white')  #CC0000
    for j in [jdt, s]:
        j.config(troughcolor='#242424', bg='#FFFFFF', activebackground='red')
    o1.config(bg='#FFFFFF', fg='#000000', selectbackground="#3F3F3F")
    songs.config(bg='#FFFFFF', fg='#000000', selectbackground="#3F3F3F")
    kong.config(image=bg6)

def next_one_m():
    global index
    global previous_index
    try:
        index = o1.index(o1.curselection())
    except:
        pass

    global playing
    playing = True
    previous_index = index

    music = Music()
    t = MusicThread(music)
    t.start()

def delete_o1_music():
    global music_list
    global current_index
    global previous_index

    try:
        if music_list:
            # music_get = o1.get(o1.curselection()) + '.mp3'
            # de_index = music_list.index(music_get)
            de_index = o1.curselection()[0]  # 被选中的index
            o1.delete(de_index)
            music_list.pop(de_index) # O(n)
            o1.select_set(de_index)  # 删除操作后设置原来的下一个光标   

            if de_index < current_index:
                previous_index -= 1
                current_index -= 1
            elif de_index == current_index:
                next_one_m()
    except:
        pass

def add_playlist():
    pass

def caidan(root, o1):
    
    menu = Menu(root)

    # 查看栏
    submenu1 = Menu(menu, tearoff=0)
    submenu1.add_command(label='版本介绍', command=introduce)
            # submenu1.add_command(label='版本介绍')
    submenu1_1 = Menu(menu, tearoff=0)
    submenu1_1.add_command(label='music_player v1.7.1')
    submenu1.add_cascade(menu=submenu1_1, label='播放版本')
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
    submenu3_1.add_command(label='酷雅黑', command=bg3_set)
    submenu3_1.add_command(label='酷雅黑红', command=bg3_1_set)
    submenu3_1.add_command(label='酷狗蓝', command=bg4_set)
    submenu3_1.add_command(label='网易云红(1)', command=bg5_set)
    submenu3_1.add_command(label='网易云红(2)', command=bg6_set)
    submenu3.add_cascade(menu=submenu3_1, label='背景set')
    submenu3.add_command(label='福利',command=bomb)
    menu.add_cascade(menu=submenu3,label='附加功能')

    root.config(menu=menu)

    menu2 = Menu(root, tearoff=False)
    # 歌名栏o1中右键菜单
    menu2.add_command(label="删除", command=delete_o1_music)
    menu2.add_command(label="取消", command=add_playlist)
    def popup(event):
        menu2.post(event.x_root, event.y_root)
    o1.bind("<Button-3>", popup)

# 菜单栏---------------------------------------------

if __name__ == "__main__":

    # 关闭窗口
    root = Tk()
    root.geometry('1000x670+183+10')
    root.title('MP3音乐播放器 v1.7.1')
    root.iconbitmap(path+'/images/head.ico')
    root.attributes("-alpha", 0.95)
    root.resizable(False,False)

    root.protocol('WM_DELETE_WINDOW', closeWindow) # x掉窗口并运行closeWindow

    # tk背景设置
    file1 = path+'/images/bg1.png'
    file2 = path+'/images/bg2.png'
    file3 = path+'/images/bg3.png'
    file4 = path+'/images/bg4.png'
    file5 = path+'/images/bg5.png'
    file6 = path+'/images/bg6.png'
    bg1 = PhotoImage(file=file1)
    bg2 = PhotoImage(file=file2)
    bg3 = PhotoImage(file=file3)
    bg4 = PhotoImage(file=file4)
    bg5 = PhotoImage(file=file5)
    bg6 = PhotoImage(file=file6)

    lable1 = Label(image=bg1, bd=0)
    lable1.grid(rowspan=6, columnspan=9)

    #歌单
    scrollbar1 = scr.Scrollbar(root,bd=1, width=12)
    scrollbar1.grid(sticky=E+N+S,row=2, column=3, columnspan=1)
    o1=Listbox(root,width=24, heigh=23, font=("楷书", 15), bd=2, selectmode=BROWSE,bg="#B4F4CB",
            yscrollcommand=scrollbar1.set) # scrollbar重点
    o1.grid(row=2, column=0, columnspan=4,sticky=W+N+S)  # selectmode=tkinter.MULTIPLE 不用ctrl/shift就能多选
    find()  # 运行第一次默认加载foldpath
    # for i in range(100):
    #     o1.insert(END, i)
    o1.bind("<Double-Button-1>",click_two_play)  # 绑定双击
    o1.bind("<ButtonRelease-1>", click_one_play) # 绑定单击释放时的动作
    scrollbar1.config(command = o1.yview)

    # 打开菜单N+S
    caidan(root, o1)

    # DD歌单
    m1 = Button(root, text='播放歌单', command=find,width=10,heigh=2, font=("黑体", 12), bg="#8DFCDD")
    m1.grid(row=0, rowspan=2, column=0, columnspan=4)

    # 选择文件
    pathn = StringVar()
    sel_file = Button(root, text="选择文件/播放", command=alone_play, width=10, bg="#8DFCDD")
    sel_file.grid(row=0,rowspan=1, column=4, columnspan=1,sticky=E)
    entry1 = Entry(root, text=pathn, width=25, bd=2,bg="#FFFFFF")
    entry1.grid(row=0,rowspan=1, column=5, columnspan=1,sticky=W) # 只能写入 , state='readonly'

    # 搜索下载
    search_file = Button(root, text="歌名/下载", command=music_get, width=10, bg="#8DFCDD")
    search_file.grid(row=1,rowspan=1, column=4, columnspan=1,sticky=E)
    entry2 = Entry(root, width=25, bd=2)
    entry2.grid(row=1,rowspan=1, column=5, columnspan=1,sticky=W)

    # 转换DD模式  
    switch_judge = StringVar(root, value='顺序')
    switch_play = Button(root, textvariable=switch_judge,
        width=6, bg="#8DFCDD", command=switch_j)
    switch_play.grid(row=3, rowspan=3, column=8, sticky=E, padx=(0,15))

    # 音量弹出键(点击)
    volume_popup = Button(root, text='音量', bg="#8DFCDD", width=4, command=volume_popup_click)
    volume_popup.grid(row=3, rowspan=3, column=7, columnspan=2)
    createToolTip(volume_popup, '音量键控制')

    # 音量大小设置

    volume_increase = Button(root, text='+', bg="#8DFCDD", width=5,command=volume_increase_click)
    volume_increase.grid(row=3, rowspan=1, column=1, columnspan=3)
    volume_decrease = Button(root, text='-', bg="#8DFCDD", width=5, command=volume_decrease_click)
    volume_decrease.grid(row=5, rowspan=1, column=1, columnspan=3) #, pady=(10,30) sticky

    # 进度条
    # time_var = StringVar(value=0)
    jdt = Scale(root, from_=0, to=200, orient="horizontal", length=500,relief=GROOVE,
    sliderrelief=GROOVE, sliderlength=10, activebackground='black',bg="#33FF99",width=10,
        repeatinterval=100, command=progress_bar,resolution=1,show=0,troughcolor="#CCFCEF")# variable=time_var,, label="进度"
    jdt.grid(row=3,rowspan=3, column=4, columnspan=3)
    jdt['state'] = 'disable'
    createToolTip(jdt, '进度条控制')

    # 上下首
    next_one = Button(root, text='>', bg="#8DFCDD", command=next_one_music)  # 下一首
    next_one.grid(row=3, rowspan=3, column=3, columnspan=1, sticky=W)
    previous_one = Button(root, text='<', bg="#8DFCDD", command=previous_one_music)  # 上一首
    previous_one.grid(row=3, rowspan=3, column=1, columnspan=1, sticky=E)

    # 点击DD
    pause_resume = StringVar(root, value='ID')
    pause = Button(root, textvariable=pause_resume, width=5,command=click_play, bg="#8DFCDD")  # lambda:click_play(music_name)
    pause.grid(row=4, column=2, columnspan=1, rowspan=1)
    # pause.bind("<Return>",func=click_play_)
    # pause['state']='disable'  click_play_

    # 重新DD 停止DD
    contiplay = Button(root, text='重新D', command=rewind_play, bg="#8DFCDD")
    contiplay.grid(row=3, rowspan=2, column=0, columnspan=1)
    stoplay = Button(root, text='停止D', command=stop_play, bg="#8DFCDD")
    stoplay.grid(row=4, rowspan=2, column=0, columnspan=1)

    # DD显示
    musicName = StringVar(value='暂无播放')
    music_name = Label(root, textvariable=musicName, width=24,heigh=2, font=("楷书", 12),
    bd=3,bg="#8DFCDD", wraplength = 200,justify = 'center')
        # wraplength： 指定多少单位后开始换行justify:  指定多行的对齐方式
    music_name.grid(row=0, rowspan=2, column=7, columnspan=3,padx=(32,0),sticky=N+W+E)

    # DD时间
    musicTime = StringVar(value='')
    music_time = Label(root, textvariable=musicTime, width=22,heigh=1, font=("Helvetica", 12),
    bg="#8DFCDD",bd=2, )
    music_time.grid(row=1, rowspan=1, column=7, columnspan=2,padx=(32,0),sticky=S+W+E)
    musicTime.set('00:00')

    # song time
    musicLong = StringVar(value='00:00')
    music_long = Label(root, textvariable=musicLong, width=5,heigh=1, font=("Helvetica", 12),
    bg="#8DFCDD",bd=2, )
    music_long.grid(row=4, rowspan=1, column=7, columnspan=1, sticky=W)

    # songs listbox
    scrollbar2 = scr.Scrollbar(root, bd=1, width=14)
    scrollbar2.grid(row=2, column=8, sticky=E+N+S)
    songs = Listbox(root,selectmode="extended",bg="#85F0AC", font=("楷书", 14), 
    width=72, bd=3, yscrollcommand=scrollbar2.set)
    songs.grid(row=2, rowspan=1, column=4, columnspan=6, sticky=W+N+S)
    scrollbar2.config(command=songs.yview)

    # kong
    kong = Label(root, width=5,heigh=1, font=("Helvetica", 12),bd=0,image=bg1)  # 暂时隐藏在背景下
    kong.grid(row=0, rowspan=2, column=6, columnspan=1)  # 

    # 音量控制
    #注意，Scale的回调函数需要给定形参，当触发时会将Scale的值传给函数
    # , orient=HORIZONTAL # VERTICAL # , showvalue=0 , label='音量'
    s = Scale(root, from_=1, to=0,length=100, width=9, sliderlength=10,borderwidth=0.5,      # tickinterval=2, 
    resolution=0.02, command=control_volume, showvalu=0, troughcolor="#CCFCEF",bg="#33FF99",
    sliderrelief=FLAT, activebackground="black") 
    s.grid_forget()   # 隐藏音量
    s.bind("<MouseWheel>", control_volume_)

    hide_list = [s, volume_increase, volume_decrease]
    for i in hide_list:
        i.bind("<Leave>", volume_hide)

    pygame.mixer.init()
    pygame.mixer.music.set_volume(float(0.5))
    s.set(0.5)

    bg6_set()

    # 开启循环
    root.mainloop()