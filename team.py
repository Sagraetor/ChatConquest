import pygame

class Team(pygame.sprite.Group):
    castle = None

    def __init__(self, color):
        pygame.sprite.Group.__init__(self)
        self.team_color = color


TEAM1 = Team((150, 195, 89))
TEAM2 = Team((255, 182, 193))
TEAM3 = Team((137, 207, 240))
NONE = Team((192, 192, 192))
TEAMS = [TEAM1, TEAM2, TEAM3, NONE]