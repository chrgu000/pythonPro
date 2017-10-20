# -*- coding: utf-8 -*
from abc import ABCMeta,abstractmethod,abstractproperty
'''
abc.ABCMeta :生成抽象基础类的元类，由它生成的类可直接被继承
'''
class Recommend:
    __metaclass__ = ABCMeta

    @abstractmethod
    def speak(self):
        print("person speak")

    @abstractmethod
    def run(self):
        print("person run")

class male(person):

    def speak(self):
        print("hello")

    def run(self):
        print("run")

if __name__ == '__main__':
    a = male()
    print(a.run())
    # print(a.speak())
    pass