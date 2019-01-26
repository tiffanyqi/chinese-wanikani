from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [ 
    path('login/', auth_views.LoginView.as_view(template_name='wanikani/registration/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
]
