from django.db import models
from django.core.validators import MinValueValidator
import os


class PCBuild(models.Model):
    """
    Модель сборки компьютера для генерации карточек
    """
    
    # Фотография компьютера
    photo = models.ImageField(
        upload_to='uploads/',
        verbose_name='Фото ПК',
        help_text='Загрузите фотографию собранного компьютера'
    )
    
    # Характеристики
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
        help_text='Например: 512GB NVMe SSD + 1TB HDD'
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
        help_text='Например: DeepCool MATREXX 55'
    )
    
    # Цена и бонусы
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Цена (руб.)',
        help_text='Цена в рублях'
    )
    bonuses = models.TextField(
        blank=True,
        verbose_name='Бонусы',
        help_text='Например: Windows 11 + Office в подарок!'
    )
    
    # Стиль карточки
    STYLE_CHOICES = [
        ('msi', '🔴 MSI Gaming'),
        ('steam', '🎮 Steam Library'),
        ('apple', '🍎 Apple Premium'),
        ('spotify', '🎵 Spotify Minimal'),
    ]
    style = models.CharField(
        max_length=20,
        choices=STYLE_CHOICES,
        default='msi',
        verbose_name='Стиль карточки'
    )
    
    # Метаданные
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Последнее обновление'
    )
    generated_card = models.ImageField(
        upload_to='generated/',
        blank=True,
        null=True,
        verbose_name='Сгенерированная карточка'
    )
    
    class Meta:
        verbose_name = 'Сборка ПК'
        verbose_name_plural = 'Сборки ПК'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.cpu} + {self.gpu} - {self.price}₽"
    
    def get_specs_list(self):
        """Возвращает список основных характеристик"""
        specs = [
            ('🖥 Процессор', self.cpu),
            ('🎮 Видеокарта', self.gpu),
            ('🧠 Оперативка', self.ram),
            ('💾 Накопитель', self.storage),
        ]
        if self.motherboard:
            specs.append(('🔧 Мат. плата', self.motherboard))
        if self.psu:
            specs.append(('⚡ Блок питания', self.psu))
        if self.case:
            specs.append(('📦 Корпус', self.case))
        return specs


class Preset(models.Model):
    """
    Пресеты для быстрого заполнения характеристик
    """
    name = models.CharField(
        max_length=100,
        verbose_name='Название пресета',
        help_text='Например: Игровой бюджетный'
    )
    cpu = models.CharField(max_length=100, verbose_name='Процессор')
    gpu = models.CharField(max_length=100, verbose_name='Видеокарта')
    ram = models.CharField(max_length=50, verbose_name='Оперативка')
    storage = models.CharField(max_length=100, verbose_name='Накопитель')
    motherboard = models.CharField(max_length=100, blank=True, verbose_name='Мат. плата')
    psu = models.CharField(max_length=100, blank=True, verbose_name='БП')
    case = models.CharField(max_length=100, blank=True, verbose_name='Корпус')
    
    class Meta:
        verbose_name = 'Пресет'
        verbose_name_plural = 'Пресеты'
        ordering = ['name']
    
    def __str__(self):
        return self.name
