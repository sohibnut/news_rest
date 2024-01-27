from django.urls import path
from .views import (SignUpView, PersonalDataView, PasswordChangeView,
                    LoginView, LogoutView, AccessRefreshView, PasswordResetView,
                    PasswordResetViaCodeView, ProfileView)

urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('personal_data/', PersonalDataView.as_view()),
    path('password_change/', PasswordChangeView.as_view()),
    path('password_reset/', PasswordResetView.as_view()),
    path('password_reset_code/', PasswordResetViaCodeView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('refresh_token/', AccessRefreshView.as_view()),
    path('profile/', ProfileView.as_view()),
]