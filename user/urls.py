from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path('login', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('registration', views.register, name='registration'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('add_friend/<str:username>', views.add_friend, name='add_friend'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('edit_account', views.edit_account, name='edit_account'),
    path('delete_account', views.delete_account, name='delete_account')
]
