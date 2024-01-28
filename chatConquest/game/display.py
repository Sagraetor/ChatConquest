import pygame
import pygame_textinput

import asyncio

from chatConquest.game import character
from chatConquest.common import team, constant, text_handler

from chatConquest.game.game_space import game_elements, game_data

background = pygame.image.load(constant.BACKGROUND).convert()
background = pygame.transform.scale_by(background, 2)

text_how_to = text_handler.draw_how_to()
text_battle_log = text_handler.draw_battle_log()
text_menu = text_handler.draw_menu()
id_input = text_handler.id_input


class Display:
    def __init__(self):
        self.screen = game_elements.init()
        self._running = True
        self.init_tiktok = None

    def set_tiktok_initialiser(self, func):
        self.init_tiktok = func

    async def start(self):
        pygame.display.set_caption("Demo")

        self._running = True
        await self.__screen_loop()

    def stop(self):
        self._running = False
        pygame.quit()

    async def __screen_loop(self):
        while self._running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.stop()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    char = character.create_character(14, team.TEAM3, "mage")
                    char1 = character.create_character(11, team.TEAM2, "mage")
                    char.move(11)
                    char1.move(14)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if not game_data.connected:
                            self.init_tiktok(id_input.value)

            if game_data.connected:
                pygame.display.update()
                game_elements.update()

                self.screen.blit(background, (0, 0))
                self.screen.blit(text_how_to, (240, 360))
                self.screen.blit(text_battle_log, (240, 540))

                game_elements.draw(self.screen)

            else:
                id_input.update(events)

                self.screen.blit(background, (0, 0))
                menu = pygame.Surface((440, 680)).convert_alpha()
                menu.fill((0, 0, 0, 200))
                menu.blit(text_menu, (0,0))
                menu.blit(id_input.surface, (15, 55))
                self.screen.blit(menu, (20, 20))

            pygame.display.flip()
            await asyncio.sleep(0.001)


display = Display()