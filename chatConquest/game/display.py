import pygame
import asyncio

from chatConquest.game import character
from chatConquest.common import team, constant, text_handler

from chatConquest.game.game_space import game_elements

background = pygame.image.load(constant.BACKGROUND).convert()
background = pygame.transform.scale_by(background, 2)
how_to = text_handler.how_to_play()
battle_log = text_handler.draw_battle_log()


class Display:
    def __init__(self):
        self.screen = game_elements.init()
        self._running = True

    async def start(self):
        pygame.display.set_caption("Demo")

        self._running = True
        await self.__screen_loop()

    def stop(self):
        self._running = False
        pygame.quit()

    async def __screen_loop(self):
        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:

                    char = character.create_character(14, team.TEAM3, "mage")
                    char1 = character.create_character(11, team.TEAM2, "mage")
                    char.move(11)
                    char1.move(14)

            pygame.display.update()
            game_elements.update()

            self.screen.blit(background, (0, 0))
            self.screen.blit(how_to, (240, 360))
            self.screen.blit(battle_log, (240, 540))

            game_elements.draw(self.screen)

            pygame.display.flip()
            await asyncio.sleep(0.001)

display = Display()