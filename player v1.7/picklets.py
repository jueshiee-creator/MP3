import pickle
import time

with open('songs/lyrics/曾经的你.txt', 'r',encoding='utf-8') as f:
    text = f.readlines()
    # print(text)

with open('sample.bat', 'wb') as f:
    try:
        pickle.dump(len(text), f)
        for i in text:
            pickle.dump(i, f)
    except:
        print('写入错误')


def load_bat():
    with open('sample.bat', 'rb') as f:
        n = pickle.load(f)  # n为数据个数
        print(n) 
        for i in range(n):   # 遍历后为内容
            x = pickle.load(f)
            print(x)

def load_txt():
    with open('songs/lyrics/曾经的你.txt', 'r',encoding='utf-8') as f:
        # for i in range(f):
        x = f.readlines()
        for i in x:
            print(i)


time1 = time.time()
load_bat()
time2 = time.time()

print(time2-time1)