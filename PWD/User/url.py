from django.urls import path
from .views import RegisterView,LoginView,UserView,LogoutView, StaffRegistration, VerifyOTP,ForgotPasswordView,ResetPasswordView,UserEditProfileView

app_name= "User"
urlpatterns = [
    path('register', RegisterView.as_view(),name='user-register'),
    path('login', LoginView.as_view(),name='user-login' ),
    path('user', UserView.as_view(),name='user-view' ),
    path('logout', LogoutView.as_view(),name='user-logout' ),
    path('staffRegistration',  StaffRegistration.as_view(),name='staff-registartion' ),
    path('verifyotp', VerifyOTP.as_view(),name='verify_otp' ),
    path('userget', UserEditProfileView.as_view(),name='user_get' ),
    path('useredit', UserEditProfileView.as_view(),name='user_edit' ),

    path('forgotpassword', ForgotPasswordView.as_view(),name='forgot_password' ),
    path('resetpassword', ResetPasswordView.as_view(),name='reset-password' ),
    path('resetpassword/', ResetPasswordView.as_view(),name='reset-password' ),

]