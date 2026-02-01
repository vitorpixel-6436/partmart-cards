from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
from .base_generator import BaseCardGenerator


class SteamStyleGenerator(BaseCardGenerator):
    """
    🎮 Steam Library Style - glass morphism эффекты
    """
    
    # Steam цветовая палитра
    STEAM_DARK_BLUE = (27, 40, 56)
    STEAM_BLUE = (102, 192, 244)
    STEAM_LIGHT = (193, 207, 217)
    STEAM_GLASS = (255, 255, 255, 40)  # Полупрозрачный белый
    
    def generate(self):
        """
        Генерирует карточку в стиле Steam Library
        """
        # Создаем базовый градиентный фон
        card = self.create_gradient(
            direction='diagonal',
            colors=[self.STEAM_DARK_BLUE, (15, 25, 35)]
        )
        
        # Загружаем фото ПК
        photo = self.load_and_prepare_photo((1000, 800))
        
        # Применяем размытие к фото для фона
        photo_blur = photo.filter(ImageFilter.GaussianBlur(15))
        
        # Затемняем размытое фото
        enhancer = ImageEnhance.Brightness(photo_blur)
        photo_blur = enhancer.enhance(0.4)
        
        # Размещаем размытое фото как фон
        card_rgba = card.convert('RGBA')
        photo_blur_rgba = photo_blur.convert('RGBA')
        
        # Центрируем фото
        x_offset = (self.width - photo_blur.width) // 2
        y_offset = 50
        
        # Создаем маску для плавного перехода
        mask = Image.new('L', photo_blur.size, 200)
        card_rgba.paste(photo_blur_rgba, (x_offset, y_offset), mask)
        
        card = card_rgba.convert('RGB')
        
        # Рисуем элементы поверх
        draw = ImageDraw.Draw(card, 'RGBA')
        
        # Логотип ПАРТМАРТ
        self._draw_logo(draw)
        
        # Главная карточка с фото в центре
        self._draw_main_card(card, photo, x_offset, y_offset)
        
        # Glass панели с характеристиками
        draw = ImageDraw.Draw(card, 'RGBA')
        self._draw_specs_glass_panels(draw)
        
        # Цена в glass контейнере
        self._draw_price_panel(draw)
        
        # Бонусы
        if self.build.bonuses:
            self._draw_bonuses(draw)
        
        return card
    
    def _draw_logo(self, draw):
        """
        Рисует логотип ПАРТМАРТ
        """
        font = self.get_font(42, bold=True)
        text = "ПАРТМАРТ"
        
        x = 40
        y = 30
        
        # Glass подложка
        bbox = draw.textbbox((x, y), text, font=font)
        padding = 15
        self.draw_rounded_rectangle(
            draw,
            [bbox[0] - padding, bbox[1] - padding, 
             bbox[2] + padding, bbox[3] + padding],
            radius=12,
            fill=self.STEAM_GLASS
        )
        
        # Текст
        draw.text((x, y), text, fill=self.STEAM_BLUE, font=font)
    
    def _draw_main_card(self, card, photo, x_offset, y_offset):
        """
        Рисует главную карточку с фото
        """
        # Создаем glass эффект для фото
        card_rgba = card.convert('RGBA')
        
        # Рамка вокруг фото
        draw = ImageDraw.Draw(card_rgba, 'RGBA')
        
        border_padding = 20
        self.draw_rounded_rectangle(
            draw,
            [x_offset - border_padding, y_offset - border_padding,
             x_offset + photo.width + border_padding, 
             y_offset + photo.height + border_padding],
            radius=20,
            fill=(255, 255, 255, 30),
            outline=self.STEAM_BLUE,
            width=3
        )
        
        # Вставляем фото
        photo_rgba = photo.convert('RGBA')
        card_rgba.paste(photo_rgba, (x_offset, y_offset))
        
        card.paste(card_rgba.convert('RGB'))
    
    def _draw_specs_glass_panels(self, draw):
        """
        Рисует характеристики в glass панелях
        """
        specs = self.build.get_specs_list()
        
        # Размещаем в 2 колонки по 2 строки
        y_start = 900
        col_width = (self.width - 120) // 2
        
        font_label = self.get_font(18, bold=True)
        font_value = self.get_font(20)
        
        for i, (label, value) in enumerate(specs[:4]):
            col = i % 2
            row = i // 2
            
            x = 40 + col * (col_width + 40)
            y = y_start + row * 90
            
            # Glass панель
            panel_width = col_width
            panel_height = 70
            
            self.draw_rounded_rectangle(
                draw,
                [x, y, x + panel_width, y + panel_height],
                radius=15,
                fill=(255, 255, 255, 35)
            )
            
            # Текст
            draw.text((x + 15, y + 10), label, fill=self.STEAM_BLUE, font=font_label)
            draw.text((x + 15, y + 35), value, fill=self.STEAM_LIGHT, font=font_value)
    
    def _draw_price_panel(self, draw):
        """
        Рисует цену в glass контейнере
        """
        price_text = self.format_price(self.build.price)
        font = self.get_font(64, bold=True)
        
        bbox = draw.textbbox((0, 0), price_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Центрируем внизу
        x = (self.width - text_width) // 2
        y = 1090
        
        # Glass подложка
        padding = 25
        self.draw_rounded_rectangle(
            draw,
            [x - padding, y - padding, 
             x + text_width + padding, y + text_height + padding + 20],
            radius=20,
            fill=(102, 192, 244, 80),
            outline=self.STEAM_BLUE,
            width=3
        )
        
        # Текст цены
        draw.text((x, y), price_text, fill=(255, 255, 255), font=font)
    
    def _draw_bonuses(self, draw):
        """
        Рисует бонусы
        """
        font = self.get_font(16, bold=True)
        
        bonuses_lines = self.build.bonuses.split('\n')[:2]
        y_start = 1020
        
        for i, line in enumerate(bonuses_lines):
            y = y_start + i * 25
            x = 40
            
            # Небольшая glass подложка
            bbox = draw.textbbox((x, y), f"✨ {line}", font=font)
            padding = 10
            
            self.draw_rounded_rectangle(
                draw,
                [bbox[0] - padding, bbox[1] - padding,
                 bbox[2] + padding, bbox[3] + padding],
                radius=8,
                fill=(255, 215, 0, 40)
            )
            
            draw.text((x, y), f"✨ {line}", fill=(255, 215, 0), font=font)
