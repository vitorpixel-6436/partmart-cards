from PIL import Image, ImageDraw, ImageFont, ImageFilter
from abc import ABC, abstractmethod
import os
from django.conf import settings


class BaseCardGenerator(ABC):
    """
    Базовый класс для генераторов карточек
    """
    
    def __init__(self, pc_build):
        self.pc_build = pc_build
        self.canvas_size = (1200, 1200)
        self.fonts_loaded = False
        self.fonts = {}
        
    def load_fonts(self):
        """Загрузка шрифтов"""
        if self.fonts_loaded:
            return
        
        try:
            # Пытаемся загрузить системные шрифты
            font_paths = [
                '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
                '/System/Library/Fonts/Supplemental/Arial Bold.ttf',
                'C:\\Windows\\Fonts\\arialbd.ttf',
            ]
            
            font_path = None
            for path in font_paths:
                if os.path.exists(path):
                    font_path = path
                    break
            
            if font_path:
                self.fonts['title'] = ImageFont.truetype(font_path, 72)
                self.fonts['large'] = ImageFont.truetype(font_path, 48)
                self.fonts['medium'] = ImageFont.truetype(font_path, 36)
                self.fonts['small'] = ImageFont.truetype(font_path, 28)
                self.fonts['tiny'] = ImageFont.truetype(font_path, 20)
            else:
                # Fallback на стандартный шрифт
                self.fonts['title'] = ImageFont.load_default()
                self.fonts['large'] = ImageFont.load_default()
                self.fonts['medium'] = ImageFont.load_default()
                self.fonts['small'] = ImageFont.load_default()
                self.fonts['tiny'] = ImageFont.load_default()
            
            self.fonts_loaded = True
        except Exception as e:
            print(f"Error loading fonts: {e}")
            # Используем стандартный шрифт
            default_font = ImageFont.load_default()
            self.fonts = {k: default_font for k in ['title', 'large', 'medium', 'small', 'tiny']}
            self.fonts_loaded = True
    
    def load_and_resize_photo(self, target_size):
        """Загрузка и изменение размера фото ПК"""
        try:
            photo = Image.open(self.pc_build.photo.path)
            
            # Конвертируем в RGB если нужно
            if photo.mode != 'RGB':
                photo = photo.convert('RGB')
            
            # Масштабируем с сохранением пропорций
            photo.thumbnail(target_size, Image.Resampling.LANCZOS)
            
            # Создаем новое изображение с центрированием
            result = Image.new('RGB', target_size, (0, 0, 0))
            offset = ((target_size[0] - photo.width) // 2, (target_size[1] - photo.height) // 2)
            result.paste(photo, offset)
            
            return result
        except Exception as e:
            print(f"Error loading photo: {e}")
            # Возвращаем черное изображение при ошибке
            return Image.new('RGB', target_size, (0, 0, 0))
    
    def draw_text_with_outline(self, draw, position, text, font, fill_color, outline_color, outline_width=2):
        """Отрисовка текста с обводкой"""
        x, y = position
        
        # Рисуем обводку
        for offset_x in range(-outline_width, outline_width + 1):
            for offset_y in range(-outline_width, outline_width + 1):
                draw.text((x + offset_x, y + offset_y), text, font=font, fill=outline_color)
        
        # Рисуем основной текст
        draw.text(position, text, font=font, fill=fill_color)
    
    def add_gradient_overlay(self, image, color1, color2, direction='vertical'):
        """Добавление градиентного оверлея"""
        gradient = Image.new('RGBA', image.size, color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(gradient)
        
        if direction == 'vertical':
            for i in range(image.height):
                ratio = i / image.height
                r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                a = int(color1[3] * (1 - ratio) + color2[3] * ratio) if len(color1) > 3 else 255
                draw.line([(0, i), (image.width, i)], fill=(r, g, b, a))
        
        return Image.alpha_composite(image.convert('RGBA'), gradient)
    
    def get_output_path(self):
        """Получить путь для сохранения файла"""
        filename = f'pc_card_{self.pc_build.pk}_{self.pc_build.style}.png'
        return os.path.join('generated', filename)
    
    def save_card(self, image):
        """Сохранение готовой карточки"""
        output_path = self.get_output_path()
        full_path = os.path.join(settings.MEDIA_ROOT, output_path)
        
        # Создаем директорию если не существует
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # Сохраняем в высоком качестве
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        image.save(full_path, 'PNG', quality=95, optimize=True)
        
        return output_path
    
    @abstractmethod
    def generate(self):
        """Абстрактный метод генерации - должен быть реализован в подклассах"""
        pass
