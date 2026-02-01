from PIL import Image
import os
from django.conf import settings
from .msi_style import MSIStyleGenerator
from .steam_style import SteamStyleGenerator
from .apple_style import AppleStyleGenerator
from .spotify_style import SpotifyStyleGenerator


class CardGenerator:
    """
    Главный класс для генерации карточек в разных стилях
    """
    
    GENERATORS = {
        'msi': MSIStyleGenerator,
        'steam': SteamStyleGenerator,
        'apple': AppleStyleGenerator,
        'spotify': SpotifyStyleGenerator,
    }
    
    def __init__(self, pc_build):
        self.build = pc_build
        self.style = pc_build.style
        
    def generate(self):
        """
        Генерирует карточку выбранного стиля
        """
        generator_class = self.GENERATORS.get(self.style)
        if not generator_class:
            raise ValueError(f"Неизвестный стиль: {self.style}")
        
        generator = generator_class(self.build)
        output_path = self._get_output_path()
        
        # Генерируем изображение
        img = generator.generate()
        
        # Сохраняем
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        img.save(output_path, 'PNG', quality=95, optimize=True)
        
        # Возвращаем относительный путь для Django
        return os.path.relpath(output_path, settings.MEDIA_ROOT)
    
    def _get_output_path(self):
        """
        Генерирует путь для сохранения карточки
        """
        filename = f"partmart_{self.build.pk}_{self.style}.png"
        return os.path.join(settings.MEDIA_ROOT, 'generated', filename)
