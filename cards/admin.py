from django.contrib import admin
from .models import PCBuild, Preset


@admin.register(PCBuild)
class PCBuildAdmin(admin.ModelAdmin):
    list_display = ['cpu', 'gpu', 'price', 'style', 'created_at']
    list_filter = ['style', 'created_at']
    search_fields = ['cpu', 'gpu', 'motherboard']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Фотография', {
            'fields': ('photo',)
        }),
        ('Основные характеристики', {
            'fields': ('cpu', 'gpu', 'ram', 'storage')
        }),
        ('Дополнительные компоненты', {
            'fields': ('motherboard', 'psu', 'case'),
            'classes': ('collapse',)
        }),
        ('Цена и бонусы', {
            'fields': ('price', 'bonuses')
        }),
        ('Оформление', {
            'fields': ('style', 'generated_card')
        }),
        ('Метаданные', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Preset)
class PresetAdmin(admin.ModelAdmin):
    list_display = ['name', 'cpu', 'gpu']
    search_fields = ['name', 'cpu', 'gpu']
