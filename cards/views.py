from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, FileResponse
from django.contrib import messages
from .models import PCBuild, Preset
from .forms import PCBuildForm
from .generators.card_generator import CardGenerator
import os


def index(request):
    """
    Главная страница с последними сборками
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
            build = form.save()
            messages.success(request, '✅ Сборка создана! Теперь сгенерируйте карточку.')
            return redirect('cards:preview', pk=build.pk)
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
    Preview карточки перед генерацией
    """
    build = get_object_or_404(PCBuild, pk=pk)
    context = {
        'build': build,
    }
    return render(request, 'cards/preview.html', context)


def generate_card(request, pk):
    """
    Генерация карточки с выбранным стилем
    """
    build = get_object_or_404(PCBuild, pk=pk)
    
    try:
        generator = CardGenerator(build)
        generated_path = generator.generate()
        
        # Сохраняем путь к сгенерированной карточке
        build.generated_card = generated_path
        build.save()
        
        messages.success(request, f'🎉 Карточка сгенерирована в стиле {build.get_style_display()}!')
    except Exception as e:
        messages.error(request, f'❌ Ошибка генерации: {str(e)}')
    
    return redirect('cards:preview', pk=pk)


def download_card(request, pk):
    """
    Скачивание сгенерированной карточки
    """
    build = get_object_or_404(PCBuild, pk=pk)
    
    if not build.generated_card:
        messages.error(request, '❌ Сначала сгенерируйте карточку!')
        return redirect('cards:preview', pk=pk)
    
    file_path = build.generated_card.path
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename="partmart_{build.pk}.png"'
        return response
    else:
        messages.error(request, '❌ Файл карточки не найден!')
        return redirect('cards:preview', pk=pk)


def gallery(request):
    """
    Галерея всех созданных карточек
    """
    builds = PCBuild.objects.filter(generated_card__isnull=False)
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
