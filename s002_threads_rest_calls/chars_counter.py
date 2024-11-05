import json
import urllib.request
import time
from threading import Thread, Lock

finished_count = 0


def count_letters(url, frequency, lock):
    response = urllib.request.urlopen(url)
    txt = str(response.read())
    lock.acquire()
    for l in txt:
        letter = l.lower()
        if letter in frequency:
            frequency[letter] += 1
    global finished_count
    finished_count += 1
    lock.release()


def main():
    lock = Lock()
    frequency = {}
    for c in "abcdefghijklmnopqrstuvwxyz":
        frequency[c] = 0
    start = time.time()
    for i in range(1000, 1040):
        Thread(target=count_letters, args=(f"https://www.rfc-editor.org/rfc/rfc{i}.txt", frequency, lock)).start()
    while True:
        lock.acquire()
        if finished_count == 40:
            break
        lock.release()
    end = time.time()
    print(json.dumps(frequency, indent=4))
    print("Done, time taken", end - start)


main()
