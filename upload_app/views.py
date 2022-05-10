from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.views.generic import CreateView
from .forms import BlackWhiteImageForm
from .models import BlackWhiteImage


class BookCreate(CreateView):
    # Модель куда выполняется сохранение
    model = BlackWhiteImage
    # Класс на основе которого будет валидация полей
    form_class = BlackWhiteImageForm
    # Выведем все существующие записи на странице
    extra_context = {'books': BlackWhiteImage.objects.all()}
    # Шаблон с помощью которого
    # будут выводиться данные
    template_name = 'book_create.html'
    # На какую страницу будет перенаправление
    # в случае успешного сохранения формы
    success_url = '/image/book/'

def image_page(request):
    # POST - обязательный метод
    if request.method == 'POST' and request.FILES:
        # получаем загруженный файл
        file = request.FILES['myfile1']
        fs = FileSystemStorage()
        # сохраняем на файловой системе
        filename = fs.save(file.name, file)
        # получение адреса по которому лежит файл
        file_url = fs.url(filename)
        return render(request, 'image_page.html', {
            'file_url': file_url,
        })
    return render(request, 'image_page.html')
