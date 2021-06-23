import random
import control
import matplotlib.pyplot
import math
import cmath
# pole = random.random()
# zero = random.random()

# Poles = list(map(int, input("Enter pole(s) ").split()))
# Zeros = list(map(int, input("Enter zero(s) ").split()))
Complex_Poles = complex(input('Enter the real part and imaginary part of complex poles '))
# Complex_Zeros = complex(input('Enter the real part and imaginary part of complex poles '))
print(Complex_Poles.real, Complex_Poles.imag)


class Root(object):

    def __init__(self, real, imag=0.0):
        self.real = real
        self.imag = imag








class TF(object):

    def __init__(self, poles=None, zeros=None, real=None, imag=None):
        self.pole = poles
        self.zero = zeros
        self.num = []
        self.deno = []
        self.real = real
        self.imag= imag

    def make_tf_first(self):
        if self.zero is None and self.pole is not None:
            self.num = [1]
            self.deno = [1, -self.pole[0]]
            return control.tf(self.num, self.deno)
        else:
            self.num = [1, -self.zero[0]]
            self.deno = [1]
            return control.tf(self.num, self.deno)

    def make_tf_second(self):
        if self.zero is None and self.pole is not None:
            self.num = [1]
            self.deno = [1, -(self.pole[0]+self.pole[1]), self.pole[0]*self.pole[1]]
            return control.tf(self.num,self.deno)
        else:
            self.deno = [1]
            self.num = [1, -(self.zero[0]+self.zero[1]), self.zero[0]*self.zero[1]]
            return control.tf(self.num, self.deno)

    def make_tf_complex_pole(self):
        self.num = [1]
        self.deno = [self.real**2, 2*self.real*self.imag, -self.imag**2]
        return control.tf(self.num, self.deno)

    def make_tf_complex_zero(self):
        self.num = [self.real**2, 2*self.real*self.imag, -self.imag**2]
        self.deno = [1]
        return control.tf(self.num, self.deno)

class Plot(object):

    def make_plot(self, g):
        control.bode_plot(g, dB=True)

class Puzzle(object):
    pass

class Score(object):

    def puzzle_phase_sum(self):     #  adding up squared deviation of puzzle phase plot from zero. This forms a basis to get percentage difference
        pass

    def user_puzzle_difference(self):
        pass

    def calculate_percentage(self):
        pass


def main():
    pass



#
# G1 = control.tf([1],[5,1])
# G2 = control.tf([1],[100,1])
# mag = control.bode_plot(G1, dB=True)
# control.bode_plot(G2, dB=True)
# matplotlib.pyplot.show()
# print(mag)
# G1_ss = control.tf2ss(G1)
# G2_ss = control.tf2ss(G2)
# # print(G1_ss.A)



