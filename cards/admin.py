from django.contrib import admin
from .models import PCBuild, PCBuildPreset


@admin.register(PCBuild)
class PCBuildAdmin(admin.ModelAdmin):
    list_display = ['cpu', 'gpu', 'price', 'style', 'created_at']
    list_filter = ['style', 'created_at']
    search_fields = ['cpu', 'gpu', 'ram']
    readonly_fields = ['created_at', 'updated_at', 'generated_card']
    
    fieldsets = (
        ('Фотография', {
            'fields': ('photo',)
        }),
        ('Характеристики', {
            'fields': ('cpu', 'gpu', 'ram', 'storage', 'motherboard', 'psu', 'case')
        }),
        ('Цена и бонусы', {
            'fields': ('price', 'bonuses')
        }),
        ('Дизайн', {
            'fields': ('style',)
        }),
        ('Результат', {
            'fields': ('generated_card', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PCBuildPreset)
class PCBuildPresetAdmin(admin.ModelAdmin):
    list_display = ['name', 'cpu', 'gpu', 'created_at']
    search_fields = ['name', 'cpu', 'gpu']
    
    fieldsets = (
        ('Общая информация', {
            'fields': ('name', 'description')
        }),
        ('Характеристики', {
            'fields': ('cpu', 'gpu', 'ram', 'storage', 'motherboard', 'psu', 'case')
        }),
        ('Бонусы', {
            'fields': ('bonuses',)
        }),
    )
