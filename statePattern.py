import random

import matplotlib.pyplot
import numpy
import control
import matplotlib.pyplot as plt
import math
import cmath
from numpy import logspace
from itertools import repeat


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
            self.deno = [1, -(self.pole[0] + self.pole[1]), self.pole[0] * self.pole[1]]
            return control.tf(self.num, self.deno)
        else:
            self.deno = [1]
            self.num = [1, -(self.zero[0] + self.zero[1]), self.zero[0] * self.zero[1]]
            return control.tf(self.num, self.deno)

    def make_tf_complex_pole(self):
        self.num = [1]
        self.deno = [self.real ** 2, 2 * self.real * self.imag, -self.imag ** 2]
        return control.tf(self.num, self.deno)

    def make_tf_complex_zero(self):
        self.num = [self.real ** 2, 2 * self.real * self.imag, -self.imag ** 2]
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


def calculate_percentage(self, puzzlearray, userarray):
    puzzlesqaurearray = 0
    temsquaredifference = 0
    for o in puzzlearray:
        puzzlesqaurearray += math.pow(o, 2)

    for idx, val in enumerate(userarray):
        temsquaredifference += math.pow((puzzlearray[idx] - val), 2)

    matchPercentage = 100 * (puzzlesqaurearray - temsquaredifference) / puzzlesqaurearray
    mismatch = 100 - matchPercentage
    return [matchPercentage, mismatch]


class GameLevel(object):
    """
    The GameLevel class stores the state variable responsible for changing the level.
    The 'allowed' variable is a list containing the allowable levels that the game can advance to.
    """
    name = "level"
    allowed = []

    def switch(self, level):
        """ Switch to new level. """
        if level.name in self.allowed:
            print("Current level:", self, " => advancing to new level:", level.name)
            self.__class__ = level
        else:
            print("Current level:", self, " => advancing to", level.name, "not possible.")

    def __str__(self):
        return self.name


class LevelOne(GameLevel):
    """ The LevelOne class contains the functionality for Level 1. The game can only advance to Level 2 from here."""

    # this is the code for forming the transfer function and bode plot
    puzzle = Puzzle()
    tf = puzzle.randGenFirstP()
    matplotlib.pyplot.figure()
    om = logspace(-3, 3, 100)
    bodePlot = control.bode(tf, om)
    matplotlib.pyplot.show()

    name = "Level One"
    allowed = ["Level Two"]


class LevelTwo(GameLevel):
    """ The LevelTwo class contains the functionality for Level 2. The game can only advance to Level 3 from here."""

    name = "Level Two"
    allowed = ["Level Three"]


class LevelThree(GameLevel):
    """ The LevelThree class contains the functionality for Level 3. This is the final level of the game (?)."""

    name = "Level Three"
    allowed = []


class Game(object):
    """ The Game class represents the game, in which the user starts in Level 1."""

    # The game defaults to Level 1.
    def __init__(self):
        self.level = LevelOne()

    # Changes the level.
    def change(self, level):
        self.level.switch(level)

    # Returns the current level.
    def getLevel(self):
        return self.level


if __name__ == "__main__":
    game = Game()  # creates a new game object
    game.change(LevelTwo)  # advances to level 2
    game.change(LevelThree)  # advances to level 3
    game.change(LevelTwo)  # error, since can't go from level 3 to level 2

"""
1. How to incorporate the different difficult level puzzles into each level.
2. Need to decide which puzzles go in each level.
3. More than 3 levels?
4. Can do levels or can do random difficulty option
"""