from PIL import Image, ImageDraw, ImageFont
from .base import BaseCardGenerator


class MSIStyleGenerator(BaseCardGenerator):
    """
    Генератор карточек в стиле MSI Gaming
    Агрессивный красно-черный дизайн с диагональными линиями
    """
    
    def generate(self):
        # Загружаем шрифты
        self.load_fonts()
        
        # Создаем черный фон
        canvas = Image.new('RGB', self.canvas_size, color='#0d0d0d')
        draw = ImageDraw.Draw(canvas)
        
        # Загружаем и размещаем фото ПК (верхняя часть)
        pc_photo = self.load_and_resize_photo((1200, 700))
        
        # Добавляем красный градиент оверлей на фото
        overlay = Image.new('RGBA', pc_photo.size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        
        # Градиент от прозрачного к черно-красному
        for y in range(pc_photo.height):
            alpha = int((y / pc_photo.height) * 180)
            red_value = int((y / pc_photo.height) * 50)
            overlay_draw.line([(0, y), (pc_photo.width, y)], fill=(red_value, 0, 0, alpha))
        
        pc_photo_rgba = pc_photo.convert('RGBA')
        pc_photo_with_overlay = Image.alpha_composite(pc_photo_rgba, overlay)
        canvas.paste(pc_photo_with_overlay, (0, 0))
        
        # Диагональные линии MSI-style
        for i in range(0, 1200, 60):
            draw.line([(i, 650), (i + 200, 850)], fill='#cc0000', width=3)
        
        # Логотип ПАРТМАРТ (верхний левый угол)
        draw.rectangle([30, 30, 250, 90], fill='#cc0000')
        draw.text((140, 60), 'ПАРТМАРТ', font=self.fonts['medium'], fill='white', anchor='mm')
        
        # Черная панель с характеристиками
        draw.rectangle([30, 720, 1170, 1050], fill='#1a1a1a', outline='#cc0000', width=3)
        
        # Характеристики в 2 столбца
        specs = [
            (f'🔥 CPU: {self.pc_build.cpu}', 70, 760),
            (f'🎮 GPU: {self.pc_build.gpu}', 70, 820),
            (f'💾 RAM: {self.pc_build.ram}', 70, 880),
            (f'💿 SSD: {self.pc_build.storage}', 70, 940),
        ]
        
        for spec_text, x, y in specs:
            draw.text((x, y), spec_text, font=self.fonts['small'], fill='white')
        
        # Дополнительные характеристики (если есть)
        extra_y = 1000
        if self.pc_build.motherboard:
            draw.text((70, extra_y), f'⚡ MB: {self.pc_build.motherboard}', font=self.fonts['tiny'], fill='#cccccc')
        
        # Цена (крупно и ярко)
        price_text = f"{int(self.pc_build.price):,} ₽".replace(',', ' ')
        draw.rectangle([30, 1070, 550, 1160], fill='#cc0000')
        self.draw_text_with_outline(draw, (290, 1115), price_text, self.fonts['large'], 'white', 'black', 3)
        
        # Бонусы
        if self.pc_build.bonuses:
            bonus_y = 1070
            for line in self.pc_build.bonuses.split('\n')[:2]:  # Макс 2 строки
                draw.text((600, bonus_y), f'⭐ {line}', font=self.fonts['tiny'], fill='#ffcc00')
                bonus_y += 35
        
        # RGB акценты (углы)
        rgb_colors = ['#ff0000', '#00ff00', '#0000ff']
        for i, color in enumerate(rgb_colors):
            x = 1100 + i * 25
            draw.ellipse([x, 1100, x + 20, 1120], fill=color)
        
        # Сохраняем
        return self.save_card(canvas)
