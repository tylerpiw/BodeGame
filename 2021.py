import random
import numpy
import control
import matplotlib.pyplot as plt
import math
import cmath
from numpy import logspace
from itertools import repeat
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
        self.imag = imag

    def make_tf_first(self):
        if self.zero is None and self.pole is not None:
            self.num = [1]
            self.deno = [1, -self.pole]
            return control.tf(self.num, self.deno)
        else:
            self.num = [1, -self.zero]
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


class Puzzle(TF):
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


# class Plot(Puzzle, TF):
#
#     def make_plot(self, g, om):
#         control.bode(g, om, dB=True)
#
#     def mag(self, g):
#         mag = control.bode(g)
#         return mag[0].tolist()
#
#     def phase(self, g):
#         phase = control.bode(g)
#         return phase[1].tolist()
#
#     def omega(self, g):
#         omega = control.bode(g)
#         return omega[2].tolist()


class Score:

    # def data_process(self, puzzlearray, userarray):
    #     first_data = puzzlearray[1][0]  # find the first data
    #     last_data = puzzlearray[1][-1]  # find the last data of x axis in puzzle
    #
    #     filtered_user_x = [x for x in userarray[1] if first_data <= x <= last_data]  # filter the user array,
    #     # that present in the range of the puzzle
    #     # print(len(filtered_user_x))
    #     last_data_user = filtered_user_x[-1]
    #     first_data_user = filtered_user_x[0]  # find the last data of the user that's in the range of the puzzle
    #     last_index_user = userarray[1].index(last_data_user)
    #     first_index_user = userarray[1].index(first_data_user)  # find the index of the first and last data
    #     filtered_user_y = userarray[0][first_index_user:last_index_user+1]  # filtered y data of the user array
    #     # with last data index
    #
    #     rebuild_user = [0]*first_index_user + filtered_user_y + [0]*((len(puzzlearray[0])-1)-last_index_user)
    #     print(rebuild_user)
    #     return rebuild_user

    def calculate_percentage(self, puzzlearray, userarray):
        puzzlesqaurearray = 0
        temsquaredifference = 0
        for o in puzzlearray:
            puzzlesqaurearray += math.pow(o, 2)

        for idx, val in enumerate(userarray):
            temsquaredifference += math.pow((puzzlearray[idx]-val), 2)

        matchPercentage = 100*(puzzlesqaurearray - temsquaredifference)/puzzlesqaurearray
        mismatch = 100 - matchPercentage
        return [matchPercentage, mismatch]

# problem : the two array is not on the same x-axis,
# so that if the shape of the plot is similar, the percentage is always high
# only show the puzzle range, compare with the puzzle range

class Level:
    pass


def main():
    # generate puzzle
    # test level
    puzzle1 = Puzzle()
    G1 = puzzle1.randGenFirstP()

    # user input
    user_pole = random.uniform(0.01, 100)  # simulate user input
    user = TF(poles=user_pole)
    G2 = user.make_tf_first()
    # show plot
    plt.figure()
    om = logspace(-3, 3, 100)  ## this set the puzzle and user in same range!!!!
    puzzle_phase = control.bode(G1, om, grid=True)
    user_phase = control.bode(G2, om, grid=True)
    plt.subplot(211)
    plt.legend(['p', 'u'])
    plt.title('Bode Plot')
    plt.show()
    # score
    percentage = Score()
    pre = percentage.calculate_percentage(puzzle_phase[1].tolist(), user_phase[1].tolist())
    print(pre)


main()



# G1 = control.tf([1],[5,1])
# G2 = control.tf([1],[100,1,2])
# mag1 = control.bode_plot(G1, dB=True)
# mag2 = control.bode_plot(G2, dB=True)
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



