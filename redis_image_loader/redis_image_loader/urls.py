from django.urls import path
from imageprocessor import views

urlpatterns = [
    path('load-images/', views.load_images_to_redis, name='load_images_to_redis'),
]
