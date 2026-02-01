# Generated migration

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PCBuild',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(help_text='Загрузите фотографию собранного компьютера', upload_to='uploads/', verbose_name='Фото ПК')),
                ('cpu', models.CharField(help_text='Например: Intel Core i5-12400F', max_length=100, verbose_name='Процессор')),
                ('gpu', models.CharField(help_text='Например: NVIDIA RTX 3060 Ti 8GB', max_length=100, verbose_name='Видеокарта')),
                ('ram', models.CharField(help_text='Например: 16GB DDR4 3200MHz', max_length=50, verbose_name='Оперативная память')),
                ('storage', models.CharField(help_text='Например: 512GB NVMe SSD + 1TB HDD', max_length=100, verbose_name='Накопитель')),
                ('motherboard', models.CharField(blank=True, help_text='Например: ASUS B660M-PLUS', max_length=100, verbose_name='Материнская плата')),
                ('psu', models.CharField(blank=True, help_text='Например: 650W 80+ Bronze', max_length=100, verbose_name='Блок питания')),
                ('case', models.CharField(blank=True, help_text='Например: DeepCool MATREXX 55', max_length=100, verbose_name='Корпус')),
                ('price', models.DecimalField(decimal_places=2, help_text='Цена в рублях', max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Цена (руб.)')),
                ('bonuses', models.TextField(blank=True, help_text='Например: Windows 11 + Office в подарок!', verbose_name='Бонусы')),
                ('style', models.CharField(choices=[('msi', '🔴 MSI Gaming'), ('steam', '🎮 Steam Library'), ('apple', '🍎 Apple Premium'), ('spotify', '🎵 Spotify Minimal')], default='msi', max_length=20, verbose_name='Стиль карточки')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Последнее обновление')),
                ('generated_card', models.ImageField(blank=True, null=True, upload_to='generated/', verbose_name='Сгенерированная карточка')),
            ],
            options={
                'verbose_name': 'Сборка ПК',
                'verbose_name_plural': 'Сборки ПК',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Preset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Например: Игровой бюджетный', max_length=100, verbose_name='Название пресета')),
                ('cpu', models.CharField(max_length=100, verbose_name='Процессор')),
                ('gpu', models.CharField(max_length=100, verbose_name='Видеокарта')),
                ('ram', models.CharField(max_length=50, verbose_name='Оперативка')),
                ('storage', models.CharField(max_length=100, verbose_name='Накопитель')),
                ('motherboard', models.CharField(blank=True, max_length=100, verbose_name='Мат. плата')),
                ('psu', models.CharField(blank=True, max_length=100, verbose_name='БП')),
                ('case', models.CharField(blank=True, max_length=100, verbose_name='Корпус')),
            ],
            options={
                'verbose_name': 'Пресет',
                'verbose_name_plural': 'Пресеты',
                'ordering': ['name'],
            },
        ),
    ]
