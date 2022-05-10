from django.urls import path
from .views import Image_Model_Predict

urlpatterns = [
    path('predict/image/', Image_Model_Predict.as_view(), name='api_image_predict'),
    path('predict/image/<int:pk>/', Image_Model_Predict.as_view(), name='api_image_predict1'),
]
