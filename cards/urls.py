from django.urls import path
from . import views

app_name = 'cards'

urlpatterns = [
    # Главная
    path('', views.index, name='index'),
    
    # Галереи
    path('gallery/', views.gallery, name='gallery'),
    path('mixpc-gallery/', views.mixpc_gallery, name='mixpc_gallery'),
    
    # Создание
    path('create/', views.create_card, name='create'),
    path('presets/', views.presets, name='presets'),
    
    # Просмотр
    path('card/<int:card_id>/', views.card_detail, name='card_detail'),
    
    # MIXPC Series
    path('mixpc/<int:build_id>/', views.mixpc_result, name='mixpc_result'),
    path('mixpc/<int:build_id>/download/', views.download_mixpc_series, name='download_mixpc_series'),
]
