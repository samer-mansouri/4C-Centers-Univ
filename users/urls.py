from django.urls import path
from .views import (
    #ProtectorRegistrationView,  
    StudentRegistrationView, 
    MyTokenObtainPairView,
    GetProtectors,
    GetStudents,
    GetProtector,
    LogoutView,
    )
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView


urlpatterns = [
    #Registration Urls
    #path('registration/protector/', ProtectorRegistrationView.as_view(), name='register-protector'),
    path('registration/student/', StudentRegistrationView.as_view(), name='register-student'),
    path('login/token/', MyTokenObtainPairView.as_view(), name='token_obtain'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('protectors/', GetProtectors.as_view(), name='protectors'),
    path('protector/<int:pk>/', GetProtector.as_view(), name='protector-update'),     
    path('students/', GetStudents.as_view(), name='students'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
]