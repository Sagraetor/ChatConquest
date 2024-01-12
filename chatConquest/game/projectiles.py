import pygame
from chatConquest.common import constant
import math
import random

from chatConquest.game.game_space import game_elements


class _Projectile(pygame.sprite.Sprite):
    def __init__(self, image: pygame.surface, rect: pygame.Rect, angle, speed, parent, color, trail_max_radius):
        pygame.sprite.Sprite.__init__(self)
        self.rect = rect
        self.position = [rect.x, rect.y]

        self.image = pygame.transform.scale_by(image, constant.SCALE)
        self.image.set_colorkey((0, 0, 0))

        self.angle = angle
        self.speed = speed
        self.parent = parent
        self.last_trail = pygame.time.get_ticks()

        self.trail = Trail(self, game_elements.screen, color, trail_max_radius)

        self.parent.target.add_killed_listener(self.kill)
        game_elements.add_draw(self.trail.emit, True)

    def update(self, *args, **kwargs):
        self.trail.add_particle()

        dx = (self.speed * math.sin(self.angle))
        dy = (self.speed * math.cos(self.angle))
        self.position = (self.position[0] + dx, self.position[1] + dy)

        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

        if self.parent.target:
            if pygame.sprite.collide_mask(self, self.parent.target):
                self.parent.target.take_damage(self.parent.damage)
                self.kill()


class Trail:
    def __init__(self, parent: _Projectile, screen, color, max_radius):
        self.particles = []
        self.parent = parent
        self.screen = screen
        self.color = color
        self.max_radius = max_radius
        self.delay = 5

    def emit(self):
        if self.particles:
            for particle in self.particles:
                pygame.draw.circle(self.screen, self.color, particle[0], particle[1]/self.delay)
                particle[1] -= 1
                if particle[1] <= 0:
                    self.particles.remove(particle)
                    if len(self.particles) == 0:
                        game_elements.remove_draw(self.emit)
                    continue

    def add_particle(self):
        particle = [None, None]
        x = random.uniform(self.parent.rect.left, self.parent.rect.left + self.parent.image.get_rect().w)
        y = random.uniform(self.parent.rect.top, self.parent.rect.top + self.parent.image.get_rect().h)
        particle[0] = (x, y)
        particle[1] = random.uniform(0, self.max_radius) * self.delay
        self.particles.append(particle)


def launch_mage_projectile(parent):
    projectile_image = pygame.Surface((4, 4)).convert_alpha()
    projectile_image.blit(pygame.image.load(constant.MAGE).convert_alpha(), (0, 0), (320, 0, 4, 4))

    new_rect = parent.get_rect()
    if math.sin(parent.movement_angle) < 0:
        new_rect.x = new_rect.right - 20
    else:
        new_rect.x = new_rect.x + 12

    new_rect.y = new_rect.y + 20
    new_rect.w = 4
    new_rect.h = 4
    projectile = _Projectile(projectile_image, new_rect, parent.movement_angle, 2.5, parent, (135, 82, 156), 5)
    game_elements.show(projectile)