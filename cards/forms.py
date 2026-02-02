from django import forms
from .models import PCBuild


class PCBuildForm(forms.ModelForm):
    """Форма для создания конфигурации ПК"""
    
    class Meta:
        model = PCBuild
        fields = [
            'name', 'photo',
            'cpu', 'gpu', 'ram', 'storage',
            'motherboard', 'psu', 'case', 'cooling',
            'price', 'warranty_months'
        ]
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl bg-white/5 border border-white/20 text-white placeholder-gray-400 focus:border-purple-500 focus:ring-2 focus:ring-purple-500/50 transition-all',
                'placeholder': 'Игровой ПК'
            }),
            'cpu': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl bg-white/5 border border-white/20 text-white placeholder-gray-400 focus:border-purple-500 focus:ring-2 focus:ring-purple-500/50 transition-all',
                'placeholder': 'AMD Ryzen 5 7500F'
            }),
            'gpu': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl bg-white/5 border border-white/20 text-white placeholder-gray-400 focus:border-purple-500 focus:ring-2 focus:ring-purple-500/50 transition-all',
                'placeholder': 'RTX 5060 Ti 16GB GDDR7'
            }),
            'ram': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl bg-white/5 border border-white/20 text-white placeholder-gray-400 focus:border-purple-500 focus:ring-2 focus:ring-purple-500/50 transition-all',
                'placeholder': 'DDR5 32GB (2x16GB)'
            }),
            'storage': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl bg-white/5 border border-white/20 text-white placeholder-gray-400 focus:border-purple-500 focus:ring-2 focus:ring-purple-500/50 transition-all',
                'placeholder': 'SSD M.2 1TB NVMe'
            }),
            'motherboard': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl bg-white/5 border border-white/20 text-white placeholder-gray-400 focus:border-purple-500 focus:ring-2 focus:ring-purple-500/50 transition-all',
                'placeholder': 'B650'
            }),
            'psu': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl bg-white/5 border border-white/20 text-white placeholder-gray-400 focus:border-purple-500 focus:ring-2 focus:ring-purple-500/50 transition-all',
                'placeholder': '750W'
            }),
            'case': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl bg-white/5 border border-white/20 text-white placeholder-gray-400 focus:border-purple-500 focus:ring-2 focus:ring-purple-500/50 transition-all',
                'placeholder': 'ATX Tower'
            }),
            'cooling': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl bg-white/5 border border-white/20 text-white placeholder-gray-400 focus:border-purple-500 focus:ring-2 focus:ring-purple-500/50 transition-all',
                'placeholder': 'Tower Cooler'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl bg-white/5 border border-white/20 text-white placeholder-gray-400 focus:border-purple-500 focus:ring-2 focus:ring-purple-500/50 transition-all',
                'placeholder': '85000',
                'step': '0.01'
            }),
            'warranty_months': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl bg-white/5 border border-white/20 text-white placeholder-gray-400 focus:border-purple-500 focus:ring-2 focus:ring-purple-500/50 transition-all',
                'placeholder': '36',
                'min': '1',
                'max': '60'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'hidden',
                'accept': 'image/*',
                'id': 'photo-upload'
            }),
        }
