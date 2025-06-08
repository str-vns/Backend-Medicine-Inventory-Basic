from django.urls import path
from ..views_rl.multipleUp import views

urlpattern = [
    path('imageMultiple', views.image_multiple, name='image_multiple')
]