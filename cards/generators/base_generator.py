from PIL import Image, ImageDraw, ImageFont, ImageFilter
from abc import ABC, abstractmethod
import os
from django.conf import settings


class BaseCardGenerator(ABC):
    """
    Базовый класс для всех генераторов карточек
    """
    
    # Размер карточки для Авито
    CARD_SIZE = (1200, 1200)
    
    def __init__(self, pc_build):
        self.build = pc_build
        self.width, self.height = self.CARD_SIZE
        
    @abstractmethod
    def generate(self):
        """
        Генерирует карточку в определенном стиле
        """
        pass
    
    def load_and_prepare_photo(self, target_size=None):
        """
        Загружает и подготавливает фото ПК
        """
        if target_size is None:
            target_size = (self.width, int(self.height * 0.6))
        
        photo = Image.open(self.build.photo.path)
        photo = photo.convert('RGB')
        
        # Масштабируем с сохранением пропорций
        photo.thumbnail(target_size, Image.Resampling.LANCZOS)
        
        # Создаем центрированное изображение
        result = Image.new('RGB', target_size, (0, 0, 0))
        offset = ((target_size[0] - photo.width) // 2, 
                  (target_size[1] - photo.height) // 2)
        result.paste(photo, offset)
        
        return result
    
    def create_gradient(self, direction='vertical', colors=None):
        """
        Создает градиентный фон
        direction: 'vertical', 'horizontal', 'diagonal'
        colors: [(r,g,b), (r,g,b)] - начальный и конечный цвета
        """
        if colors is None:
            colors = [(0, 0, 0), (40, 40, 40)]
        
        img = Image.new('RGB', self.CARD_SIZE, colors[0])
        draw = ImageDraw.Draw(img)
        
        if direction == 'vertical':
            for i in range(self.height):
                ratio = i / self.height
                color = self._interpolate_color(colors[0], colors[1], ratio)
                draw.line([(0, i), (self.width, i)], fill=color)
        elif direction == 'horizontal':
            for i in range(self.width):
                ratio = i / self.width
                color = self._interpolate_color(colors[0], colors[1], ratio)
                draw.line([(i, 0), (i, self.height)], fill=color)
        elif direction == 'diagonal':
            for i in range(self.width + self.height):
                ratio = i / (self.width + self.height)
                color = self._interpolate_color(colors[0], colors[1], ratio)
                for x in range(self.width):
                    y = i - x
                    if 0 <= y < self.height:
                        draw.point((x, y), fill=color)
        
        return img
    
    def _interpolate_color(self, color1, color2, ratio):
        """
        Интерполирует между двумя цветами
        """
        return tuple(int(color1[i] + (color2[i] - color1[i]) * ratio) for i in range(3))
    
    def add_glass_effect(self, img, blur_radius=10, opacity=180):
        """
        Добавляет эффект матового стекла (frosted glass)
        """
        # Создаем размытую версию
        blurred = img.filter(ImageFilter.GaussianBlur(blur_radius))
        
        # Создаем полупрозрачный белый слой
        glass_overlay = Image.new('RGBA', img.size, (255, 255, 255, opacity))
        
        # Конвертируем в RGBA если нужно
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        if blurred.mode != 'RGBA':
            blurred = blurred.convert('RGBA')
        
        # Комбинируем
        result = Image.alpha_composite(blurred, glass_overlay)
        
        return result
    
    def draw_rounded_rectangle(self, draw, xy, radius, fill=None, outline=None, width=1):
        """
        Рисует прямоугольник со скругленными углами
        """
        x1, y1, x2, y2 = xy
        
        # Рисуем основной прямоугольник
        draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill, outline=outline, width=width)
        draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill, outline=outline, width=width)
        
        # Рисуем углы
        draw.pieslice([x1, y1, x1 + radius * 2, y1 + radius * 2], 180, 270, fill=fill, outline=outline)
        draw.pieslice([x2 - radius * 2, y1, x2, y1 + radius * 2], 270, 360, fill=fill, outline=outline)
        draw.pieslice([x1, y2 - radius * 2, x1 + radius * 2, y2], 90, 180, fill=fill, outline=outline)
        draw.pieslice([x2 - radius * 2, y2 - radius * 2, x2, y2], 0, 90, fill=fill, outline=outline)
    
    def get_font(self, size, bold=False):
        """
        Загружает шрифт нужного размера
        """
        try:
            if bold:
                # Попытка загрузить жирный шрифт
                font_paths = [
                    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
                    'C:\\Windows\\Fonts\\arialbd.ttf',
                    '/System/Library/Fonts/Helvetica.ttc',
                ]
            else:
                font_paths = [
                    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
                    'C:\\Windows\\Fonts\\arial.ttf',
                    '/System/Library/Fonts/Helvetica.ttc',
                ]
            
            for font_path in font_paths:
                if os.path.exists(font_path):
                    return ImageFont.truetype(font_path, size)
            
            # Fallback на дефолтный
            return ImageFont.load_default()
        except:
            return ImageFont.load_default()
    
    def format_price(self, price):
        """
        Форматирует цену для отображения
        """
        return f"{int(price):,}".replace(',', ' ') + ' ₽'
