import pygame

from chatConquest.game import character
from chatConquest.common import team, constant, text_handler

from chatConquest.game.game_space import game_elements

screen = game_elements.init()

background = pygame.image.load(constant.BACKGROUND).convert()
background = pygame.transform.scale_by(background, 2)
how_to = text_handler.how_to_play()

running = True
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False
    if event.type == pygame.MOUSEBUTTONDOWN:
        char = character.create_character(14, team.TEAM3, "mage")
        char1 = character.create_character(11, team.TEAM2, "mage")
        char.move(11)
        char1.move(14)

pygame.display.update()
game_elements.update()

screen.blit(background, (0, 0))
screen.blit(how_to, (240, 360))

game_elements.draw(screen)

pygame.display.flip()