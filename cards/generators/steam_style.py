from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os
from django.conf import settings
from .card_generator import CardGenerator


class SteamStyleGenerator:
    """
    🎮 Steam Library Style Generator
    Glass morphism эффекты и игровая эстетика
    """
    
    # Цветовая палитра Steam
    COLOR_DARK_BLUE = (27, 40, 56)
    COLOR_STEAM_BLUE = (102, 192, 244)
    COLOR_WHITE = (255, 255, 255)
    COLOR_GLASS = (255, 255, 255, 40)
    
    def __init__(self, pc_build):
        self.pc_build = pc_build
        self.canvas_size = (1200, 1200)
    
    def generate(self):
        """
        Генерирует карточку в Steam стиле
        """
        # Создаем холст
        img = Image.new('RGB', self.canvas_size, color=self.COLOR_DARK_BLUE)
        
        # Загружаем фото
        pc_photo = Image.open(self.pc_build.photo.path)
        pc_photo = self._prepare_photo(pc_photo)
        
        # Размытие фона
        background = pc_photo.copy()
        background = background.filter(ImageFilter.GaussianBlur(radius=20))
        enhancer = ImageEnhance.Brightness(background)
        background = enhancer.enhance(0.4)
        img.paste(background, (0, 0))
        
        # Фото ПК в центре сверху
        photo_small = pc_photo.resize((900, 600), Image.Resampling.LANCZOS)
        img.paste(photo_small, (150, 50))
        
        # Glass-панели с характеристиками
        self._add_glass_specs(img)
        
        # Лого
        draw = ImageDraw.Draw(img)
        self._add_logo(draw)
        
        # Цена
        self._add_price(draw)
        
        # Бонусы
        if self.pc_build.bonuses:
            self._add_bonuses(draw)
        
        return self._save_image(img)
    
    def _prepare_photo(self, photo):
        """Подготавливает фото"""
        aspect = photo.width / photo.height
        new_width = 1200
        new_height = int(new_width / aspect)
        
        if new_height < 800:
            new_height = 800
            new_width = int(new_height * aspect)
        
        photo = photo.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Центрируем
        left = (new_width - 1200) // 2
        top = (new_height - 800) // 2
        photo = photo.crop((left, top, left + 1200, top + 800))
        
        return photo
    
    def _add_glass_specs(self, img):
        """Добавляет glass-панели с характеристиками"""
        overlay = Image.new('RGBA', self.canvas_size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        specs = self.pc_build.get_specs_list()
        x_offset = 60
        y_offset = 680
        
        font_label = CardGenerator.get_font(16, bold=True)
        font_value = CardGenerator.get_font(20, bold=False)
        
        for label, value in specs:
            # Glass-панель
            CardGenerator.add_rounded_rectangle(
                draw,
                (x_offset, y_offset, x_offset + 1080, y_offset + 70),
                radius=10,
                fill=(255, 255, 255, 40),
                outline=(102, 192, 244, 100),
                width=2
            )
            
            y_offset += 80
        
        img.paste(overlay, (0, 0), overlay)
        
        # Текст поверх glass
        draw = ImageDraw.Draw(img)
        y_offset = 690
        
        for label, value in specs:
            draw.text((80, y_offset), label, font=font_label, fill=self.COLOR_STEAM_BLUE)
            draw.text((80, y_offset + 25), value, font=font_value, fill=self.COLOR_WHITE)
            y_offset += 80
    
    def _add_logo(self, draw):
        """Лого ПАРТМАРТ"""
        font = CardGenerator.get_font(42, bold=True)
        draw.text((50, 30), "PARTMART", font=font, fill=self.COLOR_STEAM_BLUE)
    
    def _add_price(self, draw):
        """Цена"""
        price_font = CardGenerator.get_font(64, bold=True)
        price_text = f"{int(self.pc_build.price):,}".replace(',', ' ') + " ₽"
        
        bbox = draw.textbbox((0, 0), price_text, font=price_font)
        text_width = bbox[2] - bbox[0]
        
        x = 1200 - text_width - 60
        y = 30
        
        draw.text((x, y), price_text, font=price_font, fill=self.COLOR_STEAM_BLUE)
    
    def _add_bonuses(self, draw):
        """Бонусы"""
        font = CardGenerator.get_font(16, bold=False)
        lines = self.pc_build.bonuses.split('\n')[:2]
        
        y = 100
        for line in lines:
            draw.text((60, y), f"✨ {line.strip()}", font=font, fill=(255, 255, 255, 200))
            y += 25
    
    def _save_image(self, img):
        """Сохраняет изображение"""
        filename = f"partmart_steam_{self.pc_build.pk}.png"
        filepath = os.path.join(settings.MEDIA_ROOT, 'generated', filename)
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        img.save(filepath, 'PNG', quality=95, optimize=True)
        
        return os.path.join('generated', filename)
