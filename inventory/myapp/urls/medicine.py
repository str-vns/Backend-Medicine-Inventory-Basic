from django.urls import path
from ..views_rl.medicine import views

urlpatterns = [
    path('medicine', views.create_medicine, name='create_medicine'),
    path('medicines', views.get_all_medicines, name='get_all_medicines'),
    path('medicine/patch/<str:medicine_id>', views.get_Update_medicines, name='get_Update_medicines'),
    path('medicine/delete/<str:medicine_id>',views.delete_medicine, name='delete_medicine'),
    path('medicine/<str:medicine_id>', views.single_medicine, name='single_medicine'), 
]