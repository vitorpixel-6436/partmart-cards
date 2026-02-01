from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
from .base_generator import BaseCardGenerator


class AppleStyleGenerator(BaseCardGenerator):
    """
    🍎 Apple Premium Style - минималистичный liquid glass дизайн
    """
    
    # Apple цветовая палитра
    APPLE_WHITE = (255, 255, 255)
    APPLE_LIGHT_GRAY = (242, 242, 247)
    APPLE_GRAY = (142, 142, 147)
    APPLE_DARK = (28, 28, 30)
    APPLE_BLUE = (0, 122, 255)
    APPLE_GREEN = (52, 199, 89)
    
    def generate(self):
        """
        Генерирует карточку в стиле Apple Premium
        """
        # Чистый белый фон с легким градиентом
        card = self.create_gradient(
            direction='vertical',
            colors=[self.APPLE_WHITE, self.APPLE_LIGHT_GRAY]
        )
        
        # Загружаем фото ПК
        photo = self.load_and_prepare_photo((900, 700))
        
        # Применяем легкую тень для глубины
        photo_with_shadow = self._add_shadow(photo)
        
        # Размещаем фото в верхней части
        x_offset = (self.width - photo.width) // 2
        y_offset = 100
        
        card_rgba = card.convert('RGBA')
        card_rgba.paste(photo_with_shadow, (x_offset, y_offset), photo_with_shadow)
        card = card_rgba.convert('RGB')
        
        # Рисуем элементы
        draw = ImageDraw.Draw(card, 'RGBA')
        
        # Логотип ПАРТМАРТ
        self._draw_logo(draw)
        
        # Liquid glass панель с характеристиками
        self._draw_specs_liquid_panel(draw)
        
        # Цена в минималистичном стиле
        self._draw_price(draw)
        
        # Бонусы если есть
        if self.build.bonuses:
            self._draw_bonuses(draw)
        
        return card
    
    def _add_shadow(self, img):
        """
        Добавляет мягкую тень к изображению
        """
        # Создаем увеличенный холст для тени
        shadow_size = 30
        new_size = (img.width + shadow_size * 2, img.height + shadow_size * 2)
        
        # Создаем тень
        shadow = Image.new('RGBA', new_size, (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        
        # Рисуем размытую тень
        for i in range(shadow_size):
            alpha = int(20 * (1 - i / shadow_size))
            shadow_draw.rectangle(
                [shadow_size - i, shadow_size - i,
                 new_size[0] - shadow_size + i, new_size[1] - shadow_size + i],
                outline=(0, 0, 0, alpha)
            )
        
        # Размываем тень
        shadow = shadow.filter(ImageFilter.GaussianBlur(15))
        
        # Накладываем оригинальное изображение
        img_rgba = img.convert('RGBA')
        shadow.paste(img_rgba, (shadow_size, shadow_size))
        
        return shadow
    
    def _draw_logo(self, draw):
        """
        Рисует логотип ПАРТМАРТ в Apple стиле
        """
        font = self.get_font(38, bold=True)
        text = "ПАРТМАРТ"
        
        # Позиция в центре вверху
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        
        x = (self.width - text_width) // 2
        y = 30
        
        # Минималистичная подложка
        padding = 12
        self.draw_rounded_rectangle(
            draw,
            [x - padding, y - padding,
             x + text_width + padding, y + 40 + padding],
            radius=20,
            fill=(255, 255, 255, 200),
            outline=self.APPLE_GRAY,
            width=1
        )
        
        # Текст темно-серым
        draw.text((x, y), text, fill=self.APPLE_DARK, font=font)
    
    def _draw_specs_liquid_panel(self, draw):
        """
        Рисует liquid glass панель с характеристиками
        """
        specs = self.build.get_specs_list()
        
        # Центральная liquid glass панель
        panel_width = 1000
        panel_height = 180
        panel_x = (self.width - panel_width) // 2
        panel_y = 830
        
        # Liquid glass эффект - полупрозрачная белая панель
        self.draw_rounded_rectangle(
            draw,
            [panel_x, panel_y, panel_x + panel_width, panel_y + panel_height],
            radius=25,
            fill=(255, 255, 255, 220),
            outline=self.APPLE_GRAY,
            width=1
        )
        
        # Размещаем характеристики в 2 ряда по 2 колонки
        font_label = self.get_font(16, bold=True)
        font_value = self.get_font(18)
        
        col_width = panel_width // 2
        
        for i, (label, value) in enumerate(specs[:4]):
            col = i % 2
            row = i // 2
            
            x = panel_x + 40 + col * col_width
            y = panel_y + 30 + row * 70
            
            # Label серым
            draw.text((x, y), label, fill=self.APPLE_GRAY, font=font_label)
            
            # Value темным
            draw.text((x, y + 25), value, fill=self.APPLE_DARK, font=font_value)
    
    def _draw_price(self, draw):
        """
        Рисует цену в минималистичном Apple стиле
        """
        price_text = self.format_price(self.build.price)
        font = self.get_font(68, bold=True)
        
        # Центрируем внизу
        bbox = draw.textbbox((0, 0), price_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (self.width - text_width) // 2
        y = 1060
        
        # Чистая подложка с акцентным цветом
        padding = 20
        self.draw_rounded_rectangle(
            draw,
            [x - padding, y - padding,
             x + text_width + padding, y + text_height + padding + 15],
            radius=22,
            fill=(0, 122, 255, 255)  # Apple Blue
        )
        
        # Белый текст цены
        draw.text((x, y), price_text, fill=self.APPLE_WHITE, font=font)
    
    def _draw_bonuses(self, draw):
        """
        Рисует бонусы в минималистичном стиле
        """
        font = self.get_font(15, bold=True)
        
        bonuses_lines = self.build.bonuses.split('\n')[:2]
        y_start = 1020
        
        for i, line in enumerate(bonuses_lines):
            y = y_start + i * 28
            
            bbox = draw.textbbox((0, 0), f"✓ {line}", font=font)
            text_width = bbox[2] - bbox[0]
            
            x = (self.width - text_width) // 2
            
            # Минималистичная подложка
            padding = 8
            self.draw_rounded_rectangle(
                draw,
                [x - padding, y - padding,
                 x + text_width + padding, y + 20 + padding],
                radius=12,
                fill=(52, 199, 89, 40)  # Apple Green с прозрачностью
            )
            
            draw.text((x, y), f"✓ {line}", fill=self.APPLE_GREEN, font=font)
