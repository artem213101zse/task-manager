from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Task

# Common Tailwind classes for nice visible form controls
_INPUT_CLASSES = "w-full px-4 py-3 border border-slate-300 rounded-2xl focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition text-sm bg-white placeholder:text-slate-400"
_SELECT_CLASSES = "w-full px-4 py-3 border border-slate-300 rounded-2xl focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition text-sm bg-white"
_TEXTAREA_CLASSES = "w-full px-4 py-3 border border-slate-300 rounded-2xl focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition text-sm bg-white resize-y"


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': _INPUT_CLASSES,
                'placeholder': 'Например: Подготовить отчёт'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': _TEXTAREA_CLASSES,
                'placeholder': 'Подробное описание задачи (необязательно)'
            }),
            'status': forms.Select(attrs={'class': _SELECT_CLASSES}),
            'priority': forms.Select(attrs={'class': _SELECT_CLASSES}),
            'due_date': forms.DateInput(attrs={
                'type': 'date',
                'class': _INPUT_CLASSES
            }),
        }
        labels = {
            'title': 'Название',
            'description': 'Описание',
            'status': 'Статус',
            'priority': 'Приоритет',
            'due_date': 'Срок выполнения',
        }


class RegisterForm(UserCreationForm):
    """Custom registration form with nice Tailwind styling."""
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply consistent styling to all fields
        for field_name, field in self.fields.items():
            if field_name == 'username':
                field.widget.attrs.update({
                    'class': _INPUT_CLASSES,
                    'placeholder': 'Придумайте имя пользователя',
                    'autofocus': True,
                })
            elif field_name in ('password1', 'password2'):
                field.widget.attrs.update({
                    'class': _INPUT_CLASSES,
                    'placeholder': 'Введите пароль' if field_name == 'password1' else 'Повторите пароль',
                })
                # Make password fields show as password
                field.widget.input_type = 'password'
