from django.urls import path
from ..views_rl.multipleUp import views

urlpatterns = [
    path('MultiUpload', views.createMultiImage, name='image_multiple'),
    path('delMultiImage/<str:id>', views.deleteMultiImage, name='delete_multi_image'),
]