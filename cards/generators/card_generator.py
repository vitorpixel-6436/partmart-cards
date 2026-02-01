from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os
from django.conf import settings
from .msi_style import MSIStyleGenerator
from .steam_style import SteamStyleGenerator
from .apple_style import AppleStyleGenerator
from .spotify_style import SpotifyStyleGenerator


class CardGenerator:
    """
    Главный генератор карточек - выбирает нужный стиль
    """
    
    CANVAS_SIZE = (1200, 1200)
    
    def __init__(self, pc_build):
        self.pc_build = pc_build
        self.style_generators = {
            'msi': MSIStyleGenerator,
            'steam': SteamStyleGenerator,
            'apple': AppleStyleGenerator,
            'spotify': SpotifyStyleGenerator,
        }
    
    def generate(self):
        """
        Генерирует карточку в выбранном стиле
        """
        generator_class = self.style_generators.get(self.pc_build.style, MSIStyleGenerator)
        generator = generator_class(self.pc_build)
        return generator.generate()
    
    @staticmethod
    def get_font(size, bold=False):
        """
        Получить шрифт нужного размера
        """
        try:
            if bold:
                return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
            return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
        except:
            # Fallback для Windows
            try:
                if bold:
                    return ImageFont.truetype("arial.ttf", size)
                return ImageFont.truetype("arial.ttf", size)
            except:
                return ImageFont.load_default()
    
    @staticmethod
    def add_rounded_rectangle(draw, xy, radius, fill, outline=None, width=1):
        """
        Рисует скругленный прямоугольник
        """
        x1, y1, x2, y2 = xy
        draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill, outline=outline, width=width)
        draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill, outline=outline, width=width)
        draw.pieslice([x1, y1, x1 + radius * 2, y1 + radius * 2], 180, 270, fill=fill, outline=outline)
        draw.pieslice([x2 - radius * 2, y1, x2, y1 + radius * 2], 270, 360, fill=fill, outline=outline)
        draw.pieslice([x1, y2 - radius * 2, x1 + radius * 2, y2], 90, 180, fill=fill, outline=outline)
        draw.pieslice([x2 - radius * 2, y2 - radius * 2, x2, y2], 0, 90, fill=fill, outline=outline)
