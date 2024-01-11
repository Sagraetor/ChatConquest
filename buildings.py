import pygame

import animated_sprite
import constant
import team as tm
import text_handler


class _FlaggedBuilding(animated_sprite.TeamColorSprite):
    def __init__(self, image, width, height, max_hp, id_, position, team: tm.Team):
        animated_sprite.TeamColorSprite.__init__(self, image, width, height,
                                                 90, [[1, 14], [15, 15]], team)
        self.id_ = id_
        self.rect = pygame.rect.Rect(position[0], position[1], self.rect.width, self.rect.height)
        self.max_hp = max_hp
        self.hp = max_hp

        self.health_bar = animated_sprite.HealthBar(self, y_displacement=10)

    def send_unit(self, sprite_group, target, unit_type='knight'):
        import character
        if (self.id_, target) in constant.PATHS or (target, self.id_) in constant.PATHS:
            new_knight = character.create_character(self.id_, self.team, unit_type)
            sprite_group.add(new_knight)

    def capture(self, team):
        self.current_frame_loop = 0
        self.hp = self.max_hp
        self.team = team
        self.health_bar.show(3)

    def destroy(self):
        self.current_frame_loop = 1
        self.health_bar.update_health(0)

    def take_damage(self, attacker):
        if self.team == tm.NONE:
            self.capture(attacker.team)
            return

        if attacker.team != self.team:
            self.hp -= attacker.hp
            self.health_bar.show(3)
            if self.current_frame_loop == 1:
                self.capture(attacker.team)
            elif self.hp <= 0:
                self.destroy()


class _Towers(pygame.sprite.Group):
    companion_sprites = pygame.sprite.Group()

    class _Tower(_FlaggedBuilding):
        def __init__(self, id_, position, team: tm.Team):
            _FlaggedBuilding.__init__(self, constant.TOWER, 16, 32, 1000,
                                      id_, position, team,)

    def __init__(self):
        pygame.sprite.Group.__init__(self)

        for i in range(len(constant.TOWER_COORDINATES)):
            x, y = constant.TOWER_COORDINATES[i]
            tower = self._Tower(i + 4, (x, y), tm.NONE)
            self.add(tower)
            self.companion_sprites.add(tower.health_bar)

    def draw(self, surface, bgsurf=None, special_flags=0):
        super().draw(surface, bgsurf, special_flags)

        sprites = self.sprites()

        for spr in sprites:
            img, pos = text_handler.label_from_id(spr)
            surface.blit(img, pos)

        self.companion_sprites.draw(surface, bgsurf, special_flags)

    def update(self, *args, **kwargs):
        super().update()
        self.companion_sprites.update()

    def find(self, id_):
        for spr in self.sprites():
            if spr.id_ == id_:
                return spr


class _Castles(pygame.sprite.Group):
    companion_sprites = pygame.sprite.Group()

    class _Castle(_FlaggedBuilding):
        def __init__(self, id_, position, team: tm.Team):
            _FlaggedBuilding.__init__(self, constant.CASTLE, 48, 44, 5000,
                                      id_, position, team)

    def __init__(self):
        pygame.sprite.Group.__init__(self)

        for i in range(len(constant.CASTLE_COORDINATES)):
            x, y = constant.CASTLE_COORDINATES[i]
            castle = self._Castle(i + 1, (x, y), tm.TEAMS[i])
            tm.TEAMS[i].castle = castle
            self.add(castle)
            self.companion_sprites.add(castle.health_bar)

    def draw(self, surface, bgsurf=None, special_flags=0):
        super().draw(surface, bgsurf, special_flags)

        sprites = self.sprites()

        for spr in sprites:
            img, pos = text_handler.label_from_id(spr, 25)
            surface.blit(img, pos)
        self.companion_sprites.draw(surface, bgsurf, special_flags)

    def update(self, *args, **kwargs):
        super().update()
        self.companion_sprites.update()

    def find(self, id_):
        for spr in self.sprites():
            if spr.id_ == id_:
                return spr


towers = _Towers()
castles = _Castles()
