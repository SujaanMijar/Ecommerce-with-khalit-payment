from django.urls import path,include
from .views import *
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('',log_in,name='log_in'),
    path('signup/',signup,name='signup'),
    path('log_out/',log_out,name="log_out"),
    path("password_change/",change_password,name="password_change"),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='account/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'), name='password_reset_complete'),
    path('profile/',profile,name='profile'),
    path('update_profile/',update_profile,name='update_profile'),
    path('reset_password/',reset_password,name='reset_password'),
    path('order/',my_order,name='my_order'),
]
