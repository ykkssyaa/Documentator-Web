from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
import django.forms as forms


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Должность", widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']