import matplotlib.pyplot as plt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .apps import PredictionConfig, PredictionImageConfig
import pandas as pd
import PIL
from torchvision import transforms
from .utils import lab_to_rgb
import torch
from .models import Post
from .serializers import PostSerializer

# Create your views here.


class Image_Model_Predict(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        posts = Post.objects.order_by('-id')[:12]
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=200)
        # return render(request, 'image_page.html')
        # return Response(status=200)

    def post(self, request, *args, **kwargs):
        posts_serializer = PostSerializer(data=request.data)
        if posts_serializer.is_valid():
            posts_serializer.save()

        if request.method == 'POST' and request.FILES:
            # получаем загруженный файл
            file = posts_serializer.save()
            # file = request.FILES.get('myfile1', false);
            fs = FileSystemStorage()
            # сохраняем на файловой системе
            # filename = fs.save(file, file)
            # получение адреса по которому лежит файл
            picture = Post.objects.order_by('-id').all()[0].image
            file_url = fs.url(picture)

            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            loaded_mlmodel = PredictionImageConfig.mlmodel
            img = PIL.Image.open(f'C:/DiplomaProjects/ProjectOne/backend/django_app{file_url}')
            width, height = img.size

            img = img.resize((256, 256))
            # to make it between -1 and 1
            img = transforms.ToTensor()(img)[:1] * 2. - 1.
            loaded_mlmodel.eval()
            with torch.no_grad():
                preds = loaded_mlmodel.net_G(img.unsqueeze(0).to(device))
            colorized = lab_to_rgb(img.unsqueeze(0), preds.cpu())[0]

            plt.imshow(colorized)
            ax = plt.gca()
            plt.axis('off')
            plt.savefig('C:/DiplomaProjects/ProjectOne/backend/django_app/media/results/col_' + f'{picture}'[12:], bbox_inches='tight', pad_inches=0)

            new_img = PIL.Image.open('C:/DiplomaProjects/ProjectOne/backend/django_app/media/results/col_' + f'{picture}'[12:])
            result_image = new_img.resize((width, height))
            result_image = result_image.save('C:/DiplomaProjects/ProjectOne/backend/django_app/media/results/res_' + f'{picture}'[12:])

            return Response(posts_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('error', posts_serializer.errors)
            return Response(posts_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

