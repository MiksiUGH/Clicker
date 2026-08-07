"""Django-формы"""

from django import forms


class RegisterForm(forms.Form):
    """Форма регистрации"""

    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Введите имя",
                "class": "form-control",
                "id": "name",
                "name": "name",
                "type": "text",
            }
        ),
        required=True,
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Введите пароль",
                "class": "form-control",
                "id": "password",
                "name": "password",
                "type": "password",
            }
        ),
        required=True,
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Повторите пароль",
                "class": "form-control",
                "id": "password2",
                "name": "password2",
                "type": "password",
            }
        ),
        required=True,
    )

    def clean(self):
        """Проверка совпадения паролей"""
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            self.add_error("password2", "Пароли не совпадают")
        return cleaned_data


class LoginForm(forms.Form):
    """Форма входа"""

    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "id": "name",
                "name": "name",
                "placeholder": "Введите имя",
            }
        ),
        required=True,
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={
                "type": "password",
                "class": "form-control",
                "id": "password",
                "name": "password",
                "placeholder": "Введите пароль",
            }
        ),
        required=True,
    )
