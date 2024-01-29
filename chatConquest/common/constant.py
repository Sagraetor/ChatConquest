import os
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent

SCREEN_RATIO = [480, 720]
BACKGROUND = os.path.join(ROOT_DIR, 'Assets\\Map.png')
TOWER = os.path.join(ROOT_DIR, 'Assets\\Tower.png')
CASTLE = os.path.join(ROOT_DIR, 'Assets\\Castle.png')
KNIGHT = os.path.join(ROOT_DIR, 'Assets\\Knight.png')
MAGE = os.path.join(ROOT_DIR, 'Assets\\Mage.png')
FONT = os.path.join(ROOT_DIR, 'Assets\\Fonts\\PixeloidSans-mLxMm.ttf')
FONT_BOLD = os.path.join(ROOT_DIR, 'Assets\\Fonts\\PixeloidSansBold-PKnYd.ttf')
TIK_TOK_ID = os.path.join(ROOT_DIR, "@lttqzd2002")
SCALE = 2

TOWER_COORDINATES = [(165, 9),
                     (283, 7),
                     (190, 114),
                     (258, 114),
                     (71, 137),
                     (378, 132),
                     (127, 205),
                     (318, 201),
                     (33, 259),
                     (416, 254),
                     (167, 299),
                     (33, 338),
                     (127, 396),
                     (71, 460),
                     (192, 479),
                     (165, 584)]

CASTLE_COORDINATES = [(14, 8),
                      (371, 8),
                      (11, 576),]

PATHS = [(1, 8),
         (4, 6),
         (5, 7),
         (2, 9),
         (6, 7),
         (8, 10),
         (6, 10),
         (7, 11),
         (9, 11),
         (11, 13),
         (10, 12),
         (10, 14),
         (11, 14),
         (12, 15),
         (14, 16),
         (15, 16),
         (16, 17),
         (16, 18),
         (19, 18),
         (3, 17),]
