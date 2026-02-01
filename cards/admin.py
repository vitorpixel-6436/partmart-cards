from django.contrib import admin
from .models import PCBuild, GeneratedCard


@admin.register(PCBuild)
class PCBuildAdmin(admin.ModelAdmin):
    """Админка для конфигураций ПК"""
    
    list_display = ('name', 'cpu', 'gpu', 'price', 'warranty_months', 'created_at')
    list_filter = ('created_at', 'warranty_months')
    search_fields = ('name', 'cpu', 'gpu')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'price', 'warranty_months')
        }),
        ('Компоненты', {
            'fields': ('cpu', 'gpu', 'ram', 'storage', 'motherboard', 'psu', 'case', 'cooling')
        }),
        ('Фото', {
            'fields': ('photo',)
        }),
        ('Метаданные', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(GeneratedCard)
class GeneratedCardAdmin(admin.ModelAdmin):
    """Админка для сгенерированных карточек"""
    
    list_display = ('build', 'style', 'card_number', 'created_at')
    list_filter = ('style', 'created_at', 'card_number')
    search_fields = ('build__name', 'build__cpu', 'build__gpu')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('build', 'style', 'card_number')
        }),
        ('Изображение', {
            'fields': ('image',)
        }),
        ('Метаданные', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
