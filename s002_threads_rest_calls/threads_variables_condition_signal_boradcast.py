import time
from threading import Thread, Condition


class Bank:
    money = 100
    vc = Condition()

    def deposit(self):
        for i in range(10000):
            self.vc.acquire()
            self.money += 10
            self.vc.notify()
            self.vc.release()

        print("Stingy Done")

    def withdraw(self):
        for i in range(5000):
            self.vc.acquire()
            while self.money < 20:
                self.vc.wait()
            self.money -= 20
            self.vc.release()
        print("Spendy Done")


acc = Bank()
Thread(target=acc.deposit, args=()).start()
Thread(target=acc.withdraw, args=()).start()

time.sleep(5)
print("Money in the end", acc.money)
