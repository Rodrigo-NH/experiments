# SPDX-License-Identifier: BSD-2-Clause

import threading
import time
import random
import atexit

cc = list()
ct1 = 0
ct2 = 0
ct3 = 0
ct4 = 0
locklist = False
lock = threading.RLock()

def main():
    v0 = 0
    v1 = 0
    cc.append(v0)
    cc.append(v1)

    for x in range(0, 1000):
        t = threading.Thread(target=_cat, )
        t.start()

def _cat():
    lock.acquire()
    global ct1
    global ct2
    global ct3
    global ct4
    global cc
    global locklist
    global lockcontrol

    randn = random.random() / 100
    v0 = cc[0]
    v1 = cc[1]
    v0 = 1 - v0
    v1 = 1 - v1
    cc[0] = v0
    time.sleep(randn)
    cc[1] = v1
    if cc == [0, 0]:
        ct1 += 1
    if cc == [1, 0]:
        ct2 += 1
    if cc == [0, 1]:
        ct3 += 1
    if cc == [1, 1]:
        ct4 += 1

    lock.release()

@atexit.register
def _results():
    print ("[0, 0] = " + str(ct1) + " | " + "[1, 0] = " + str(ct2) + " | " + "[0, 1] = " + str(ct3) + " | " + "[1, 1] = " + str(ct4))
    print("Total processed: " + str(ct1+ct2+ct3+ct4))

if __name__ == "__main__":
	main()
