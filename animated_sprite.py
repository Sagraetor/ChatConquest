import pygame
import constant


class HealthBar(pygame.sprite.Sprite):
    BORDER = 1

    def __init__(self, sprite, height=8, y_displacement=0):
        pygame.sprite.Sprite.__init__(self)
        self._parent = sprite
        self.y_displacement = y_displacement
        parent_rect = self._parent.get_rect()

        width = parent_rect.w

        self.rect = pygame.Rect(0, parent_rect.y + y_displacement, width, height)
        self.rect.centerx = parent_rect.centerx
        self.last_update = pygame.time.get_ticks()

        self.update_health(0)

    def update(self, *args, **kwargs):
        self.rect.centerx = self._parent.get_rect().centerx
        self.rect.y = self._parent.get_rect().y + self.y_displacement
        if self.image.get_alpha() != 0:
            current_time = pygame.time.get_ticks()
            if current_time > self.last_update:
                self.image.set_alpha(self.image.get_alpha() - 5)

    def show(self, duration):
        self.last_update = pygame.time.get_ticks() + (duration * 1000)
        self.update_health(255)

    def update_health(self, alpha):
        self.image = pygame.Surface((self.rect.width, self.rect.height)).convert_alpha()
        hp_percent = (self._parent.hp / self._parent.max_hp)
        border = self.BORDER
        width = self.rect.width
        height = self.rect.height
        pygame.draw.rect(self.image, (50, 50, 50), (0, 0, self.rect.w, self.rect.h))
        pygame.draw.rect(self.image, (136, 8, 8), (border, border, hp_percent * (width - 2 * border), height - 2 * border))
        self.image.set_alpha(alpha)


class TeamColorSprite(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet, width, height, animation_cooldown, frame_ranges, team):
        pygame.sprite.Sprite.__init__(self)

        self.sprite_sheet = pygame.image.load(sprite_sheet).convert_alpha()
        self.rect = pygame.rect.Rect(0, 0, width, height)
        self.animation_cooldown = animation_cooldown
        self.frame_ranges = frame_ranges
        self.team = team

        self.current_frame_loop = 0
        self.current_frame = self.frame_ranges[self.current_frame_loop][0]
        self.last_update = pygame.time.get_ticks()

        self._getimage(self.current_frame)

    def get_rect(self):
        return pygame.Rect(self.rect.x, self.rect.y, self.image.get_rect().w, self.image.get_rect().h)

    def pause_animation(self, seconds):
        self.last_update = pygame.time.get_ticks() + (seconds * 1000)

    def update(self, *args, **kwargs):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_cooldown:
            self.last_update = current_time
            self.current_frame += 1

            if self.current_frame not in range(self.frame_ranges[self.current_frame_loop][0] + 1,
                                               self.frame_ranges[self.current_frame_loop][1] + 1):
                self.current_frame = self.frame_ranges[self.current_frame_loop][0]

            self._getimage(self.current_frame)

    def _getimage(self, frame):
        self.image = pygame.Surface((self.rect.width, self.rect.height)).convert_alpha()
        pygame.draw.rect(self.image, self.team.team_color, (0, 0, self.rect.width, self.rect.height))

        self.image.blit(self.sprite_sheet, (0, 0), (self.rect.width * (frame - 1), 0, self.rect.width, self.rect.height))

        self.image = pygame.transform.scale_by(self.image, constant.SCALE)
        self.image.set_colorkey((0, 0, 0))