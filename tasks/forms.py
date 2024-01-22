from django import forms
from .models import Task
from django.core.exceptions import ValidationError


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "task_exp"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Titulo"}
            ),
            "description": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Descripción"}
            ),
            'task_exp': forms.DateTimeInput(
                attrs={'class': 'form-control', 'placeholder': 'Fecha de entrega', 'type': 'datetime-local'}
            )
        }

    def clean_title(self):
        title = self.cleaned_data["title"]
        error_dict = []

        print(title)

        if len(title) < 5:
            error_dict.append(
                ValidationError('El título de la tarea tiene que ser mayor de 5 caracteres', code='min_len')
            )

        if len(title) > 50:
            error_dict.append(
                ValidationError('El titulo de la tarea no puede ser mayor a 50 caracteres', code='max_len')
            )

        if error_dict:
            raise ValidationError(error_dict)
        
        return title

    def clean_description(self):
        des = self.cleaned_data["description"]
        error_dict = []


        if len(des) < 5:
            error_dict.append(
                ValidationError('El título de la tarea tiene que ser mayor de 5 caracteres', code='min_len')
            )

        if len(des) > 150:
            error_dict.append(
                ValidationError('El titulo de la tarea no puede ser mayor a 50 caracteres', code='max_len')
            )

        if error_dict:
            raise ValidationError(error_dict)
        
        return des
    
