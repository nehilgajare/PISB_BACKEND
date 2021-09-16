from django.urls import path
from . import views 

urlpatterns = [
    path('', views.signup ,name='signup') , 
    path('login/', views.login ,name='login') , 
    path('search/', views.search ,name='search') , 
    # path('login_view/', views.login_view ,name='login_view') , 
]