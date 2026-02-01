from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os
from django.conf import settings
from .card_generator import CardGenerator


class MSIStyleGenerator:
    """
    🔴 MSI Gaming Style Generator
    Агрессивный красно-черный дизайн с RGB-подсветкой
    """
    
    # Цветовая палитра MSI
    COLOR_BLACK = (13, 13, 13)
    COLOR_RED = (227, 6, 19)
    COLOR_DARK_RED = (140, 0, 0)
    COLOR_WHITE = (255, 255, 255)
    COLOR_GRAY = (180, 180, 180)
    
    def __init__(self, pc_build):
        self.pc_build = pc_build
        self.canvas_size = (1200, 1200)
    
    def generate(self):
        """
        Генерирует карточку в MSI стиле
        """
        # Создаем холст
        img = Image.new('RGB', self.canvas_size, color=self.COLOR_BLACK)
        draw = ImageDraw.Draw(img)
        
        # Загружаем и обрабатываем фото ПК
        pc_photo = Image.open(self.pc_build.photo.path)
        pc_photo = self._prepare_photo(pc_photo)
        
        # Размещаем фото в верхней части
        img.paste(pc_photo, (0, 0))
        
        # Добавляем градиентный overlay
        self._add_gradient_overlay(img)
        
        # Добавляем диагональные линии
        self._add_diagonal_lines(img)
        
        # Добавляем лого ПАРТМАРТ
        draw = ImageDraw.Draw(img)
        self._add_logo(draw)
        
        # Добавляем характеристики
        self._add_specs(draw)
        
        # Добавляем цену
        self._add_price(draw)
        
        # Добавляем бонусы
        if self.pc_build.bonuses:
            self._add_bonuses(draw)
        
        # Сохраняем
        return self._save_image(img)
    
    def _prepare_photo(self, photo):
        """Подготавливает фото ПК"""
        # Обрезаем и масштабируем
        target_width = 1200
        target_height = 700
        
        # Сохраняем пропорции
        aspect = photo.width / photo.height
        if aspect > target_width / target_height:
            new_height = target_height
            new_width = int(new_height * aspect)
        else:
            new_width = target_width
            new_height = int(new_width / aspect)
        
        photo = photo.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Центрируем
        left = (new_width - target_width) // 2
        top = (new_height - target_height) // 2
        photo = photo.crop((left, top, left + target_width, top + target_height))
        
        # Приглушаем яркость
        enhancer = ImageEnhance.Brightness(photo)
        photo = enhancer.enhance(0.7)
        
        return photo
    
    def _add_gradient_overlay(self, img):
        """Добавляет градиентный overlay"""
        overlay = Image.new('RGBA', self.canvas_size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Градиент снизу вверх
        for i in range(700, 1200):
            alpha = int((i - 700) / 500 * 200)
            draw.rectangle([(0, i), (1200, i + 1)], fill=(13, 13, 13, alpha))
        
        img.paste(overlay, (0, 0), overlay)
    
    def _add_diagonal_lines(self, img):
        """Добавляет диагональные линии MSI-стиля"""
        overlay = Image.new('RGBA', self.canvas_size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Диагональные линии
        for i in range(0, 1400, 100):
            draw.line([(i, 0), (i - 400, 400)], fill=(227, 6, 19, 30), width=3)
        
        img.paste(overlay, (0, 0), overlay)
    
    def _add_logo(self, draw):
        """Добавляет лого ПАРТМАРТ"""
        font = CardGenerator.get_font(48, bold=True)
        text = "PARTMART"
        
        # Тень
        draw.text((52, 32), text, font=font, fill=(0, 0, 0, 180))
        # Основной текст
        draw.text((50, 30), text, font=font, fill=self.COLOR_RED)
    
    def _add_specs(self, draw):
        """Добавляет характеристики"""
        specs = self.pc_build.get_specs_list()
        y_offset = 720
        
        font_label = CardGenerator.get_font(18, bold=True)
        font_value = CardGenerator.get_font(22, bold=False)
        
        for label, value in specs:
            # Лейбл
            draw.text((50, y_offset), label, font=font_label, fill=self.COLOR_RED)
            # Значение
            draw.text((50, y_offset + 25), value, font=font_value, fill=self.COLOR_WHITE)
            
            y_offset += 65
    
    def _add_price(self, draw):
        """Добавляет цену"""
        price_font = CardGenerator.get_font(72, bold=True)
        price_text = f"{int(self.pc_build.price):,}".replace(',', ' ') + " ₽"
        
        # Позиция справа снизу
        bbox = draw.textbbox((0, 0), price_text, font=price_font)
        text_width = bbox[2] - bbox[0]
        
        x = 1200 - text_width - 50
        y = 1100
        
        # Тень
        draw.text((x + 3, y + 3), price_text, font=price_font, fill=(0, 0, 0, 200))
        # Основной текст
        draw.text((x, y), price_text, font=price_font, fill=self.COLOR_RED)
    
    def _add_bonuses(self, draw):
        """Добавляет бонусы"""
        font = CardGenerator.get_font(16, bold=False)
        lines = self.pc_build.bonuses.split('\n')[:2]  # Максимум 2 строки
        
        y = 1030
        for line in lines:
            draw.text((50, y), f"✨ {line.strip()}", font=font, fill=self.COLOR_GRAY)
            y += 25
    
    def _save_image(self, img):
        """Сохраняет изображение"""
        filename = f"partmart_msi_{self.pc_build.pk}.png"
        filepath = os.path.join(settings.MEDIA_ROOT, 'generated', filename)
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        img.save(filepath, 'PNG', quality=95, optimize=True)
        
        return os.path.join('generated', filename)
