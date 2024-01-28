import pygame
import pygame_textinput
from chatConquest.common import constant

pygame.font.init()


def add_outline(image: pygame.Surface, thickness: int, color: tuple, color_key: tuple = (255, 0, 255)) -> pygame.Surface:
    mask = pygame.mask.from_surface(image)
    mask_surf = mask.to_surface(setcolor=color)
    mask_surf.set_colorkey((0, 0, 0))

    new_img = pygame.Surface((image.get_width() + 2, image.get_height() + 2))
    new_img.fill(color_key)
    new_img.set_colorkey(color_key)

    for i in -thickness, thickness:
        new_img.blit(mask_surf, (i + thickness, thickness))
        new_img.blit(mask_surf, (thickness, i + thickness))
    new_img.blit(image, (thickness, thickness))

    return new_img



def label_from_id(sprite, font_size = 16):
    font = pygame.font.Font(constant.FONT_BOLD, font_size)
    number = font.render(str(int(sprite.id_)), False, sprite.team.team_color)
    number = add_outline(number, 2, (50, 50, 50))

    width = number.get_width()
    height = number.get_height()

    if int(sprite.id_) > 9:
        width = 26

    image = pygame.Surface((width, height)).convert_alpha()
    sprite_rect = sprite.get_rect()

    pos = (sprite_rect.centerx - width/2, sprite_rect.y - height)

    if pos[1] < 0:
        pos = (pos[0] - width, 0)

    image.blit(number, (0, 0))

    image.set_colorkey((0, 0, 0))
    return image, pos

def draw_menu():
    font = pygame.font.Font(constant.FONT, 16)
    lines = ["Type room ID or steamer username:",
             "-----------------------------------------------------------",
             "",
             "-----------------------------------------------------------",
             "How to play:",
             "1. Type (1 - 3) to choose team and spawn in ",
             'that castle',
             "",
             "2. Type (a/b/c) to change class",
             "      a - knight",
             "      b - mage",
             "      c - archer",
             "",
             "3. Type any number to travel to that building",
             "",
             "4. Travelling to a captured building will make",
             "you rest in that building",
             "",
             "5. Travelling to an uncaptured building will make",
             "you capture the building",
             "",
             "6. Soldiers from different factions will fight",
             "automatically",
             "",
             "7. If you are killed, you will respawn in the",
             "last captured building you entered",
             ]
    image = pygame.Surface((440, 680)).convert_alpha()

    for i in range(len(lines)):
        line = font.render(lines[i], False, (180, 180, 180))
        image.blit(line, (15, 15 + 20 * i))

    image.set_colorkey((0, 0, 0))
    return image

def draw_how_to():
    font = pygame.font.Font(constant.FONT, 16)
    lines = ["1. Type (1 - 3) to choose",
             'team and spawn in that',
             'castle',
             "2. Type (a/b/c) to",
             "change class",
             "3. Type any number to",
             "travel to that building",
             "",
             "Battle log:"]
    image = pygame.Surface((240, 360)).convert_alpha()

    for i in range(len(lines)):
        line = font.render(lines[i], False, (50, 50, 50))
        image.blit(line, (15, 15 + 20 * i))

    image.set_colorkey((0, 0, 0))
    return image


def draw_battle_log():
    font = pygame.font.Font(constant.FONT, 16)
    lines = ["Sagrator HAS BEEN SLAIN",
             'team and spawn in that',
             'castle',
             "2. Type (a/b/c) to",
             "change class",
             "3. Type any number to",
             "travel to that building",
             "Battle log:"]
    image = pygame.Surface((240, 360)).convert_alpha()

    for i in range(len(lines)):
        line = font.render(lines[i], False, (50, 50, 50))
        image.blit(line, (15, 15 + 20 * i))

    image.set_colorkey((0, 0, 0))
    return image


id_input = pygame_textinput.TextInputVisualizer(font_object=pygame.font.Font(constant.FONT, 16), font_color=(200,200,200), cursor_color=((180, 180, 180)))