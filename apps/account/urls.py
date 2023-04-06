from django.urls import path

from . import views

urlpatterns = [
    path('', views.account, name='account'),
    path('all_tests', views.all_tests, name='all_tests'),
    path('register/', views.register, name='register'),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name= "logout"),

    path('test/<int:pk>', views.test, name='test'),
    path('test/<int:pk>/pass', views.pass_test, name='pass_test'), 
]