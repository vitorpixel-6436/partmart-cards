from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
from .base_generator import BaseCardGenerator


class SpotifyStyleGenerator(BaseCardGenerator):
    """
    🎵 Spotify Minimal Style - ультра-чистый дизайн
    """
    
    # Spotify цветовая палитра
    SPOTIFY_GREEN = (30, 215, 96)
    SPOTIFY_BLACK = (18, 18, 18)
    SPOTIFY_DARK_GRAY = (40, 40, 40)
    SPOTIFY_LIGHT_GRAY = (179, 179, 179)
    SPOTIFY_WHITE = (255, 255, 255)
    
    def generate(self):
        """
        Генерирует карточку в стиле Spotify Minimal
        """
        # Чистый черный фон
        card = Image.new('RGB', self.CARD_SIZE, self.SPOTIFY_BLACK)
        
        # Загружаем фото ПК
        photo = self.load_and_prepare_photo((950, 750))
        
        # Применяем легкий контраст
        enhancer = ImageEnhance.Contrast(photo)
        photo = enhancer.enhance(1.1)
        
        # Размещаем фото
        x_offset = (self.width - photo.width) // 2
        y_offset = 80
        card.paste(photo, (x_offset, y_offset))
        
        # Рисуем элементы
        draw = ImageDraw.Draw(card, 'RGBA')
        
        # Логотип ПАРТМАРТ
        self._draw_logo(draw)
        
        # Минимум характеристик - только главное
        self._draw_specs_minimal(draw)
        
        # Жирная цена - главный фокус
        self._draw_bold_price(draw)
        
        # Градиентная линия акцента
        self._draw_accent_line(draw)
        
        # Бонусы
        if self.build.bonuses:
            self._draw_bonuses(draw)
        
        return card
    
    def _draw_logo(self, draw):
        """
        Рисует логотип ПАРТМАРТ в Spotify стиле
        """
        font = self.get_font(36, bold=True)
        text = "ПАРТМАРТ"
        
        x = 40
        y = 30
        
        # Зеленый текст как у Spotify
        draw.text((x, y), text, fill=self.SPOTIFY_GREEN, font=font)
    
    def _draw_specs_minimal(self, draw):
        """
        Рисует характеристики в минималистичном стиле
        """
        specs = self.build.get_specs_list()
        
        # Только 4 основные характеристики в одну линию
        y_pos = 870
        
        font_label = self.get_font(14)
        font_value = self.get_font(18, bold=True)
        
        # Распределяем по ширине
        spacing = (self.width - 80) // 4
        
        for i, (label, value) in enumerate(specs[:4]):
            x = 40 + i * spacing
            
            # Удаляем эмодзи из label для чистоты
            clean_label = label.split()[-1] if ' ' in label else label
            
            # Label серым сверху
            draw.text((x, y_pos), clean_label, fill=self.SPOTIFY_LIGHT_GRAY, font=font_label)
            
            # Value белым снизу
            # Сокращаем длинные значения
            short_value = value[:25] + '...' if len(value) > 25 else value
            draw.text((x, y_pos + 20), short_value, fill=self.SPOTIFY_WHITE, font=font_value)
    
    def _draw_bold_price(self, draw):
        """
        Рисует жирную цену - главный элемент
        """
        price_text = self.format_price(self.build.price)
        font = self.get_font(88, bold=True)
        
        # Центрируем
        bbox = draw.textbbox((0, 0), price_text, font=font)
        text_width = bbox[2] - bbox[0]
        
        x = (self.width - text_width) // 2
        y = 970
        
        # Без подложки - чистый текст
        # Рисуем с легкой тенью для глубины
        draw.text((x + 3, y + 3), price_text, fill=self.SPOTIFY_DARK_GRAY, font=font)
        draw.text((x, y), price_text, fill=self.SPOTIFY_WHITE, font=font)
    
    def _draw_accent_line(self, draw):
        """
        Рисует акцентную линию Spotify green
        """
        # Горизонтальная линия под ценой
        y = 1080
        line_width = 400
        x_start = (self.width - line_width) // 2
        
        # Градиент от прозрачного к зеленому и обратно
        for i in range(line_width):
            if i < line_width // 3:
                alpha = int(255 * (i / (line_width // 3)))
            elif i > 2 * line_width // 3:
                alpha = int(255 * ((line_width - i) / (line_width // 3)))
            else:
                alpha = 255
            
            color = self.SPOTIFY_GREEN + (alpha,)
            draw.line([(x_start + i, y), (x_start + i, y + 3)], fill=color, width=3)
    
    def _draw_bonuses(self, draw):
        """
        Рисует бонусы минималистично
        """
        font = self.get_font(16, bold=True)
        
        bonuses_lines = self.build.bonuses.split('\n')[:2]
        
        # Размещаем под линией
        y_start = 1100
        
        for i, line in enumerate(bonuses_lines):
            y = y_start + i * 25
            
            bbox = draw.textbbox((0, 0), f"• {line}", font=font)
            text_width = bbox[2] - bbox[0]
            
            x = (self.width - text_width) // 2
            
            # Просто зеленый текст без подложки
            draw.text((x, y), f"• {line}", fill=self.SPOTIFY_GREEN, font=font)
