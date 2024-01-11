import pygame
import constant


class _GameElements(pygame.sprite.Group):
    towers = None
    castles = None
    visible = pygame.sprite.Group()
    invisible = pygame.sprite.Group()
    draw_behind = []
    draw_in_front = []

    def __init__(self,):
        pygame.sprite.Group.__init__(self)
        pygame.init()
        self.screen = pygame.display.set_mode(constant.SCREEN_RATIO)

    def init(self):
        from buildings import towers
        from buildings import castles
        self.towers = towers
        self.castles = castles
        return self.screen

    def get_building_from_id(self, id_):
        if id_ <= 3:
            return self.castles.find(id_)
        else:
            return self.towers.find(id_)

    def add_draw(self, func, behind=False):
        if behind:
            self.draw_behind.append(func)
        else:
            self.draw_in_front.append(func)

    def remove_draw(self, func):
        if func in self.draw_behind:
            self.draw_behind.remove(func)
        elif func in self.draw_in_front:
            self.draw_in_front.remove(func)

    def hide(self, sprite):
        self.visible.remove(sprite)
        self.invisible.add(sprite)

    def show(self, sprite):
        self.invisible.remove(sprite)
        self.visible.add(sprite)

    def update(self, *args, **kwargs):
        self.towers.update(args, kwargs=kwargs)
        self.castles.update(args, kwargs=kwargs)
        self.visible.update(args, kwargs=kwargs)

    def draw(self, surface, bgsurf=None, special_flags=0):
        self.towers.draw(surface, bgsurf, special_flags)
        self.castles.draw(surface, bgsurf, special_flags)
        if self.draw_behind:
            for func in self.draw_behind:
                func()
        self.visible.draw(surface, bgsurf, special_flags)
        if self.draw_in_front:
            for func in self.draw_in_front:
                func()


game_elements = _GameElements()
