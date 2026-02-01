from django.urls import path
from . import views

app_name = 'cards'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_card, name='create'),
    path('preview/<int:pk>/', views.preview_card, name='preview'),
    path('generate/<int:pk>/', views.generate_card, name='generate'),
    path('download/<int:pk>/', views.download_card, name='download'),
    path('gallery/', views.gallery, name='gallery'),
    path('presets/', views.presets, name='presets'),
]
