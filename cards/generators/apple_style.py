from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os
from django.conf import settings
from .card_generator import CardGenerator


class AppleStyleGenerator:
    """
    🍎 Apple Premium Style Generator
    Минималистичный liquid glass дизайн
    """
    
    # Цветовая палитра Apple
    COLOR_WHITE = (255, 255, 255)
    COLOR_LIGHT_GRAY = (247, 247, 247)
    COLOR_DARK_GRAY = (29, 29, 31)
    COLOR_ACCENT = (0, 122, 255)  # Apple Blue
    COLOR_TEXT = (51, 51, 51)
    
    def __init__(self, pc_build):
        self.pc_build = pc_build
        self.canvas_size = (1200, 1200)
    
    def generate(self):
        """
        Генерирует карточку в Apple стиле
        """
        # Светлый фон
        img = Image.new('RGB', self.canvas_size, color=self.COLOR_WHITE)
        draw = ImageDraw.Draw(img)
        
        # Фото ПК
        pc_photo = Image.open(self.pc_build.photo.path)
        pc_photo = self._prepare_photo(pc_photo)
        
        # Размещаем фото в круглом контейнере
        self._add_photo_container(img, pc_photo)
        
        # Лого
        self._add_logo(draw)
        
        # Характеристики в минималистичном стиле
        self._add_specs(draw)
        
        # Цена - самый заметный элемент
        self._add_price(draw)
        
        # Бонусы
        if self.pc_build.bonuses:
            self._add_bonuses(draw)
        
        return self._save_image(img)
    
    def _prepare_photo(self, photo):
        """Подготавливает фото"""
        # Квадратное кадрирование
        min_side = min(photo.width, photo.height)
        left = (photo.width - min_side) // 2
        top = (photo.height - min_side) // 2
        photo = photo.crop((left, top, left + min_side, top + min_side))
        
        # Размер 700x700
        photo = photo.resize((700, 700), Image.Resampling.LANCZOS)
        
        return photo
    
    def _add_photo_container(self, img, photo):
        """Добавляет фото в скругленном контейнере"""
        # Создаем маску со скругленными углами
        mask = Image.new('L', (700, 700), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([(0, 0), (700, 700)], radius=30, fill=255)
        
        # Применяем маску
        output = Image.new('RGBA', (700, 700), (0, 0, 0, 0))
        output.paste(photo, (0, 0))
        output.putalpha(mask)
        
        # Вставляем в центр сверху
        img.paste(output, (250, 80), output)
        
        # Добавляем тонкую тень
        shadow = Image.new('RGBA', self.canvas_size, (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        shadow_draw.rounded_rectangle(
            [(255, 85), (945, 775)],
            radius=30,
            outline=(0, 0, 0, 20),
            width=2
        )
        img.paste(shadow, (0, 0), shadow)
    
    def _add_logo(self, draw):
        """Лого ПАРТМАРТ"""
        font = CardGenerator.get_font(36, bold=True)
        draw.text((50, 30), "PARTMART", font=font, fill=self.COLOR_DARK_GRAY)
    
    def _add_specs(self, draw):
        """Характеристики"""
        specs = self.pc_build.get_specs_list()
        y_offset = 820
        
        font_label = CardGenerator.get_font(14, bold=True)
        font_value = CardGenerator.get_font(18, bold=False)
        
        # Две колонки
        left_specs = specs[:4]
        right_specs = specs[4:]
        
        # Левая колонка
        for label, value in left_specs:
            draw.text((80, y_offset), label, font=font_label, fill=self.COLOR_ACCENT)
            draw.text((80, y_offset + 20), value, font=font_value, fill=self.COLOR_TEXT)
            y_offset += 55
        
        # Правая колонка
        y_offset = 820
        for label, value in right_specs:
            draw.text((620, y_offset), label, font=font_label, fill=self.COLOR_ACCENT)
            draw.text((620, y_offset + 20), value, font=font_value, fill=self.COLOR_TEXT)
            y_offset += 55
    
    def _add_price(self, draw):
        """Цена"""
        price_font = CardGenerator.get_font(68, bold=True)
        price_text = f"{int(self.pc_build.price):,}".replace(',', ' ') + " ₽"
        
        bbox = draw.textbbox((0, 0), price_text, font=price_font)
        text_width = bbox[2] - bbox[0]
        
        # Центрируем по горизонтали
        x = (1200 - text_width) // 2
        y = 1100
        
        draw.text((x, y), price_text, font=price_font, fill=self.COLOR_ACCENT)
    
    def _add_bonuses(self, draw):
        """Бонусы"""
        font = CardGenerator.get_font(14, bold=False)
        lines = self.pc_build.bonuses.split('\n')[:2]
        
        # Центрируем
        y = 1050
        for line in lines:
            text = f"✨ {line.strip()}"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            x = (1200 - text_width) // 2
            draw.text((x, y), text, font=font, fill=self.COLOR_TEXT)
            y += 22
    
    def _save_image(self, img):
        """Сохраняет изображение"""
        filename = f"partmart_apple_{self.pc_build.pk}.png"
        filepath = os.path.join(settings.MEDIA_ROOT, 'generated', filename)
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        img.save(filepath, 'PNG', quality=95, optimize=True)
        
        return os.path.join('generated', filename)
