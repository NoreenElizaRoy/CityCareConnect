from django.urls import path
from .views import RegisterView,LoginView

app_name= "User"
urlpatterns = [
    path('register', RegisterView.as_view(),name='user-register'),
    path('login', LoginView.as_view(),name='user-login' )
    
]