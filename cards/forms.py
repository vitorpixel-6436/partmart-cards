from django import forms
from .models import PCBuild, PCBuildPreset


class PCBuildForm(forms.ModelForm):
    """
    Форма для создания карточки ПК
    """
    
    preset = forms.ModelChoiceField(
        queryset=PCBuildPreset.objects.all(),
        required=False,
        empty_label='Выберите пресет...',
        widget=forms.Select(attrs={
            'class': 'form-control glass-select',
            'id': 'preset-select'
        }),
        label='Пресет конфигурации'
    )
    
    class Meta:
        model = PCBuild
        fields = [
            'photo', 'cpu', 'gpu', 'ram', 'storage',
            'motherboard', 'psu', 'case', 'price', 'bonuses', 'style'
        ]
        
        widgets = {
            'photo': forms.FileInput(attrs={
                'class': 'form-control-file',
                'id': 'photo-upload',
                'accept': 'image/*'
            }),
            'cpu': forms.TextInput(attrs={
                'class': 'form-control glass-input',
                'placeholder': 'Например: Intel Core i5-12400F'
            }),
            'gpu': forms.TextInput(attrs={
                'class': 'form-control glass-input',
                'placeholder': 'Например: NVIDIA RTX 3060 Ti 8GB'
            }),
            'ram': forms.TextInput(attrs={
                'class': 'form-control glass-input',
                'placeholder': 'Например: 16GB DDR4 3200MHz'
            }),
            'storage': forms.TextInput(attrs={
                'class': 'form-control glass-input',
                'placeholder': 'Например: SSD 512GB NVMe'
            }),
            'motherboard': forms.TextInput(attrs={
                'class': 'form-control glass-input',
                'placeholder': 'Например: ASUS B660M-PLUS (опционально)'
            }),
            'psu': forms.TextInput(attrs={
                'class': 'form-control glass-input',
                'placeholder': 'Например: 650W 80+ Bronze (опционально)'
            }),
            'case': forms.TextInput(attrs={
                'class': 'form-control glass-input',
                'placeholder': 'Например: DeepCool CC560 (опционально)'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control glass-input',
                'placeholder': '50000',
                'step': '100'
            }),
            'bonuses': forms.Textarea(attrs={
                'class': 'form-control glass-input',
                'placeholder': 'Windows 11 Pro + Microsoft Office в подарок!',
                'rows': 3
            }),
            'style': forms.RadioSelect(attrs={
                'class': 'style-radio'
            })
        }


class PCBuildPresetForm(forms.ModelForm):
    """
    Форма для создания пресета
    """
    class Meta:
        model = PCBuildPreset
        fields = '__all__'
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control glass-input'}),
            'description': forms.Textarea(attrs={'class': 'form-control glass-input', 'rows': 2}),
            'cpu': forms.TextInput(attrs={'class': 'form-control glass-input'}),
            'gpu': forms.TextInput(attrs={'class': 'form-control glass-input'}),
            'ram': forms.TextInput(attrs={'class': 'form-control glass-input'}),
            'storage': forms.TextInput(attrs={'class': 'form-control glass-input'}),
            'motherboard': forms.TextInput(attrs={'class': 'form-control glass-input'}),
            'psu': forms.TextInput(attrs={'class': 'form-control glass-input'}),
            'case': forms.TextInput(attrs={'class': 'form-control glass-input'}),
            'bonuses': forms.Textarea(attrs={'class': 'form-control glass-input', 'rows': 3}),
        }
