from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.validators import UnicodeUsernameValidator

from .models import Person

username_validator = UnicodeUsernameValidator()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=50,
        help_text="Required. Inform a valid email address.",
        widget=(forms.TextInput(attrs={"class": "form-control"})),
    )
    password1 = forms.CharField(
        label="Password",
        widget=(forms.PasswordInput(attrs={"class": "form-control"})),
        help_text=password_validation.password_validators_help_text_html,
    )
    password2 = forms.CharField(
        label="Password Confirmation",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        help_text="Just Enter the same password, for confirmation",
    )
    username = forms.CharField(
        label="Username",
        max_length=150,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        validators=[username_validator],
        error_messages={"unique": "A user with that username already exists."},
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Person
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )


class CustomUserChangeForm(UserChangeForm):
    first_name = forms.CharField(
        max_length=12,
        min_length=2,
        required=False,
        help_text="Optional: First Name",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    last_name = forms.CharField(
        max_length=12,
        min_length=2,
        required=False,
        help_text="Optional: Last Name",
        widget=(forms.TextInput(attrs={"class": "form-control"})),
    )
    email = forms.EmailField(
        max_length=50,
        required=False,
        help_text="Required. Inform a valid email address.",
        widget=(forms.TextInput(attrs={"class": "form-control"})),
    )
    image = forms.ImageField(
        required=False,
        widget=(forms.FileInput(attrs={"class": "form-control", "type": "file"})),
    )
    about = forms.CharField(
        required=False,
        widget=(forms.Textarea(attrs={"class": "form-control", "type": "textarea"})),
    )
    username = forms.CharField(
        label="Username",
        max_length=150,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        validators=[username_validator],
        error_messages={"unique": "A user with that username already exists."},
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
    )

    class Meta:
        model = Person
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "image",
            "about",
        )
