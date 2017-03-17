import multiprocessing

from watch_dog import WatchDog

if __name__ == "__main__":
    multiprocessing.freeze_support()
    wd = WatchDog()
    wd.run()
