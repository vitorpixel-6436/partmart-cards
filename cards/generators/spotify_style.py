from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os
from django.conf import settings
from .card_generator import CardGenerator


class SpotifyStyleGenerator:
    """
    🎵 Spotify Minimal Style Generator
    Ультра-чистый минималистичный дизайн
    """
    
    # Цветовая палитра Spotify
    COLOR_BLACK = (18, 18, 18)
    COLOR_GREEN = (30, 215, 96)
    COLOR_WHITE = (255, 255, 255)
    COLOR_GRAY = (179, 179, 179)
    
    def __init__(self, pc_build):
        self.pc_build = pc_build
        self.canvas_size = (1200, 1200)
    
    def generate(self):
        """
        Генерирует карточку в Spotify стиле
        """
        # Черный фон
        img = Image.new('RGB', self.canvas_size, color=self.COLOR_BLACK)
        draw = ImageDraw.Draw(img)
        
        # Фото
        pc_photo = Image.open(self.pc_build.photo.path)
        pc_photo = self._prepare_photo(pc_photo)
        
        # Квадратное фото сверху
        img.paste(pc_photo, (100, 100))
        
        # Лого
        self._add_logo(draw)
        
        # Характеристики - минимум элементов
        self._add_specs(draw)
        
        # Цена - очень крупно
        self._add_price(draw)
        
        # Бонусы
        if self.pc_build.bonuses:
            self._add_bonuses(draw)
        
        return self._save_image(img)
    
    def _prepare_photo(self, photo):
        """Подготавливает фото"""
        # Квадрат 1000x1000
        min_side = min(photo.width, photo.height)
        left = (photo.width - min_side) // 2
        top = (photo.height - min_side) // 2
        photo = photo.crop((left, top, left + min_side, top + min_side))
        
        photo = photo.resize((1000, 1000), Image.Resampling.LANCZOS)
        
        return photo
    
    def _add_logo(self, draw):
        """Лого"""
        font = CardGenerator.get_font(32, bold=True)
        draw.text((40, 30), "PARTMART", font=font, fill=self.COLOR_GREEN)
    
    def _add_specs(self, draw):
        """Характеристики - только основные"""
        font_value = CardGenerator.get_font(20, bold=False)
        
        # Только CPU и GPU
        specs_text = f"{self.pc_build.cpu} • {self.pc_build.gpu}"
        
        # Длинную строку разбиваем
        if len(specs_text) > 60:
            draw.text((40, 1120), self.pc_build.cpu, font=font_value, fill=self.COLOR_GRAY)
            draw.text((40, 1150), self.pc_build.gpu, font=font_value, fill=self.COLOR_GRAY)
        else:
            draw.text((40, 1135), specs_text, font=font_value, fill=self.COLOR_GRAY)
    
    def _add_price(self, draw):
        """Цена - самый заметный элемент"""
        price_font = CardGenerator.get_font(80, bold=True)
        price_text = f"{int(self.pc_build.price):,}".replace(',', ' ') + " ₽"
        
        bbox = draw.textbbox((0, 0), price_text, font=price_font)
        text_width = bbox[2] - bbox[0]
        
        # Справа снизу
        x = 1200 - text_width - 40
        y = 1090
        
        draw.text((x, y), price_text, font=price_font, fill=self.COLOR_GREEN)
    
    def _add_bonuses(self, draw):
        """Бонусы"""
        font = CardGenerator.get_font(16, bold=False)
        line = self.pc_build.bonuses.split('\n')[0]  # Только первая строка
        
        if line:
            draw.text((40, 1100), f"✨ {line.strip()}", font=font, fill=self.COLOR_WHITE)
    
    def _save_image(self, img):
        """Сохраняет изображение"""
        filename = f"partmart_spotify_{self.pc_build.pk}.png"
        filepath = os.path.join(settings.MEDIA_ROOT, 'generated', filename)
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        img.save(filepath, 'PNG', quality=95, optimize=True)
        
        return os.path.join('generated', filename)
