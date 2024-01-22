from django import forms
from .models import Assignment
from django.core.exceptions import ValidationError
from django.conf import settings


class CreateAssignmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(CreateAssignmentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Assignment
        fields = ["title", "teacher", "description", "image"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Título"}
            ),
            "teacher": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Maestr@"}
            ),
            "description": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Descripción"}
            ),
            "image": forms.FileInput(
                attrs={"class": "form-control", "placeholder": "Imagen"}
            ),
        }

    def clean_title(self):
        title = self.cleaned_data["title"]
        error_dict = []

        assignmentInUse = Assignment.objects.filter(
            title=title, user=self.user.id
        ).exists()

        if assignmentInUse:
            error_dict.append(
                ValidationError(
                    "Ya tienes registrada esta materia", code="assignment_in_use"
                )
            )

        if len(title) > 25:
            error_dict.append(
                ValidationError(
                    "El título de la materia no debe tener más de 25 caracteres",
                    code="assignment_too_long",
                )
            )

        if error_dict:
            raise forms.ValidationError(error_dict)

        return title

    def clean_teacher(self):
        teacher = self.cleaned_data["teacher"]
        error_dict = []

        if len(teacher) > 100:
            error_dict.append(
                ValidationError(
                    "El nombre del maestro no debe tener más de 100 caracteres",
                    code="teacher_too_long",
                )
            )

        if error_dict:
            raise forms.ValidationError(error_dict)

        return teacher

    def clean_description(self):
        description = self.cleaned_data["description"]
        error_dict = []

        if len(description) > 150:
            error_dict.append(
                ValidationError(
                    "La descripción no debe tener más de 150 caracteres",
                    code="description_too_long",
                )
            )

        if error_dict:
            raise forms.ValidationError(error_dict)

        return description

    def clean_image(self):
        image = self.cleaned_data["image"]

        if image is not None:
            file_type = image.content_type.split("/")[0]
            error_dict = []

            if image.size > settings.MAX_UPLOAD_SIZE:
                error_dict.append(
                    ValidationError(
                        "La imagen no debe pesar más de 5 mb", code="file_too_big"
                    )
                )

            if file_type not in settings.CONTENT_TYPES:
                error_dict.append(
                    ValidationError(
                        "Tipo de archivo no válido", code="file_not_supported"
                    )
                )

            if error_dict:
                raise forms.ValidationError(error_dict)

            return image

        return image
