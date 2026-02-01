from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
from .base_generator import BaseCardGenerator


class SpotifyStyleGenerator(BaseCardGenerator):
    """
    🎵 Spotify Minimal Style - ультра-чистый дизайн
    """
    
    # Spotify цветовая палитра
    SPOTIFY_BLACK = (18, 18, 18)
    SPOTIFY_GREEN = (29, 185, 84)
    SPOTIFY_WHITE = (255, 255, 255)
    SPOTIFY_GRAY = (179, 179, 179)
    SPOTIFY_DARK_GRAY = (40, 40, 40)
    
    def generate(self):
        """
        Генерирует карточку в стиле Spotify Minimal
        """
        # Чистый чёрный фон
        card = Image.new('RGB', self.CARD_SIZE, self.SPOTIFY_BLACK)
        
        # Загружаем фото ПК
        photo = self.load_and_prepare_photo((1000, 750))
        
        # Увеличиваем контраст фото для драматичности
        enhancer = ImageEnhance.Contrast(photo)
        photo = enhancer.enhance(1.2)
        
        # Размещаем фото по центру верхней части
        x_offset = (self.width - photo.width) // 2
        y_offset = 60
        
        card.paste(photo, (x_offset, y_offset))
        
        # Рисуем элементы
        draw = ImageDraw.Draw(card, 'RGBA')
        
        # Минималистичный логотип
        self._draw_logo(draw)
        
        # Ультра-простые характеристики
        self._draw_specs_ultra_minimal(draw)
        
        # Огромная яркая цена
        self._draw_price_bold(draw)
        
        # Spotify accent линия
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
        
        x = 50
        y = 30
        
        # Просто текст, никаких подложек - максимальная простота
        draw.text((x, y), text, fill=self.SPOTIFY_GREEN, font=font)
    
    def _draw_specs_ultra_minimal(self, draw):
        """
        Рисует характеристики в ультра-минималистичном стиле
        """
        specs = self.build.get_specs_list()
        
        # Просто список без рамок и подложек
        y_start = 850
        x_start = 50
        
        font_value = self.get_font(24, bold=True)
        
        for i, (label, value) in enumerate(specs[:4]):
            y = y_start + i * 50
            
            # Только значения, без иконок - чистота
            # Убираем эмодзи из label
            clean_label = label.split(' ', 1)[-1] if ' ' in label else label
            
            # Значение белым
            draw.text((x_start, y), value, fill=self.SPOTIFY_WHITE, font=font_value)
    
    def _draw_price_bold(self, draw):
        """
        Рисует цену огромным жирным шрифтом
        """
        price_text = self.format_price(self.build.price)
        font = self.get_font(80, bold=True)
        
        # Правый нижний угол
        bbox = draw.textbbox((0, 0), price_text, font=font)
        text_width = bbox[2] - bbox[0]
        
        x = self.width - text_width - 50
        y = self.height - 130
        
        # Подложка минимальная
        padding = 20
        self.draw_rounded_rectangle(
            draw,
            [x - padding, y - padding,
             x + text_width + padding, y + 90 + padding],
            radius=15,
            fill=self.SPOTIFY_DARK_GRAY
        )
        
        # Цена зелёным
        draw.text((x, y), price_text, fill=self.SPOTIFY_GREEN, font=font)
    
    def _draw_accent_line(self, draw):
        """
        Рисует Spotify accent линию
        """
        # Тонкая зелёная линия для акцента
        y_pos = 830
        draw.rectangle([50, y_pos, self.width - 50, y_pos + 3], 
                      fill=self.SPOTIFY_GREEN)
    
    def _draw_bonuses(self, draw):
        """
        Рисует бонусы в Spotify стиле
        """
        font = self.get_font(18, bold=True)
        
        bonuses_lines = self.build.bonuses.split('\n')[:2]
        y_start = self.height - 200
        
        for i, line in enumerate(bonuses_lines):
            y = y_start + i * 30
            
            # Простой текст с точкой
            draw.text((50, y), f"• {line}", fill=self.SPOTIFY_GRAY, font=font)
