from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django.core.mail import send_mail
from django.conf import settings


class CustomUserCreationForm(UserCreationForm):
    """Форма для создания и валидации нового пользователя"""
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш email'
        })
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )

    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите пароль'
        })
    )

    class Meta:
        model = CustomUser
        fields = ("email",)

    def clean_email(self):
        """Проверка уникальности email"""
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует')
        return email

    def save(self, commit=True):
        """Сохраняет пользователя и отправляет приветственное письмо"""

        user = super().save(commit=False)

        if commit:
            user.save()                    # cохраняем пользователя в БД
            self.send_welcome_email(user)  # отправляем письмо

        return user

    def send_welcome_email(self, user):
        """Отправляет приветственное письмо пользователю"""

        subject = 'Добро пожаловать в Skystore!'
        message = f'''Здравствуйте, {user.email}!

Спасибо за регистрацию в нашем интернет-магазине Skystore!

Теперь вы можете:
- Просматривать каталог товаров
- Добавлять новые продукты
- Управлять своими объявлениями

Желаем приятных покупок!

С уважением,
Команда Skystore'''

        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=recipient_list,
            )
            print(f"Приветственное письмо отправлено на {user.email}")
        except Exception as e:
            print(f"Не удалось отправить письмо: {e}")


class CustomAuthenticationForm(AuthenticationForm):
    """Форма для существующего в БД пользователя для входа в систему по email"""
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш email'
        })
    )

    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )

    error_messages = {
        'invalid_login': 'Пожалуйста, введите правильные email и пароль.',
        'inactive': 'Этот аккаунт неактивен.',
    }
