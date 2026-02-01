from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, FileResponse
from django.contrib import messages
from django.views.decorators.http import require_http_methods
import os

from .models import PCBuild, PCBuildPreset
from .forms import PCBuildForm
from .generators.msi_style import MSIStyleGenerator
from .generators.steam_style import SteamStyleGenerator
from .generators.apple_style import AppleStyleGenerator
from .generators.spotify_style import SpotifyStyleGenerator


def index(request):
    """Главная страница с формой создания"""
    recent_builds = PCBuild.objects.all()[:6]
    presets = PCBuildPreset.objects.all()
    
    if request.method == 'POST':
        form = PCBuildForm(request.POST, request.FILES)
        if form.is_valid():
            pc_build = form.save()
            return redirect('cards:preview', pk=pc_build.pk)
    else:
        form = PCBuildForm()
    
    context = {
        'form': form,
        'recent_builds': recent_builds,
        'presets': presets,
    }
    return render(request, 'cards/index.html', context)


def create_card(request):
    """Создание новой карточки"""
    if request.method == 'POST':
        form = PCBuildForm(request.POST, request.FILES)
        if form.is_valid():
            pc_build = form.save()
            messages.success(request, 'Карточка успешно создана!')
            return redirect('cards:preview', pk=pc_build.pk)
        else:
            messages.error(request, 'Ошибка при создании карточки. Проверьте данные.')
    else:
        form = PCBuildForm()
    
    return render(request, 'cards/create.html', {'form': form})


def preview_card(request, pk):
    """Превью карточки перед генерацией"""
    pc_build = get_object_or_404(PCBuild, pk=pk)
    
    context = {
        'pc_build': pc_build,
        'can_generate': not pc_build.generated_card,
    }
    return render(request, 'cards/preview.html', context)


def generate_card(request, pk):
    """Генерация карточки в выбранном стиле"""
    pc_build = get_object_or_404(PCBuild, pk=pk)
    
    try:
        # Выбираем генератор в зависимости от стиля
        generators = {
            'msi': MSIStyleGenerator,
            'steam': SteamStyleGenerator,
            'apple': AppleStyleGenerator,
            'spotify': SpotifyStyleGenerator,
        }
        
        generator_class = generators.get(pc_build.style, MSIStyleGenerator)
        generator = generator_class(pc_build)
        
        # Генерируем карточку
        card_path = generator.generate()
        
        # Сохраняем путь к сгенерированному файлу
        pc_build.generated_card = card_path
        pc_build.save()
        
        messages.success(request, 'Карточка успешно сгенерирована!')
        return redirect('cards:preview', pk=pk)
        
    except Exception as e:
        messages.error(request, f'Ошибка при генерации: {str(e)}')
        return redirect('cards:preview', pk=pk)


def download_card(request, pk):
    """Скачивание сгенерированной карточки"""
    pc_build = get_object_or_404(PCBuild, pk=pk)
    
    if not pc_build.generated_card:
        messages.error(request, 'Карточка еще не сгенерирована!')
        return redirect('cards:preview', pk=pk)
    
    try:
        # Открываем файл для скачивания
        file_path = pc_build.generated_card.path
        filename = f'partmart_pc_{pk}_{pc_build.style}.png'
        
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='image/png')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
            
    except Exception as e:
        messages.error(request, f'Ошибка при скачивании: {str(e)}')
        return redirect('cards:preview', pk=pk)


def history(request):
    """История созданных карточек"""
    all_builds = PCBuild.objects.all()
    
    # Фильтрация по стилю
    style_filter = request.GET.get('style')
    if style_filter:
        all_builds = all_builds.filter(style=style_filter)
    
    context = {
        'builds': all_builds,
        'current_filter': style_filter,
        'styles': PCBuild.STYLE_CHOICES,
    }
    return render(request, 'cards/history.html', context)


@require_http_methods(["POST"])
def delete_card(request, pk):
    """Удаление карточки"""
    pc_build = get_object_or_404(PCBuild, pk=pk)
    
    try:
        # Удаляем файлы
        if pc_build.photo:
            if os.path.exists(pc_build.photo.path):
                os.remove(pc_build.photo.path)
        
        if pc_build.generated_card:
            if os.path.exists(pc_build.generated_card.path):
                os.remove(pc_build.generated_card.path)
        
        # Удаляем запись
        pc_build.delete()
        
        messages.success(request, 'Карточка успешно удалена!')
    except Exception as e:
        messages.error(request, f'Ошибка при удалении: {str(e)}')
    
    return redirect('cards:history')


@require_http_methods(["GET"])
def get_preset_data(request, pk):
    """
API для получения данных пресета (AJAX)
    """
    try:
        preset = get_object_or_404(PCBuildPreset, pk=pk)
        
        data = {
            'cpu': preset.cpu,
            'gpu': preset.gpu,
            'ram': preset.ram,
            'storage': preset.storage,
            'motherboard': preset.motherboard,
            'psu': preset.psu,
            'case': preset.case,
            'bonuses': preset.bonuses,
        }
        
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
