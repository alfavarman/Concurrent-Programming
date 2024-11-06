import os
import time
from os import times
from os.path import isdir, join
from threading import Lock, Thread



mtx = Lock()
matches = []


def file_search(root, filename):
    #print("Searching in:", root)
    threads = []
    for file in os.listdir(root):
        full_path = join(root, file)
        if filename in file:
            mtx.acquire()
            matches.append(full_path)
            mtx.release()
        if isdir(full_path):
            t = Thread(target=file_search, args=([full_path, filename]))
            t.start()
            threads.append(t)
    [t.join() for t in threads]

def main():
    start = time.time()
    t = Thread(target=file_search, args=(["/home/charles/", "README.md"]))
    t.start()
    t.join()
    stop = time.time()
    for m in matches:
        print("Matched:", m)
    print(f"searching took {start-stop}")
main()
