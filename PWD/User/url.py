from django.urls import path
from .views import RegisterView,LoginView,UserView,LogoutView, StaffRegistration

app_name= "User"
urlpatterns = [
    path('register', RegisterView.as_view(),name='user-register'),
    path('login', LoginView.as_view(),name='user-login' ),
    path('user', UserView.as_view(),name='user-view' ),
    path('logout', LogoutView.as_view(),name='user-logout' ),
    path('staffRegistrartion',  StaffRegistration.as_view(),name='staff-registartion' )
]  