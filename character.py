import math
import pygame

import constant
import team
import animated_sprite

from projectiles import launch_mage_projectile
from game_space import game_elements


class Character(animated_sprite.TeamColorSprite):
    target = None
    target_building_id = None
    movement_angle = None
    on_kill_events = []
    moving = False
    projectile = None
    cooldown = False
    launch_projectile = None

    def __init__(self, image, width, height, frame_ranges, attack_frame, speed, damage, hp, reach, attack_delay,
                 current_building_id, team_: team.Team):
        animated_sprite.TeamColorSprite.__init__(self, image, width, height,
                                                 90, frame_ranges, team_)
        self.attack_frame = attack_frame
        self.speed = speed
        self.damage = damage
        self.hp = hp
        self.max_hp = hp
        self.reach = reach
        self.attack_delay = attack_delay
        self.current_building_id = current_building_id
        self.team = team_
        self.health_bar = animated_sprite.HealthBar(self, y_displacement=-4)
        game_elements.show(self.health_bar)

        self.position = self.__get_checkpoint(current_building_id)
        self.destination = self.position
        self.rect = pygame.Rect(self.position[0], self.position[1], width, height)

    def move(self, destination_id):
        if ((self.current_building_id, destination_id) not in constant.PATHS and
                (destination_id, self.current_building_id) not in constant.PATHS):
            return
        if self.moving:
            return

        self.target_building_id = destination_id
        self.destination = self.__get_checkpoint(destination_id)

        self.movement_angle = math.atan2(self.destination[0] - self.position[0], self.destination[1] - self.position[1])
        self.moving = True

        game_elements.show(self)

    def take_damage(self, damage):
        self.hp -= damage
        self.health_bar.show(3)
        if self.hp <= 0:
            self.kill()

    def add_killed_listener(self, func):
        self.on_kill_events.append(func)

    def update(self, *args, **kwargs):
        if self.target:
            self._attack()
        else:
            if self.destination != self.position:
                if not self._find_target():
                    dx = (self.speed * math.sin(self.movement_angle))
                    dy = (self.speed * math.cos(self.movement_angle))
                    self.position = (self.position[0] + dx, self.position[1] + dy)

                    self.rect.x = self.position[0]
                    self.rect.y = self.position[1]

        animated_sprite.TeamColorSprite.update(self, *args, **kwargs)

        if int(self.rect.x) == int(self.destination[0]):
            target_building = game_elements.get_building_from_id(self.target_building_id)
            self.moving = False
            if target_building.team == self.team:
                self._enter_building()
            elif target_building.team == team.NONE:
                self._enter_building()
                target_building.take_damage(self)
            else:
                self.kill()
                target_building.take_damage(self)

    def kill(self):
        self.health_bar.kill()
        for function in self.on_kill_events:
            if function:
                function()
        pygame.sprite.Sprite.kill(self)

    def __get_checkpoint(self, _id):
        building = game_elements.get_building_from_id(_id)
        building_rect = building.get_rect()
        self_rect = self.get_rect()
        self_rect.centerx = building_rect.centerx
        self_rect.bottom = building_rect.bottom
        return self_rect.x, self_rect.y

    def _enter_building(self):
        self.position = self.destination
        self.current_building_id = self.target_building_id
        self.movement_angle = None
        game_elements.hide(self)

    def _attack(self):
        if self.current_frame == self.attack_frame:
            if self.cooldown:
                return

            if self.launch_projectile:
                self.launch_projectile(self)
            else:
                self.target.take_damage(self.damage)

            self.cooldown = True

        elif self.current_frame == self.frame_ranges[self.current_frame_loop][1]:
            self.pause_animation(self.attack_delay)
            self.current_frame = self.frame_ranges[self.current_frame_loop][0]

            self.cooldown = False

    def _drop_target(self):
        self.target = None
        self.last_update = pygame.time.get_ticks()
        self.current_frame_loop = 0

    def _find_target(self) -> bool:
        if not self.groups():
            return False

        for spr in self.groups()[0].sprites():

            if not issubclass(type(spr), Character):
                continue

            if spr.team == self.team:
                continue

            dx = self.rect.x - spr.rect.x
            dy = self.rect.y - spr.rect.y
            if math.sqrt(dx ** 2 + dy ** 2) <= self.reach:
                self.current_frame_loop = 1
                self.target = spr
                spr.add_killed_listener(self._drop_target)
                return True

        return False

    def _getimage(self, frame):
        animated_sprite.TeamColorSprite._getimage(self, frame)

        if self.movement_angle is not None:
            if math.sin(self.movement_angle) < 0:
                self.image = pygame.transform.flip(self.image, True, False)
                self.image.set_colorkey((0, 0, 0))


def create_character(spawn, team_, character_type="knight", on_kill_event=None) -> Character:
    match character_type:
        case "knight":
            new_character = Character(constant.KNIGHT, 18, 17, [[2, 9], [10, 18]], 15,
                                      1, 10, 100, 20, 1,
                                      spawn, team_)
            if on_kill_event:
                new_character.add_killed_listener(on_kill_event)
            return new_character
        case "archer":
            new_character = Character("none", 10, 10, [2, 9],15,
                                      1.25, 10, 50, 60, 1,
                                      spawn, team_, 3)
            if on_kill_event:
                new_character.on_kill = on_kill_event
            return new_character
        case "mage":
            new_character = Character(constant.MAGE, 16, 17, [[2, 9], [10, 20]], 15,
                                      1, 25, 50, 60, 2,
                                      spawn, team_)
            new_character.launch_projectile = launch_mage_projectile
            if on_kill_event:
                new_character.on_kill = on_kill_event
            return new_character
