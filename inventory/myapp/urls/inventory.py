from django.urls import path
from ..views_rl.inventory import views

urlpatterns = [
    path('inventory', views.create_inventory, name='create_inventory'),
    path('inventories', views.get_all_inventories, name='get_all_inventories'),
    path('inventory/single/<str:inventory_id>', views.get_single_inventory, name='get_single_inventory'),
    path('inventory/patch/<str:inventory_id>', views.update_inventory, name='update_inventory'),
]