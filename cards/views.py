from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, FileResponse, JsonResponse
from .models import PCBuild, GeneratedCard
from .generators import (
    MSIStyleGenerator,
    SteamStyleGenerator,
    AppleStyleGenerator,
    SpotifyStyleGenerator,
    MIXPCSeriesGenerator
)
from PIL import Image
import zipfile
import io
import os
from django.conf import settings


def index(request):
    """Главная страница с недавними карточками"""
    recent_cards = GeneratedCard.objects.select_related('build').order_by('-created_at')[:6]
    
    context = {
        'recent_cards': recent_cards,
    }
    return render(request, 'cards/index.html', context)


def gallery(request):
    """Галерея всех сгенерированных карточек"""
    cards = GeneratedCard.objects.select_related('build').order_by('-created_at')
    
    # Фильтр по стилю
    style = request.GET.get('style')
    if style:
        cards = cards.filter(style=style)
    
    context = {
        'cards': cards,
        'current_style': style,
    }
    return render(request, 'cards/gallery.html', context)


def mixpc_gallery(request):
    """Специальная галерея для MIXPC Series"""
    return render(request, 'cards/mixpc_gallery.html')


def create_card(request):
    """Создание новой карточки"""
    if request.method == 'POST':
        # Получаем данные из формы
        name = request.POST.get('name', 'Gaming PC')
        cpu = request.POST.get('cpu', 'AMD Ryzen 5 7500F')
        gpu = request.POST.get('gpu', 'RTX 5060 Ti 16GB')
        ram = request.POST.get('ram', 'DDR5 32GB (2x16GB)')
        storage = request.POST.get('storage', 'SSD M.2 1TB NVMe')
        motherboard = request.POST.get('motherboard', 'B650')
        psu = request.POST.get('psu', '750W')
        case = request.POST.get('case', 'ATX Tower')
        price = request.POST.get('price', '0')
        warranty = request.POST.get('warranty', '36')
        
        # Стиль
        style = request.POST.get('style', 'msi')
        
        # Фото
        photo = request.FILES.get('photo')
        
        try:
            # Создаём PCBuild
            build = PCBuild.objects.create(
                name=name,
                cpu=cpu,
                gpu=gpu,
                ram=ram,
                storage=storage,
                motherboard=motherboard,
                psu=psu,
                case=case,
                price=float(price) if price else 0,
                warranty_months=int(warranty) if warranty else 36
            )
            
            # Сохраняем фото если есть
            if photo:
                build.photo = photo
                build.save()
            
            # Генерируем карточку
            generator_map = {
                'msi': MSIStyleGenerator,
                'steam': SteamStyleGenerator,
                'apple': AppleStyleGenerator,
                'spotify': SpotifyStyleGenerator,
                'mixpc': MIXPCSeriesGenerator,
            }
            
            generator_class = generator_map.get(style, MSIStyleGenerator)
            generator = generator_class(build)
            
            # Генерация серии или одной карточки
            if style == 'mixpc':
                cards = generator.generate_series()
                
                # Сохраняем все карточки
                generated_cards = []
                for i, card_image in enumerate(cards, 1):
                    # Сохраняем во временный файл
                    temp_path = os.path.join(settings.MEDIA_ROOT, 'generated', f'{build.id}_card_{i}.png')
                    os.makedirs(os.path.dirname(temp_path), exist_ok=True)
                    card_image.save(temp_path, 'PNG')
                    
                    # Создаём запись в БД
                    card = GeneratedCard.objects.create(
                        build=build,
                        style=style,
                        card_number=i
                    )
                    card.image.name = f'generated/{build.id}_card_{i}.png'
                    card.save()
                    generated_cards.append(card)
                
                messages.success(request, f'✅ Серия из {len(cards)} карточек успешно создана!')
                return redirect('cards:mixpc_result', build_id=build.id)
            else:
                # Одна карточка
                card_image = generator.generate()
                
                # Сохраняем
                temp_path = os.path.join(settings.MEDIA_ROOT, 'generated', f'{build.id}_card.png')
                os.makedirs(os.path.dirname(temp_path), exist_ok=True)
                card_image.save(temp_path, 'PNG')
                
                card = GeneratedCard.objects.create(
                    build=build,
                    style=style
                )
                card.image.name = f'generated/{build.id}_card.png'
                card.save()
                
                messages.success(request, '✅ Карточка успешно создана!')
                return redirect('cards:card_detail', card_id=card.id)
                
        except Exception as e:
            messages.error(request, f'❌ Ошибка при создании карточки: {str(e)}')
            return redirect('cards:create')
    
    # GET запрос
    context = {
        'presets': [
            {
                'name': 'Бюджетный ПК',
                'cpu': 'AMD Ryzen 5 7500F',
                'gpu': 'RTX 4060 8GB',
                'ram': 'DDR5 16GB',
                'price': 45000,
            },
            {
                'name': 'Игровой ПК',
                'cpu': 'AMD Ryzen 7 7700X',
                'gpu': 'RTX 4070 Super 12GB',
                'ram': 'DDR5 32GB',
                'price': 85000,
            },
            {
                'name': 'Топовый ПК',
                'cpu': 'AMD Ryzen 9 7950X',
                'gpu': 'RTX 4090 24GB',
                'ram': 'DDR5 64GB',
                'price': 250000,
            },
        ]
    }
    return render(request, 'cards/create.html', context)


def mixpc_result(request, build_id):
    """Страница результата для MIXPC Series"""
    build = get_object_or_404(PCBuild, id=build_id)
    cards = GeneratedCard.objects.filter(build=build, style='mixpc').order_by('card_number')
    
    context = {
        'build': build,
        'cards': cards,
    }
    return render(request, 'cards/mixpc_result.html', context)


def download_mixpc_series(request, build_id):
    """Скачать всю серию MIXPC в ZIP"""
    build = get_object_or_404(PCBuild, id=build_id)
    cards = GeneratedCard.objects.filter(build=build, style='mixpc').order_by('card_number')
    
    # Создаём ZIP в памяти
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for card in cards:
            if card.image:
                # Добавляем файл в архив
                file_path = card.image.path
                arcname = f'card_{card.card_number}.png'
                zip_file.write(file_path, arcname)
    
    zip_buffer.seek(0)
    
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{build.name}_MIXPC_Series.zip"'
    
    return response


def card_detail(request, card_id):
    """Детали одной карточки"""
    card = get_object_or_404(GeneratedCard, id=card_id)
    
    context = {
        'card': card,
    }
    return render(request, 'cards/card_detail.html', context)


def presets(request):
    """Страница с пресетами"""
    presets_data = [
        {
            'name': '🎮 Игровой начальный',
            'description': 'Для комфортной игры в Full HD',
            'cpu': 'AMD Ryzen 5 7500F',
            'gpu': 'RTX 4060 8GB GDDR6',
            'ram': 'DDR5 16GB (2x8GB)',
            'storage': 'SSD M.2 512GB NVMe',
            'motherboard': 'B650',
            'psu': '650W',
            'price': 45000,
            'warranty': 36,
        },
        {
            'name': '🚀 Игровой средний',
            'description': 'Для игр в 2K с высокими настройками',
            'cpu': 'AMD Ryzen 7 7700X',
            'gpu': 'RTX 4070 Super 12GB GDDR6X',
            'ram': 'DDR5 32GB (2x16GB)',
            'storage': 'SSD M.2 1TB NVMe',
            'motherboard': 'B650',
            'psu': '750W',
            'price': 85000,
            'warranty': 36,
        },
        {
            'name': '⭐ Игровой топовый',
            'description': 'Для игр в 4K с максимальными настройками',
            'cpu': 'AMD Ryzen 9 7950X',
            'gpu': 'RTX 4090 24GB GDDR6X',
            'ram': 'DDR5 64GB (2x32GB)',
            'storage': 'SSD M.2 2TB NVMe',
            'motherboard': 'X670E',
            'psu': '1000W',
            'price': 250000,
            'warranty': 36,
        },
        {
            'name': '💼 Рабочая станция',
            'description': 'Для работы с видео и 3D',
            'cpu': 'AMD Ryzen 9 7950X3D',
            'gpu': 'RTX 4080 16GB GDDR6X',
            'ram': 'DDR5 128GB (4x32GB)',
            'storage': 'SSD M.2 4TB NVMe',
            'motherboard': 'X670E',
            'psu': '1000W',
            'price': 280000,
            'warranty': 36,
        },
    ]
    
    context = {
        'presets': presets_data,
    }
    return render(request, 'cards/presets.html', context)
