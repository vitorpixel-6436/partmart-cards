from django import forms
from .models import PCBuild, Preset
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, HTML


class PCBuildForm(forms.ModelForm):
    """
    Форма для создания/редактирования сборки ПК
    """
    
    class Meta:
        model = PCBuild
        fields = [
            'photo', 'cpu', 'gpu', 'ram', 'storage',
            'motherboard', 'psu', 'case', 'price', 'bonuses', 'style'
        ]
        widgets = {
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'cpu': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Intel Core i5-12400F / AMD Ryzen 5 5600X'
            }),
            'gpu': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'NVIDIA RTX 3060 Ti 8GB / AMD RX 6700 XT'
            }),
            'ram': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '16GB DDR4 3200MHz'
            }),
            'storage': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '512GB NVMe SSD + 1TB HDD'
            }),
            'motherboard': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ASUS B660M-PLUS'
            }),
            'psu': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '650W 80+ Bronze'
            }),
            'case': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'DeepCool MATREXX 55'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '45000'
            }),
            'bonuses': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Windows 11 + Office в подарок!\nГарантия 1 год'
            }),
            'style': forms.RadioSelect(attrs={
                'class': 'form-check-input'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'glass-panel'
