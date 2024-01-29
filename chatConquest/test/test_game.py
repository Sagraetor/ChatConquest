import asyncio

import pygame

from chatConquest.common import team
from chatConquest.game import character
from chatConquest.game.display import display
from chatConquest.game.game_space import game_data


# Add custom event Handlers
def test_func(events):
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            char = character.create_character(14, team.TEAM3, "mage")
            char1 = character.create_character(11, team.TEAM2, "mage")
            char.move(11)
            char1.move(14)


display.add_pygame_event_handlers(test_func)
# Start game without TikTok
if __name__ == '__main__':
    with asyncio.Runner() as runner:
        game_data.connected = True
        loop = runner.get_loop()
        loop.run_until_complete(display.start())