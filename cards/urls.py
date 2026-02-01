from django.urls import path
from . import views

app_name = 'cards'

urlpatterns = [
    # Главная страница
    path('', views.index, name='index'),
    
    # Создание карточки
    path('create/', views.create_card, name='create'),
    
    # Превью карточки
    path('preview/<int:pk>/', views.preview_card, name='preview'),
    
    # Генерация карточки
    path('generate/<int:pk>/', views.generate_card, name='generate'),
    
    # Скачивание карточки
    path('download/<int:pk>/', views.download_card, name='download'),
    
    # История карточек
    path('history/', views.history, name='history'),
    
    # Удаление карточки
    path('delete/<int:pk>/', views.delete_card, name='delete'),
    
    # API для получения пресета
    path('api/preset/<int:pk>/', views.get_preset_data, name='get_preset'),
]
