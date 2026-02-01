from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
from .base_generator import BaseCardGenerator


class MSIStyleGenerator(BaseCardGenerator):
    """
    🔴 MSI Gaming Style - агрессивный красно-черный дизайн
    """
    
    # MSI фирменные цвета
    MSI_RED = (227, 6, 19)
    MSI_BLACK = (13, 13, 13)
    MSI_DARK_GRAY = (30, 30, 30)
    MSI_LIGHT_GRAY = (200, 200, 200)
    
    def generate(self):
        """
        Генерирует карточку в стиле MSI Gaming
        """
        # Создаем базовый черный фон
        card = Image.new('RGB', self.CARD_SIZE, self.MSI_BLACK)
        
        # Добавляем диагональные линии
        card = self._add_diagonal_lines(card)
        
        # Загружаем и размещаем фото ПК
        photo = self.load_and_prepare_photo((1200, 720))
        
        # Затемняем низ фото для плавного перехода
        photo = self._add_gradient_overlay(photo)
        
        # Размещаем фото в верхней части
        card.paste(photo, (0, 0))
        
        # Рисуем элементы интерфейса
        draw = ImageDraw.Draw(card)
        
        # Логотип ПАРТМАРТ в углу
        self._draw_logo(draw)
        
        # RGB accent линия
        self._draw_rgb_accent(draw)
        
        # Карточки характеристик
        self._draw_specs_panel(draw)
        
        # Цена - самый заметный элемент
        self._draw_price(draw)
        
        # Бонусы если есть
        if self.build.bonuses:
            self._draw_bonuses(draw)
        
        return card
    
    def _add_diagonal_lines(self, img):
        """
        Добавляет диагональные линии в стиле MSI
        """
        draw = ImageDraw.Draw(img, 'RGBA')
        
        # Рисуем несколько диагональных полос
        for i in range(0, self.width + self.height, 100):
            # Полупрозрачные красные линии
            points = [
                (i, 0),
                (i + 50, 0),
                (0, i + 50),
                (0, i)
            ]
            if i < self.width:
                draw.polygon(points, fill=(227, 6, 19, 10))
        
        return img
    
    def _add_gradient_overlay(self, photo):
        """
        Добавляет градиентное затемнение снизу
        """
        overlay = Image.new('RGBA', photo.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Градиент от прозрачного к черному
        for y in range(photo.height // 2, photo.height):
            alpha = int(255 * (y - photo.height // 2) / (photo.height // 2))
            draw.line([(0, y), (photo.width, y)], fill=(0, 0, 0, alpha))
        
        photo = photo.convert('RGBA')
        return Image.alpha_composite(photo, overlay).convert('RGB')
    
    def _draw_logo(self, draw):
        """
        Рисует логотип ПАРТМАРТ
        """
        font = self.get_font(48, bold=True)
        text = "ПАРТМАРТ"
        
        # Позиция в правом верхнем углу
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        x = self.width - text_width - 40
        y = 30
        
        # Тень
        draw.text((x + 3, y + 3), text, fill=(0, 0, 0), font=font)
        # Основной текст красным
        draw.text((x, y), text, fill=self.MSI_RED, font=font)
    
    def _draw_rgb_accent(self, draw):
        """
        Рисует RGB accent линию
        """
        y_pos = 740
        gradient_colors = [
            (255, 0, 0),    # Red
            (255, 127, 0),  # Orange  
            (255, 255, 0),  # Yellow
            (0, 255, 0),    # Green
            (0, 0, 255),    # Blue
            (139, 0, 255),  # Purple
        ]
        
        segment_width = self.width // len(gradient_colors)
        
        for i, color in enumerate(gradient_colors):
            x1 = i * segment_width
            x2 = (i + 1) * segment_width
            draw.rectangle([x1, y_pos, x2, y_pos + 4], fill=color)
    
    def _draw_specs_panel(self, draw):
        """
        Рисует панель с характеристиками
        """
        y_start = 770
        x_margin = 40
        
        specs = self.build.get_specs_list()
        font_label = self.get_font(20, bold=True)
        font_value = self.get_font(22)
        
        for i, (label, value) in enumerate(specs[:4]):  # Показываем только 4 основные
            y_pos = y_start + i * 60
            
            # Рисуем иконку/label
            draw.text((x_margin, y_pos), label, fill=self.MSI_RED, font=font_label)
            
            # Значение
            draw.text((x_margin + 200, y_pos), value, fill=self.MSI_LIGHT_GRAY, font=font_value)
    
    def _draw_price(self, draw):
        """
        Рисует цену - самый заметный элемент
        """
        price_text = self.format_price(self.build.price)
        font = self.get_font(72, bold=True)
        
        # Позиция в правом нижнем углу
        bbox = draw.textbbox((0, 0), price_text, font=font)
        text_width = bbox[2] - bbox[0]
        
        x = self.width - text_width - 40
        y = self.height - 120
        
        # Подложка
        padding = 20
        self.draw_rounded_rectangle(
            draw,
            [x - padding, y - padding, x + text_width + padding, y + 80 + padding],
            radius=15,
            fill=(227, 6, 19, 255)
        )
        
        # Текст цены белым
        draw.text((x, y), price_text, fill=(255, 255, 255), font=font)
    
    def _draw_bonuses(self, draw):
        """
        Рисует бонусы
        """
        font = self.get_font(18, bold=True)
        
        bonuses_lines = self.build.bonuses.split('\n')[:2]  # Максимум 2 строки
        y_start = self.height - 200
        
        for i, line in enumerate(bonuses_lines):
            y = y_start + i * 30
            # Рисуем с иконкой подарка
            draw.text((40, y), f"🎁 {line}", fill=(255, 215, 0), font=font)
