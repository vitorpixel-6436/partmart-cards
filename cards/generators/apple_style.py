from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
from .base_generator import BaseCardGenerator


class AppleStyleGenerator(BaseCardGenerator):
    """
    🍎 Apple Premium Style - минималистичный liquid glass дизайн
    """
    
    # Apple цветовая палитра
    APPLE_WHITE = (255, 255, 255)
    APPLE_LIGHT_GRAY = (242, 242, 247)
    APPLE_GRAY = (174, 174, 178)
    APPLE_DARK = (28, 28, 30)
    APPLE_BLUE = (0, 122, 255)
    APPLE_GREEN = (52, 199, 89)
    
    def generate(self):
        """
        Генерирует карточку в стиле Apple Premium
        """
        # Светлый градиентный фон
        card = self.create_gradient(
            direction='vertical',
            colors=[self.APPLE_WHITE, self.APPLE_LIGHT_GRAY]
        )
        
        # Загружаем фото ПК
        photo = self.load_and_prepare_photo((900, 700))
        
        # Центрируем фото в верхней части
        x_offset = (self.width - photo.width) // 2
        y_offset = 80
        
        # Создаём мягкую тень под фото
        card = self._add_soft_shadow(card, photo, x_offset, y_offset)
        
        # Размещаем фото
        card.paste(photo, (x_offset, y_offset))
        
        # Рисуем элементы поверх
        draw = ImageDraw.Draw(card, 'RGBA')
        
        # Логотип ПАРТМАРТ
        self._draw_logo(draw)
        
        # Минималистичная панель характеристик
        self._draw_specs_minimal(draw)
        
        # Цена в премиум стиле
        self._draw_price_premium(draw)
        
        # Бонусы
        if self.build.bonuses:
            self._draw_bonuses(draw)
        
        return card
    
    def _add_soft_shadow(self, card, photo, x, y):
        """
        Добавляет мягкую тень под фото для объёма
        """
        # Создаём слой тени
        shadow = Image.new('RGBA', card.size, (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        
        # Рисуем размытую тень
        shadow_padding = 40
        shadow_draw.ellipse(
            [x - shadow_padding, y + photo.height - 50,
             x + photo.width + shadow_padding, y + photo.height + 80],
            fill=(0, 0, 0, 40)
        )
        
        # Размываем тень
        shadow = shadow.filter(ImageFilter.GaussianBlur(30))
        
        # Накладываем на карточку
        card_rgba = card.convert('RGBA')
        card_rgba = Image.alpha_composite(card_rgba, shadow)
        
        return card_rgba.convert('RGB')
    
    def _draw_logo(self, draw):
        """
        Рисует логотип ПАРТМАРТ в Apple стиле
        """
        font = self.get_font(38, bold=True)
        text = "ПАРТМАРТ"
        
        # Центрируем вверху
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        x = (self.width - text_width) // 2
        y = 25
        
        # Лёгкая подложка
        padding = 12
        self.draw_rounded_rectangle(
            draw,
            [x - padding, y - padding, 
             x + text_width + padding, bbox[3] + padding],
            radius=10,
            fill=(255, 255, 255, 180)
        )
        
        # Текст серым
        draw.text((x, y), text, fill=self.APPLE_DARK, font=font)
    
    def _draw_specs_minimal(self, draw):
        """
        Рисует характеристики в минималистичном стиле
        """
        specs = self.build.get_specs_list()
        
        # Создаём элегантную карточку по центру
        panel_width = 1000
        panel_height = 220
        panel_x = (self.width - panel_width) // 2
        panel_y = 820
        
        # Liquid glass панель
        self.draw_rounded_rectangle(
            draw,
            [panel_x, panel_y, panel_x + panel_width, panel_y + panel_height],
            radius=25,
            fill=(255, 255, 255, 200),
            outline=self.APPLE_GRAY,
            width=1
        )
        
        # Размещаем характеристики в 2 колонки
        font_label = self.get_font(16)
        font_value = self.get_font(20, bold=True)
        
        col_width = panel_width // 2
        
        for i, (label, value) in enumerate(specs[:4]):
            col = i % 2
            row = i // 2
            
            x = panel_x + 40 + col * col_width
            y = panel_y + 40 + row * 70
            
            # Метка серым
            draw.text((x, y), label, fill=self.APPLE_GRAY, font=font_label)
            # Значение чёрным жирным
            draw.text((x, y + 25), value, fill=self.APPLE_DARK, font=font_value)
    
    def _draw_price_premium(self, draw):
        """
        Рисует цену в премиум стиле Apple
        """
        price_text = self.format_price(self.build.price)
        font = self.get_font(68, bold=True)
        
        bbox = draw.textbbox((0, 0), price_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Центрируем внизу
        x = (self.width - text_width) // 2
        y = 1070
        
        # Элегантная подложка с градиентом (имитация)
        padding = 30
        self.draw_rounded_rectangle(
            draw,
            [x - padding, y - padding,
             x + text_width + padding, y + text_height + padding + 15],
            radius=22,
            fill=(0, 122, 255, 255)  # Apple Blue
        )
        
        # Текст белым
        draw.text((x, y), price_text, fill=self.APPLE_WHITE, font=font)
    
    def _draw_bonuses(self, draw):
        """
        Рисует бонусы в Apple стиле
        """
        font = self.get_font(17)
        
        bonuses_lines = self.build.bonuses.split('\n')[:2]
        y_start = 1010
        
        for i, line in enumerate(bonuses_lines):
            y = y_start + i * 28
            text = f"✓ {line}"
            
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            x = (self.width - text_width) // 2
            
            # Лёгкая подложка
            padding = 10
            self.draw_rounded_rectangle(
                draw,
                [x - padding, bbox[1] + y - padding,
                 x + text_width + padding, bbox[3] + y + padding],
                radius=8,
                fill=(52, 199, 89, 60)  # Apple Green
            )
            
            draw.text((x, y), text, fill=self.APPLE_GREEN, font=font)
