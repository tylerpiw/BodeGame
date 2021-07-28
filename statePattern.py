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