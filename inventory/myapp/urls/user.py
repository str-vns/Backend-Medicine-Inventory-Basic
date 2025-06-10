from django.urls import path
from ..views_rl.user import views

urlpatterns = [
    #Create
    path('user', views.create_a_new_user, name='create_a_new_user'),
    #Read
    path('users', views.get_all_users, name='get_all_users'),
    #Update
    path('user/patch/<str:user_id>', views.update_user, name='update_user'),
    #Delete
    path('user/delete/<str:user_id>', views.delete_user, name='delete_user'),
    #SingleUser
    path('user/profile/<str:user_id>', views.get_profile, name='get_profile'),
    # Login
    path('user/login', views.login_user, name='login_user'),
]