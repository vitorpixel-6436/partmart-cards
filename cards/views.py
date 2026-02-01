from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, FileResponse
from django.contrib import messages
from .models import PCBuild, Preset
from .forms import PCBuildForm
from .generators.card_generator import CardGenerator
import os


def index(request):
    """
    Главная страница
    """
    recent_builds = PCBuild.objects.all()[:6]
    context = {
        'recent_builds': recent_builds,
        'total_builds': PCBuild.objects.count(),
    }
    return render(request, 'cards/index.html', context)


def create_card(request):
    """
    Создание новой карточки
    """
    if request.method == 'POST':
        form = PCBuildForm(request.POST, request.FILES)
        if form.is_valid():
            pc_build = form.save()
            messages.success(request, '✅ Сборка создана! Теперь можно сгенерировать карточку.')
            return redirect('cards:preview', pk=pc_build.pk)
    else:
        form = PCBuildForm()
    
    presets = Preset.objects.all()
    context = {
        'form': form,
        'presets': presets,
    }
    return render(request, 'cards/create.html', context)


def preview_card(request, pk):
    """
    Превью карточки перед генерацией
    """
    pc_build = get_object_or_404(PCBuild, pk=pk)
    context = {
        'pc_build': pc_build,
    }
    return render(request, 'cards/preview.html', context)


def generate_card(request, pk):
    """
    Генерация карточки
    """
    pc_build = get_object_or_404(PCBuild, pk=pk)
    
    try:
        # Создаем генератор и генерируем карточку
        generator = CardGenerator(pc_build)
        card_path = generator.generate()
        
        # Сохраняем путь к сгенерированной карточке
        pc_build.generated_card = card_path
        pc_build.save()
        
        messages.success(request, '🎉 Карточка успешно сгенерирована!')
    except Exception as e:
        messages.error(request, f'❌ Ошибка при генерации: {str(e)}')
    
    return redirect('cards:preview', pk=pk)


def download_card(request, pk):
    """
    Скачивание сгенерированной карточки
    """
    pc_build = get_object_or_404(PCBuild, pk=pk)
    
    if not pc_build.generated_card:
        messages.error(request, 'Сначала сгенерируйте карточку!')
        return redirect('cards:preview', pk=pk)
    
    file_path = pc_build.generated_card.path
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename="partmart_{pc_build.pk}.png"'
        return response
    else:
        messages.error(request, 'Файл не найден!')
        return redirect('cards:preview', pk=pk)


def gallery(request):
    """
    Галерея всех созданных карточек
    """
    builds = PCBuild.objects.all()
    context = {
        'builds': builds,
    }
    return render(request, 'cards/gallery.html', context)


def presets(request):
    """
    Управление пресетами
    """
    all_presets = Preset.objects.all()
    context = {
        'presets': all_presets,
    }
    return render(request, 'cards/presets.html', context)
