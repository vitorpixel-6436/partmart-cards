from PIL import Image, ImageDraw, ImageFilter
from .base import BaseCardGenerator


class SteamStyleGenerator(BaseCardGenerator):
    """
    Генератор карточек в стиле Steam Library
    Glass morphism эффекты и игровая эстетика
    """
    
    def generate(self):
        # Загружаем шрифты
        self.load_fonts()
        
        # Загружаем фото ПК и делаем фоном
        pc_photo = self.load_and_resize_photo((1200, 1200))
        
        # Применяем blur к фону
        background = pc_photo.filter(ImageFilter.GaussianBlur(radius=15))
        
        # Добавляем темный оверлей
        overlay = Image.new('RGBA', background.size, (10, 15, 25, 180))
        background_rgba = background.convert('RGBA')
        background = Image.alpha_composite(background_rgba, overlay)
        
        canvas = background.convert('RGB')
        draw = ImageDraw.Draw(canvas, 'RGBA')
        
        # Логотип ПАРТМАРТ (верхний центр)
        draw.rectangle([450, 40, 750, 110], fill=(25, 35, 50, 200))
        draw.text((600, 75), '🔧 ПАРТМАРТ', font=self.fonts['medium'], fill='white', anchor='mm')
        
        # Центральная карточка с фото (frosted glass)
        photo_card_y = 150
        draw.rounded_rectangle([100, photo_card_y, 1100, photo_card_y + 450], radius=20, fill=(15, 20, 35, 200))
        
        # Фото ПК в центре карточки
        pc_photo_small = self.load_and_resize_photo((900, 400))
        canvas.paste(pc_photo_small, (150, photo_card_y + 25))
        
        # Нижняя панель с характеристиками (glass morphism)
        specs_y = 650
        draw.rounded_rectangle([100, specs_y, 1100, specs_y + 400], radius=20, fill=(25, 35, 50, 220))
        
        # Характеристики в карточках
        specs = [
            ('💻 Процессор', self.pc_build.cpu, 140, specs_y + 50),
            ('🎮 Видеокарта', self.pc_build.gpu, 140, specs_y + 120),
            ('💾 ОЗУ', self.pc_build.ram, 140, specs_y + 190),
            ('💿 Накопитель', self.pc_build.storage, 140, specs_y + 260),
        ]
        
        for label, value, x, y in specs:
            # Мини-карточка для каждой характеристики
            draw.rounded_rectangle([x, y, 1060, y + 50], radius=10, fill=(40, 55, 75, 180))
            draw.text((x + 20, y + 25), f'{label}: {value}', font=self.fonts['small'], fill='white', anchor='lm')
        
        # Блок с ценой (крупно, в стиле Steam)
        price_text = f"{int(self.pc_build.price):,} ₽".replace(',', ' ')
        draw.rounded_rectangle([140, specs_y + 330, 500, specs_y + 390], radius=10, fill=(66, 133, 244, 255))
        draw.text((320, specs_y + 360), price_text, font=self.fonts['large'], fill='white', anchor='mm')
        
        # Бонусы (если есть)
        if self.pc_build.bonuses:
            draw.text((550, specs_y + 345), f'✨ {self.pc_build.bonuses[:50]}', font=self.fonts['tiny'], fill='#90CAF9')
        
        # Сохраняем
        return self.save_card(canvas)
