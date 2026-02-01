from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class PCBuild(models.Model):
    """Модель конфигурации ПК"""
    
    name = models.CharField('Название', max_length=200)
    
    # Компоненты
    cpu = models.CharField('Процессор', max_length=200)
    gpu = models.CharField('Видеокарта', max_length=200)
    ram = models.CharField('Оперативная память', max_length=100)
    storage = models.CharField('Накопитель', max_length=200)
    motherboard = models.CharField('Материнская плата', max_length=200)
    psu = models.CharField('Блок питания', max_length=100)
    case = models.CharField('Корпус', max_length=200, blank=True)
    cooling = models.CharField('Охлаждение', max_length=200, blank=True)
    
    # Дополнительно
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2, default=0)
    warranty_months = models.IntegerField(
        'Гарантия (месяцы)',
        default=36,
        validators=[MinValueValidator(1), MaxValueValidator(60)]
    )
    
    # Фото
    photo = models.ImageField('Фото ПК', upload_to='uploads/', blank=True, null=True)
    
    # Метаданные
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        verbose_name = 'Конфигурация ПК'
        verbose_name_plural = 'Конфигурации ПК'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.name} ({self.cpu} + {self.gpu})'
    
    def get_specs_list(self):
        """Возвращает список характеристик для отображения на карточке"""
        specs = [
            ('🖥️ Процессор', self.cpu),
            ('🎮 Видеокарта', self.gpu),
            ('💾 Оперативка', self.ram),
            ('💿 Накопитель', self.storage),
            ('🔌 Мат. плата', self.motherboard),
            ('⚡ Блок питания', self.psu),
        ]
        
        if self.case:
            specs.append(('📦 Корпус', self.case))
        
        if self.cooling:
            specs.append(('❄️ Охлаждение', self.cooling))
        
        return specs


class GeneratedCard(models.Model):
    """Сгенерированная карточка"""
    
    STYLE_CHOICES = [
        ('msi', 'MSI Gaming'),
        ('steam', 'Steam Library'),
        ('apple', 'Apple Premium'),
        ('spotify', 'Spotify Minimal'),
        ('mixpc', 'MIXPC Series'),
    ]
    
    build = models.ForeignKey(
        PCBuild,
        on_delete=models.CASCADE,
        related_name='generated_cards',
        verbose_name='Конфигурация'
    )
    
    style = models.CharField(
        'Стиль',
        max_length=20,
        choices=STYLE_CHOICES,
        default='msi'
    )
    
    image = models.ImageField(
        'Изображение',
        upload_to='generated/',
        blank=True,
        null=True
    )
    
    # Для MIXPC Series - номер карточки в серии
    card_number = models.IntegerField(
        'Номер в серии',
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    
    # Метаданные
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Сгенерированная карточка'
        verbose_name_plural = 'Сгенерированные карточки'
        ordering = ['-created_at', 'card_number']
    
    def __str__(self):
        if self.style == 'mixpc':
            return f'{self.build.name} - {self.get_style_display()} #{self.card_number}'
        return f'{self.build.name} - {self.get_style_display()}'
    
    def get_card_title(self):
        """Название карточки для MIXPC Series"""
        if self.style != 'mixpc':
            return self.build.name
        
        titles = {
            1: 'Игровой компьютер',
            2: 'Конфигурация',
            3: 'Тесты в играх',
            4: 'Тестирование перед отправкой',
            5: 'Бесплатная доставка',
            6: 'Трейд-ин / Скидка',
        }
        
        return titles.get(self.card_number, f'Карточка #{self.card_number}')
