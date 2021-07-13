import random
import numpy
import control
import matplotlib.pyplot
import math
import cmath

# Poles = list(map(int, input("Enter pole(s) ").split()))
# Zeros = list(map(int, input("Enter zero(s) ").split()))
#Complex_Poles = complex(input('Enter the real part and imaginary part of complex poles '))
# Complex_Zeros = complex(input('Enter the real part and imaginary part of complex poles '))
#print(Complex_Poles.real, Complex_Poles.imag)


# class Root:
#
#     def __init__(self, real, imag=0.0):
#         self.real = real
#         self.imag = imag


class TF:

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

class Plot:

    def make_plot(self, g):
        control.bode_plot(g, dB=True)

    def mag(self, g):
        mag = control.bode_plot(g)
        return mag[0].tolist()

    def phase(self, g):
        phase = control.bode_plot(g)
        return phase[1].tolist()

    def omega(self, g):
        omega = control.bode_plot(g)
        return omega[2].tolist()

class Puzzle:
    def randGenFirstP(self):
        pole = random.uniform(0.001, 100)
        puzzle_first = TF(poles=pole)
        return puzzle_first.make_tf_first()

    def randGenFirstZ(self):
        zero = random.uniform(0.001, 100)
        puzzle_first = TF(zeros=zero)
        return puzzle_first.make_tf_first()

    def randGenSecondP(self):
        pole1 = random.uniform(0.001, 100)
        pole2 = random.uniform(0.001, 100)
        pole = [pole1, pole2]
        puzzle_first = TF(poles=pole)
        return puzzle_first.make_tf_second()

    def randGenSecondZ(self):
        zero1 = random.uniform(0.001, 100)
        zero2 = random.uniform(0.001, 100)
        zero = [zero1, zero2]
        puzzle_first = TF(zeros=zero)
        return puzzle_first.make_tf_second()

    def randGenCplxP(self):
        real = random.uniform(0.001, 100)
        imag = random.uniform(0.001, 100)
        puzzle_complex = TF(real=real, imag=imag)
        return puzzle_complex.make_tf_complex_pole()

    def randGenCplxZ(self):
        real = random.uniform(0.001, 100)
        imag = random.uniform(0.001, 100)
        puzzle_complex = TF(real=real, imag=imag)
        return puzzle_complex.make_tf_complex_zero()


class Score:

    def calculate_percentage(self, puzzlearray, userarray):  # adding up squared deviation of puzzle phase plot from zero. This forms a basis to get percentage difference
        puzzlesqaurearray = 0
        temsquaredifference = 0
        for o in puzzlearray:
            puzzlesqaurearray += o**2

        for idx, val in enumerate(userarray):
            temsquaredifference = (puzzlearray[idx]-val)**2
            temsquaredifference += temsquaredifference

        matchPercentage = 100*(puzzlesqaurearray - temsquaredifference)/puzzlesqaurearray
        mismatch = 100 - matchPercentage
        return [matchPercentage, mismatch]

class Level:
    pass


def main():
    pass




# G1 = control.tf([1],[5,1])
# G2 = control.tf([1],[100,1,2])
# mag1 = control.bode_plot(G1, dB=True)
# mag2 = control.bode_plot(G2, dB=True)
# # matplotlib.pyplot.show()
# print(len(mag1[0].tolist()))
# print(len(mag1[1].tolist()))
# print(len(mag1[2].tolist()))
#
# print(len(mag2[0].tolist()))
# print(len(mag2[1].tolist()))
# print(len(mag2[2].tolist()))


# G1_ss = control.tf2ss(G1)
# G2_ss = control.tf2ss(G2)
# # print(G1_ss.A)



