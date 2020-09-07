from threading import Thread, Lock
import pygame
import time


# pygame.mixer.init()
# pygame.mixer.music.load('SealWu、Egco蔡唯真 - 野草.mp3')
# pygame.mixer.music.play(1)
# time.sleep(5)
class Music(object):

    def __init__(self):
        pygame.mixer.init()
        self._lock = Lock()
        self._lock.acquire()

    def stop_music(self):
        try:
            pygame.mixer.music.stop()
        finally:
            self._lock.release()

    def play_music(self):
        self.stop_music()
        self._lock.acquire()
        
        pygame.mixer.music.load('ogceshi.ogg')
        pygame.mixer.music.play(1)
        time.sleep(30)

class MusicThread(Thread):

    def __init__(self, music):
        super().__init__()
        self._music = music

    def run(self):
        self._music.play_music()

def main():
    music = Music()
    threads = []
    for _ in range(2):
        time.sleep(2)
        t = MusicThread(music)
        t.start()
        threads.append(t)
    for i in threads:
        i.join()
        print('已切歌')

if __name__ == "__main__":

    main()