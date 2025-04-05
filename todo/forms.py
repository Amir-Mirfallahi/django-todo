from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'priority', 'status')
        labels = {
            'title': 'عنوان کار',
            'description': 'توضیحات',
            'priority': 'اولویت',
            'status': 'وضعیت',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full p-2 rounded-md dark:bg-gray-800', 'placeholder': 'عنوان کار'}),
            'description': forms.Textarea(attrs={'class': 'w-full p-2 rounded-md dark:bg-gray-800', 'placeholder': 'توضیحات'}),
            'priority': forms.Select(attrs={'class': 'w-full p-2 rounded-md dark:bg-gray-800', 'placeholder': 'اولویت'}),
            'status': forms.CheckboxInput(attrs={'class': 'p-2 rounded-md dark:bg-gray-800', 'placeholder': 'وضعیت'}),
        }
