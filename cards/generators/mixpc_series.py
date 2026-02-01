from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from .base_generator import BaseCardGenerator
import os


class MIXPCSeriesGenerator(BaseCardGenerator):
    """
    Генератор серии карточек в стиле MIXPC для Авито
    Создаёт 6-7 карточек для одного объявления
    """
    
    # MIXPC фирменные цвета
    MIXPC_PURPLE = (139, 69, 255)
    MIXPC_PINK = (255, 105, 180)
    MIXPC_BLUE = (0, 122, 255)
    MIXPC_DARK = (20, 20, 30)
    MIXPC_WHITE = (255, 255, 255)
    
    def generate(self):
        """
        Генерирует главную карточку (первую в серии)
        """
        return self.generate_main_card()
    
    def generate_series(self):
        """
        Генерирует полную серию из 6 карточек
        """
        cards = []
        
        # 1. Главная карточка с фото ПК
        cards.append(self.generate_main_card())
        
        # 2. Конфигурация (таблица)
        cards.append(self.generate_config_card())
        
        # 3. Тесты в играх
        cards.append(self.generate_gaming_tests())
        
        # 4. Тестирование перед отправкой
        cards.append(self.generate_testing_card())
        
        # 5. Бесплатная доставка
        cards.append(self.generate_delivery_card())
        
        # 6. Трейд-ин / Промо
        cards.append(self.generate_promo_card())
        
        return cards
    
    def generate_main_card(self):
        """
        1️⃣ ИГРОВОЙ КОМПЬЮТЕР - главная карточка
        """
        # Создаём градиентный фон (фиолетово-розовый)
        card = self._create_gradient_background()
        
        # Загружаем и размещаем фото ПК
        photo = self.load_and_prepare_photo((900, 700))
        
        # Создаём 3D эффект с тенью
        photo_3d = self._add_3d_effect(photo)
        
        # Размещаем по центру
        x_offset = (self.width - photo_3d.width) // 2
        y_offset = 250
        
        card_rgba = card.convert('RGBA')
        card_rgba.paste(photo_3d, (x_offset, y_offset), photo_3d)
        card = card_rgba.convert('RGB')
        
        draw = ImageDraw.Draw(card, 'RGBA')
        
        # Заголовок "ИГРОВОЙ КОМПЬЮТЕР"
        self._draw_main_title(draw)
        
        # Характеристики (CPU + GPU)
        self._draw_main_specs(draw)
        
        # Логотип ПАРТМАРТ (вместо MIXPC)
        self._draw_logo_badge(draw)
        
        # 3D игровые элементы (геймпад, джойстик)
        self._draw_3d_gaming_elements(draw)
        
        # Гарантия
        self._draw_warranty_badge(draw)
        
        return card
    
    def generate_config_card(self):
        """
        2️⃣ КОНФИГУРАЦИЯ - таблица характеристик
        """
        card = self._create_gradient_background()
        draw = ImageDraw.Draw(card, 'RGBA')
        
        # Заголовок
        font_title = self.get_font(56, bold=True)
        title = "КОНФИГУРАЦИЯ"
        bbox = draw.textbbox((0, 0), title, font=font_title)
        title_width = bbox[2] - bbox[0]
        x = (self.width - title_width) // 2
        
        # Белый текст с тенью
        draw.text((x + 3, 63), title, fill=(0, 0, 0, 100), font=font_title)
        draw.text((x, 60), title, fill=self.MIXPC_WHITE, font=font_title)
        
        # Подзаголовок
        font_sub = self.get_font(24)
        subtitle = "ТОЛЬКО НОВОЕ ЖЕЛЕЗО"
        bbox_sub = draw.textbbox((0, 0), subtitle, font=font_sub)
        sub_width = bbox_sub[2] - bbox_sub[0]
        x_sub = (self.width - sub_width) // 2
        draw.text((x_sub, 130), subtitle, fill=(200, 200, 200), font=font_sub)
        
        # Таблица конфигурации
        self._draw_config_table(draw)
        
        # 3D элементы украшения
        self._draw_3d_decorations(draw)
        
        return card
    
    def generate_gaming_tests(self):
        """
        3️⃣ ТЕСТЫ В ИГРАХ - FPS показатели
        """
        card = self._create_gradient_background()
        draw = ImageDraw.Draw(card, 'RGBA')
        
        # Заголовок
        font_title = self.get_font(56, bold=True)
        title = "ТЕСТЫ В ИГРАХ"
        bbox = draw.textbbox((0, 0), title, font=font_title)
        title_width = bbox[2] - bbox[0]
        x = (self.width - title_width) // 2
        draw.text((x, 60), title, fill=self.MIXPC_WHITE, font=font_title)
        
        # Подзаголовок
        font_sub = self.get_font(22)
        subtitle = "КОМФОРТНЫЕ ПОКАЗАТЕЛИ"
        bbox_sub = draw.textbbox((0, 0), subtitle, font=font_sub)
        sub_width = bbox_sub[2] - bbox_sub[0]
        draw.text(((self.width - sub_width) // 2, 130), subtitle, fill=(200, 200, 200), font=font_sub)
        
        # Список игр с FPS
        self._draw_fps_list(draw)
        
        # 3D геймпад
        self._draw_3d_gamepad(draw)
        
        return card
    
    def generate_testing_card(self):
        """
        4️⃣ ТЕСТИРУЕМ ПЕРЕД ОТПРАВКОЙ
        """
        card = self._create_gradient_background()
        
        # Фото ПК с экранами тестирования
        photo = self.load_and_prepare_photo((800, 600))
        
        # Добавляем мониторы с тестами (симуляция)
        photo_with_tests = self._add_test_screens_overlay(photo)
        
        x_offset = (self.width - photo_with_tests.width) // 2
        y_offset = 350
        
        card_rgba = card.convert('RGBA')
        card_rgba.paste(photo_with_tests, (x_offset, y_offset), photo_with_tests)
        card = card_rgba.convert('RGB')
        
        draw = ImageDraw.Draw(card, 'RGBA')
        
        # Заголовок
        font_title = self.get_font(56, bold=True)
        title = "ТЕСТИРУЕМ"
        bbox = draw.textbbox((0, 0), title, font=font_title)
        title_width = bbox[2] - bbox[0]
        draw.text(((self.width - title_width) // 2, 60), title, fill=self.MIXPC_WHITE, font=font_title)
        
        font_sub = self.get_font(28)
        subtitle = "ПЕРЕД ОТПРАВКОЙ"
        bbox_sub = draw.textbbox((0, 0), subtitle, font=font_sub)
        sub_width = bbox_sub[2] - bbox_sub[0]
        draw.text(((self.width - sub_width) // 2, 130), subtitle, fill=(200, 200, 200), font=font_sub)
        
        return card
    
    def generate_delivery_card(self):
        """
        5️⃣ БЕСПЛАТНАЯ ДОСТАВКА ПО РОССИИ
        """
        card = self._create_gradient_background()
        draw = ImageDraw.Draw(card, 'RGBA')
        
        # Заголовок "БЕСПЛАТНАЯ"
        font_huge = self.get_font(64, bold=True)
        title1 = "БЕСПЛАТНАЯ"
        bbox1 = draw.textbbox((0, 0), title1, font=font_huge)
        width1 = bbox1[2] - bbox1[0]
        draw.text(((self.width - width1) // 2, 180), title1, fill=self.MIXPC_WHITE, font=font_huge)
        
        # "ДОСТАВКА ПО РОССИИ"
        font_sub = self.get_font(32)
        title2 = "ДОСТАВКА ПО РОССИИ"
        bbox2 = draw.textbbox((0, 0), title2, font=font_sub)
        width2 = bbox2[2] - bbox2[0]
        draw.text(((self.width - width2) // 2, 260), title2, fill=(200, 200, 200), font=font_sub)
        
        # 3D коробка с упаковкой
        self._draw_3d_package_box(draw)
        
        # Галочка "НАДЁЖНАЯ УПАКОВКА"
        self._draw_checkmark_badge(draw)
        
        # 3D грузовик
        self._draw_3d_truck(draw)
        
        return card
    
    def generate_promo_card(self):
        """
        6️⃣ ТРЕЙД-ИН / СКИДКА
        """
        card = self._create_gradient_background()
        draw = ImageDraw.Draw(card, 'RGBA')
        
        # Заголовок
        font_huge = self.get_font(64, bold=True)
        title = "ТРЕЙД-ИН"
        bbox = draw.textbbox((0, 0), title, font=font_huge)
        title_width = bbox[2] - bbox[0]
        draw.text(((self.width - title_width) // 2, 180), title, fill=self.MIXPC_WHITE, font=font_huge)
        
        # Скидка
        font_discount = self.get_font(48)
        discount = "СКИДКА ДО 50%"
        bbox_d = draw.textbbox((0, 0), discount, font=font_discount)
        width_d = bbox_d[2] - bbox_d[0]
        draw.text(((self.width - width_d) // 2, 260), discount, fill=self.MIXPC_PINK, font=font_discount)
        
        # 3D элементы (старый ПК, новый ПК, стрелки)
        self._draw_trade_in_illustration(draw)
        
        return card
    
    # === Вспомогательные методы ===
    
    def _create_gradient_background(self):
        """
        Создаёт градиентный фон в стиле MIXPC (фиолетово-розовый)
        """
        img = Image.new('RGB', self.CARD_SIZE, self.MIXPC_DARK)
        draw = ImageDraw.Draw(img)
        
        # Радиальный градиент
        for i in range(self.height):
            ratio = i / self.height
            # От фиолетового к розовому
            r = int(139 + (255 - 139) * ratio * 0.6)
            g = int(69 + (105 - 69) * ratio * 0.8)
            b = int(255 - (255 - 180) * ratio * 0.7)
            draw.line([(0, i), (self.width, i)], fill=(r, g, b))
        
        return img
    
    def _add_3d_effect(self, img):
        """
        Добавляет 3D эффект с тенью и глубиной
        """
        # Увеличиваем холст для тени
        shadow_offset = 40
        new_size = (img.width + shadow_offset * 2, img.height + shadow_offset * 2)
        
        result = Image.new('RGBA', new_size, (0, 0, 0, 0))
        
        # Создаём мягкую тень
        shadow = Image.new('RGBA', new_size, (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        
        for i in range(shadow_offset):
            alpha = int(80 * (1 - i / shadow_offset))
            shadow_draw.rectangle(
                [shadow_offset - i + 10, shadow_offset - i + 10,
                 new_size[0] - shadow_offset + i + 10, new_size[1] - shadow_offset + i + 10],
                outline=(0, 0, 0, alpha)
            )
        
        shadow = shadow.filter(ImageFilter.GaussianBlur(20))
        
        # Накладываем оригинал
        img_rgba = img.convert('RGBA')
        result = Image.alpha_composite(result, shadow)
        result.paste(img_rgba, (shadow_offset, shadow_offset))
        
        return result
    
    def _draw_main_title(self, draw):
        """Рисует заголовок главной карточки"""
        font_huge = self.get_font(64, bold=True)
        
        # "ИГРОВОЙ"
        title1 = "ИГРОВОЙ"
        bbox1 = draw.textbbox((0, 0), title1, font=font_huge)
        width1 = bbox1[2] - bbox1[0]
        x1 = (self.width - width1) // 2
        
        # Тень
        draw.text((x1 + 4, 64), title1, fill=(0, 0, 0, 150), font=font_huge)
        # Основной текст
        draw.text((x1, 60), title1, fill=self.MIXPC_WHITE, font=font_huge)
        
        # "КОМПЬЮТЕР"
        font_big = self.get_font(56, bold=True)
        title2 = "КОМПЬЮТЕР"
        bbox2 = draw.textbbox((0, 0), title2, font=font_big)
        width2 = bbox2[2] - bbox2[0]
        x2 = (self.width - width2) // 2
        
        draw.text((x2 + 3, 143), title2, fill=(0, 0, 0, 100), font=font_big)
        draw.text((x2, 140), title2, fill=self.MIXPC_WHITE, font=font_big)
    
    def _draw_main_specs(self, draw):
        """Рисует основные характеристики (CPU + GPU)"""
        font_spec = self.get_font(28, bold=True)
        
        specs_text = f"{self.build.cpu} + {self.build.gpu}"
        bbox = draw.textbbox((0, 0), specs_text, font=font_spec)
        text_width = bbox[2] - bbox[0]
        
        x = (self.width - text_width) // 2
        y = 1020
        
        # Подложка
        padding = 20
        self.draw_rounded_rectangle(
            draw,
            [x - padding, y - padding,
             x + text_width + padding, y + 40 + padding],
            radius=20,
            fill=(255, 255, 255, 30)
        )
        
        draw.text((x, y), specs_text, fill=self.MIXPC_WHITE, font=font_spec)
    
    def _draw_logo_badge(self, draw):
        """Рисует логотип ПАРТМАРТ в круглом бейдже"""
        # Круглый бейдж в правом верхнем углу
        badge_x = self.width - 150
        badge_y = 50
        badge_radius = 60
        
        # Круг с градиентом
        for r in range(badge_radius, 0, -1):
            alpha = int(200 * (r / badge_radius))
            color = self.MIXPC_PURPLE + (alpha,)
            draw.ellipse(
                [badge_x - r, badge_y - r, badge_x + r, badge_y + r],
                fill=color
            )
        
        # Текст "PM" (ПАРТМАРТ)
        font_logo = self.get_font(32, bold=True)
        logo_text = "PM"
        bbox = draw.textbbox((0, 0), logo_text, font=font_logo)
        logo_width = bbox[2] - bbox[0]
        logo_height = bbox[3] - bbox[1]
        
        draw.text(
            (badge_x - logo_width // 2, badge_y - logo_height // 2),
            logo_text,
            fill=self.MIXPC_WHITE,
            font=font_logo
        )
    
    def _draw_warranty_badge(self, draw):
        """Рисует бейдж с гарантией"""
        x = 80
        y = 1050
        
        # Подложка
        self.draw_rounded_rectangle(
            draw,
            [x, y, x + 200, y + 100],
            radius=15,
            fill=(255, 255, 255, 40)
        )
        
        # Цифра "3"
        font_huge = self.get_font(56, bold=True)
        draw.text((x + 40, y + 5), "3", fill=self.MIXPC_WHITE, font=font_huge)
        
        # "года"
        font_small = self.get_font(20, bold=True)
        draw.text((x + 110, y + 15), "года", fill=self.MIXPC_WHITE, font=font_small)
        
        # "ГАРАНТИИ"
        font_text = self.get_font(16, bold=True)
        draw.text((x + 30, y + 70), "ГАРАНТИИ*", fill=(220, 220, 220), font=font_text)
    
    def _draw_config_table(self, draw):
        """Рисует таблицу конфигурации"""
        specs = self.build.get_specs_list()
        
        # Иконки для компонентов
        icons = {
            'Процессор': '🖥',
            'Видеокарта': '🎮',
            'Оперативка': '💾',
            'Накопитель': '💿',
            'Мат. плата': '🔌',
            'Блок питания': '⚡',
            'Корпус': '📦'
        }
        
        start_y = 220
        row_height = 90
        table_width = 1000
        x_start = (self.width - table_width) // 2
        
        font_label = self.get_font(18, bold=True)
        font_value = self.get_font(22)
        
        for i, (label, value) in enumerate(specs):
            y = start_y + i * row_height
            
            # Строка таблицы
            self.draw_rounded_rectangle(
                draw,
                [x_start, y, x_start + table_width, y + 70],
                radius=12,
                fill=(0, 0, 0, 100)
            )
            
            # Иконка
            draw.text((x_start + 20, y + 15), label.split()[0], fill=self.MIXPC_WHITE, font=self.get_font(32))
            
            # Название компонента
            clean_label = ' '.join(label.split()[1:]) if ' ' in label else label
            draw.text((x_start + 80, y + 10), clean_label, fill=(180, 180, 180), font=font_label)
            
            # Значение
            draw.text((x_start + 350, y + 20), value, fill=self.MIXPC_WHITE, font=font_value)
    
    def _draw_fps_list(self, draw):
        """Рисует список игр с FPS"""
        games = [
            ('CS2', 199),
            ('PUBG: BATTLEGROUNDS', 221),
            ('Cyberpunk 2077', 115),
            ('COD: Warzone', 122),
            ('Indiana Jones', 91),
            ('RUST', 113),
            ('DOOM The Dark Ages', 73),
            ('Hogwarts Legacy', 97),
        ]
        
        # Панель с играми
        panel_width = 900
        panel_height = 700
        panel_x = (self.width - panel_width) // 2
        panel_y = 250
        
        # Фон панели
        self.draw_rounded_rectangle(
            draw,
            [panel_x, panel_y, panel_x + panel_width, panel_y + panel_height],
            radius=25,
            fill=(0, 0, 0, 120)
        )
        
        # Список игр
        font_game = self.get_font(22, bold=True)
        font_fps = self.get_font(28, bold=True)
        
        row_height = 75
        for i, (game, fps) in enumerate(games):
            y = panel_y + 40 + i * row_height
            
            # Строка игры
            self.draw_rounded_rectangle(
                draw,
                [panel_x + 30, y, panel_x + panel_width - 30, y + 60],
                radius=15,
                fill=self.MIXPC_PURPLE + (80,)
            )
            
            # Иконка игры (квадрат)
            icon_size = 45
            draw.rectangle(
                [panel_x + 45, y + 7, panel_x + 45 + icon_size, y + 7 + icon_size],
                fill=(50, 50, 60)
            )
            
            # Название игры
            draw.text((panel_x + 110, y + 15), game, fill=self.MIXPC_WHITE, font=font_game)
            
            # FPS
            fps_text = f"{fps} FPS"
            bbox = draw.textbbox((0, 0), fps_text, font=font_fps)
            fps_width = bbox[2] - bbox[0]
            draw.text((panel_x + panel_width - 150, y + 12), fps_text, fill=self.MIXPC_PINK, font=font_fps)
    
    def _draw_3d_gaming_elements(self, draw):
        """Рисует 3D игровые элементы (декорация)"""
        # Просто placeholder - можно добавить геймпад, джойстик и т.д.
        pass
    
    def _draw_3d_decorations(self, draw):
        """3D элементы декора"""
        pass
    
    def _draw_3d_gamepad(self, draw):
        """3D геймпад"""
        pass
    
    def _add_test_screens_overlay(self, photo):
        """Добавляет оверлей с экранами тестирования"""
        return photo
    
    def _draw_3d_package_box(self, draw):
        """3D коробка"""
        pass
    
    def _draw_checkmark_badge(self, draw):
        """Бейдж с галочкой"""
        x = (self.width - 400) // 2
        y = 600
        
        # Зелёный круг с галочкой
        circle_radius = 60
        circle_x = x + 200
        circle_y = y - 50
        
        draw.ellipse(
            [circle_x - circle_radius, circle_y - circle_radius,
             circle_x + circle_radius, circle_y + circle_radius],
            fill=(52, 199, 89)
        )
        
        # Галочка
        font_check = self.get_font(48, bold=True)
        draw.text((circle_x - 15, circle_y - 30), "✓", fill=self.MIXPC_WHITE, font=font_check)
        
        # Текст
        font_text = self.get_font(26, bold=True)
        text = "НАДЁЖНАЯ УПАКОВКА"
        bbox = draw.textbbox((0, 0), text, font=font_text)
        text_width = bbox[2] - bbox[0]
        draw.text(((self.width - text_width) // 2, y + 80), text, fill=self.MIXPC_WHITE, font=font_text)
    
    def _draw_3d_truck(self, draw):
        """3D грузовик"""
        pass
    
    def _draw_trade_in_illustration(self, draw):
        """Иллюстрация трейд-ин"""
        pass
