import os
import time
import chardet


def songplay_clock(file):
    global colums
    if colums > 0:
        with open(file, 'r', encoding='utf-8') as f:
            songlines = f.readlines()
            os.system('cls')
            colums -= 1
            print('{:@^{}}'.format(m_name, colums))
            print('')
            # for i in [c.strip() for c in songlines]:
            #     i = '{:@^72}'.format(i)
            #     print(i)
    else:
        return

def songsplay(file, colums=72):

    with open(file, 'r', encoding='utf-8') as f:
        songlines = f.readlines()
        conum = colums - len(bytes(m_name.encode('gbk')))+len(m_name)
        print(conum)
        print('{:+^{}}\n'.format(m_name, conum))

    for i in songlines[:]:
        conum = colums - len(i.encode('GBK'))+len(i)
        print('{:+^{}}'.format(i, conum))
            # return

def song_display(m_name, columns=72):
    """歌词显示"""

    songs.delete(0, END)

    file = 'songs/{}.txt'.format(m_name)
    codedFormat = ['utf-8', 'gbk']
    codedIndex = 0
    while True:
        try:
            with open(file, 'r', encoding=codedFormat[codedIndex]) as f:
                songlines = f.readlines()
                songs.insert(0, '                 {}'.format(m_name))
                songs.insert(END, '')
                for i in [c.strip() for c in songlines]:
                    i = '                 {}'.format(i)
                    songs.insert(END, i)
            print('歌词加载成功')
            break
        except:
            codedIndex += 1


if __name__ == "__main__":

    m_name = '江湖流'
    file = 'songs/{}.txt'.format(m_name)

    songsplay(file)

    # colums = 50
    # while True:
    #     time.sleep(1)
    #     songplay(file)
    #     if colums == 0:
    #         break


