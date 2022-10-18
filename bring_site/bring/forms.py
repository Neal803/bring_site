from django.contrib.auth import authenticate, password_validation
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.forms import Form
from django.core.exceptions import ValidationError

from django import forms
from django.utils.html import format_html_join, format_html

from .models import CustomUser, Comment
from .utils import send_email_for_verify
from django.utils.translation import gettext_lazy as _


def _password_validators_help_text_html():
    help_texts = [
        'Пароль має містити не меньше 8 символів',
        'Пароль не може бути лише з цифр'
    ]
    help_items = format_html_join(
        "", "<li>{}</li>", ((help_text,) for help_text in help_texts)
    )
    return format_html("<ul>{}</ul>", help_items) if help_items else ""


class RegisterUserForm(UserCreationForm):
    # username = forms.CharField(label='Логін', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email_reg = forms.EmailField(label='e-mail', widget=forms.TextInput(attrs={'class': 'form-input'}))
    first_name = forms.CharField(label='Ім\'я', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор Паролю', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = CustomUser
        fields = ['email_reg', 'first_name',  'password1', 'password2']


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name']


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='E-mail', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            if not self.user_cache.email_verify:
                send_email_for_verify(self.request, self.user_cache)
                raise ValidationError('Email not verify. Chek email', code='invalid-login')
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data


class AuthenticationAjaxForm(forms.Form):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={
            "autocomplete": "email",
            "class": "form-control",
        }),
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            "autocomplete": "current-password",
            "class": "form-control",
        }),
    )


class RegistrationAjaxForm(UserCreationForm):
    # username = forms.CharField(label='Логін', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email_reg = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={
            "autocomplete": "email",
            "class": "form-control",
        }),
    )
    name = forms.CharField(
        label=_("Ім'я"),
        max_length=254,
        widget=forms.TextInput(attrs={
            "autocomplete": "name",
            "class": "form-control",
        })
    )
    communication = forms.CharField(
        label=_("Спосіб зв'язку (Номер телефону, Telegram, Viber тощо)"),
        max_length=254,
        widget=forms.TextInput(attrs={
            "autocomplete": "name",
            "class": "form-control",
        }),
    )
    password1 = forms.CharField(
        label=_("Пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "form-control"}),
        help_text=_password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Підтвердження паролю"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "form-control"}),
        strip=False,
    )

    class Meta:
        model = CustomUser
        fields = ('email_reg', 'name', 'communication', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegistrationAjaxForm, self).__init__(*args, **kwargs)
        self.fields['communication'].required = False


class CommentForm(Form):
    class Meta:
        model = Comment
        fields = ['comment_text', 'rating_vote']
