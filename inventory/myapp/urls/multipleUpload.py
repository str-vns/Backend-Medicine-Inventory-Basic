from django.urls import path
from ..views_rl.multipleUp import views

urlpatterns = [
    path('MultiUpload', views.createMultiImage, name='image_multiple')
]