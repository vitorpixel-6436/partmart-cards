from django.db import models
from django.utils import timezone


class PCBuild(models.Model):
    """
    Модель сборки ПК для генерации карточки продажи
    """
    
    # Фото компьютера
    photo = models.ImageField(
        upload_to='uploads/',
        verbose_name='Фото ПК',
        help_text='Загрузите фотографию собранного компьютера'
    )
    
    # Характеристики компьютера
    cpu = models.CharField(
        max_length=100,
        verbose_name='Процессор',
        help_text='Например: Intel Core i5-12400F'
    )
    
    gpu = models.CharField(
        max_length=100,
        verbose_name='Видеокарта',
        help_text='Например: NVIDIA RTX 3060 Ti 8GB'
    )
    
    ram = models.CharField(
        max_length=50,
        verbose_name='Оперативная память',
        help_text='Например: 16GB DDR4 3200MHz'
    )
    
    storage = models.CharField(
        max_length=100,
        verbose_name='Накопитель',
        help_text='Например: SSD 512GB NVMe + HDD 1TB'
    )
    
    motherboard = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Материнская плата',
        help_text='Например: ASUS B660M-PLUS'
    )
    
    psu = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Блок питания',
        help_text='Например: 650W 80+ Bronze'
    )
    
    case = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Корпус',
        help_text='Например: DeepCool CC560 RGB'
    )
    
    # Цена и бонусы
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена (руб)',
        help_text='Цена в рублях'
    )
    
    bonuses = models.TextField(
        blank=True,
        verbose_name='Бонусы',
        help_text='Например: Windows 11 Pro + Microsoft Office в подарок!'
    )
    
    # Стиль карточки
    STYLE_CHOICES = [
        ('msi', 'MSI Gaming'),
        ('steam', 'Steam Library'),
        ('apple', 'Apple Premium'),
        ('spotify', 'Spotify Minimal'),
    ]
    
    style = models.CharField(
        max_length=20,
        choices=STYLE_CHOICES,
        default='msi',
        verbose_name='Стиль карточки',
        help_text='Выберите стиль дизайна карточки'
    )
    
    # Сгенерированная карточка
    generated_card = models.ImageField(
        upload_to='generated/',
        blank=True,
        null=True,
        verbose_name='Готовая карточка',
        help_text='Автоматически сгенерированное изображение'
    )
    
    # Метаданные
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    
    class Meta:
        verbose_name = 'Сборка ПК'
        verbose_name_plural = 'Сборки ПК'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.cpu} + {self.gpu} - {self.price}₽"
    
    def get_style_display_verbose(self):
        """Получить человекочитаемое название стиля"""
        return dict(self.STYLE_CHOICES).get(self.style, self.style)


class PCBuildPreset(models.Model):
    """
    Пресеты (шаблоны) для быстрого создания конфигураций
    """
    name = models.CharField(
        max_length=100,
        verbose_name='Название пресета',
        help_text='Например: Игровой бюджетный'
    )
    
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
        help_text='Краткое описание конфигурации'
    )
    
    # Характеристики (аналогично PCBuild)
    cpu = models.CharField(max_length=100, verbose_name='Процессор')
    gpu = models.CharField(max_length=100, verbose_name='Видеокарта')
    ram = models.CharField(max_length=50, verbose_name='ОЗУ')
    storage = models.CharField(max_length=100, verbose_name='Накопитель')
    motherboard = models.CharField(max_length=100, blank=True, verbose_name='Мат. плата')
    psu = models.CharField(max_length=100, blank=True, verbose_name='БП')
    case = models.CharField(max_length=100, blank=True, verbose_name='Корпус')
    
    bonuses = models.TextField(blank=True, verbose_name='Бонусы')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Пресет сборки'
        verbose_name_plural = 'Пресеты сборок'
        ordering = ['name']
    
    def __str__(self):
        return self.name
