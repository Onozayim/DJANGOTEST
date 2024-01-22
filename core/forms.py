from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="Nombre de usuario",
        min_length=5,
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control mt-1", "placeholder": "Nombre de usuario"}),
    )
    email = forms.CharField(
        label="Correo", widget=forms.EmailInput(attrs={"class": "form-control mt-1", "placeholder": "Correo"})
    )
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control mt-1", "placeholder": "Contraseña"}),
    )
    password2 = forms.CharField(
        label="Confirma tu contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control mt-1", "placeholder": "Confirma tu contraseña"}),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_username(self):
        error_dict = []
        username = self.cleaned_data["username"]
        userInUse = User.objects.filter(username=username).exists()
        
        if(userInUse):
            error_dict.append(ValidationError("El nombre de usuario está en uso", code="username_in_use"))

        if len(username) < 5:
            error_dict.append(ValidationError("El nombre de usuario es demasiado corto", code="min_length"))
            
        if error_dict:
            raise forms.ValidationError(error_dict)

        return username

    def clean_email(self):
        error_dict = []

        email = self.cleaned_data["email"]
        emailInUse = User.objects.filter(email=email)

        if(emailInUse): 
            error_dict.append(ValidationError("El correo está en uso", code='email_in_use'))

        try:
            validate_email(email)
        except ValidationError:
            error_dict.append(
                ValidationError("El correo no es válido", code="not_valid")
            )

        if error_dict:
            raise ValidationError(error_dict)

        return email

    def clean_password1(self):
        erro_dict = []

        password = self.cleaned_data["password1"]

        if password.isdigit():
            erro_dict.append(
                ValidationError(
                    "La contraseña debe tener al menos un caracter", code="is_numeric"
                )
            )

        if password.isalpha():
            erro_dict.append(
                ValidationError(
                    "La contraseña debe tener al menos un numero", code="is_alpha"
                )
            )

        if len(password) < 8:
            erro_dict.append(
                ValidationError(
                    "La contraseña debe tener al menos 8 caracteres",
                    code="is_too_short",
                )
            )

        if erro_dict:
            raise ValidationError(erro_dict)

        return password

    def clean_password2(self):
        error_dict = []

        password1 = self.data["password1"]
        password2 = self.cleaned_data["password2"]

        print("CLEAN PASSWORD 2")

        if password1 != password2:
            error_dict.append(
                ValidationError("Las contraseñas no coinciden", code="no_match")
            )

        if error_dict:
            raise ValidationError(error_dict)

        return password2

    def _post_clean(self):
        return

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["username"]

        if commit:
            user.save()

        return user


class CustomAuthForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre de usuario"}),
            "password": forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Contraseña"})

        }