from .models import BlackWhiteImage
from django.forms import ModelForm


class BlackWhiteImageForm(ModelForm):

    class Meta:
        # Название модели на основе
        # которой создается форма
        model = BlackWhiteImage
        # Включаем все поля с модели в форму
        fields = '__all__'
