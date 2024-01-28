import io
import pygame
from chatConquest.game.character import create_character
from PIL import Image, ImageDraw, ImageFilter


class _Players:
    class _Player:
        def __init__(self, username, image):
            self.username = username

            self.character = None
            self.team = None
            self.icon = None

            try:
                image = self._mask_avatar_to_circle(Image.open(io.BytesIO(image)), 2)
                self.icon = pygame.transform.scale(pygame.image.frombuffer(image.tobytes(), image.size, image.mode),
                                                   (16, 16))
            except:
                pass

        def _mask_avatar_to_circle(self, original: Image, blur_radius: int, offset: int = 0) -> Image:
            offset += blur_radius * 2
            mask = Image.new("L", original.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((offset, offset, original.size[0] - offset, original.size[1] - offset), fill=255)
            mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))

            result = original.copy()
            result.putalpha(mask)

            return result

        def character_killed(self):
            self.character = None

        def new_character(self, unit_type='a'):
            match unit_type:
                case 'a':
                    self.character = create_character(self.team.castle.id_, self.team, "knight", self.character_killed)
                case 'b':
                    self.character = create_character(self.team.castle.id_, self.team, "mage", self.character_killed)

    def __init__(self):
        self.players = []

    def __call__(self, username, icon):
        for player in self.players:
            if player.username == username:
                return player
        else:
            self.players.append(self._Player(username, icon))

    def __str__(self):
        string = ""
        for player in self.players:
            string += player.username
            string += ", "
        return string


players = _Players()
