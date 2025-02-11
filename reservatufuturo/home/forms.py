from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, get_user_model

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Correo electrónico", widget=forms.EmailInput(attrs={'autofocus': True}))

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            UserModel = get_user_model()
            try:
                user = UserModel.objects.get(email=email)
                self.confirm_login_allowed(user)
            except UserModel.DoesNotExist:
                raise forms.ValidationError("Correo electrónico o contraseña incorrectos.", code='invalid_login')

            self.user_cache = authenticate(self.request, username=user.username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Correo electrónico o contraseña incorrectos.", code='invalid_login')
        return self.cleaned_data
    
class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        required=True,
        label="Nombre de usuario",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'})
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label="Nombre",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label="Apellidos",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'})
    )
    phone_number = forms.CharField(
        max_length=15,
        required=True,
        label="Número de teléfono",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de teléfono'})
    )

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "phone_number", "password1", "password2"]

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit():
            raise ValidationError("El número de teléfono solo debe contener dígitos.")
        if len(phone_number) > 15:
            raise ValidationError("El número de teléfono debe tener menos de 15 dígitos.")
        return phone_number

    def save(self, commit=True):
        self.full_clean()
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile, created = Profile.objects.get_or_create(user=user)
            profile.phone_number = self.cleaned_data['phone_number']
            profile.save()
        return user
    
class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(
        max_length=30,
        required=True,
        label="Nombre de usuario",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'})
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label="Nombre",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label="Apellidos",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'})
    )
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]

class ProfileUpdateForm(forms.ModelForm):
    phone_number = forms.CharField(
        max_length=15,
        required=True,
        label="Número de teléfono",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de teléfono'})
    )

    class Meta:
        model = Profile
        fields = ['phone_number']

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit():
            raise ValidationError("El número de teléfono solo debe contener dígitos.")
        if len(phone_number) > 15:
            raise ValidationError("El número de teléfono debe tener menos de 15 dígitos.")
        return phone_number