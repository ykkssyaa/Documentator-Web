from django.urls import path

from users import views as views

urlpatterns = [
    path('login', views.LoginUser.as_view(), name='login'),
    path('logout', views.logout_user, name='logout'),
]
